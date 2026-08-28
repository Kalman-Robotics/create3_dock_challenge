"""Create 3 oficial + LiDAR, nada mas.

Replica create3_spawn.launch.py del paquete oficial cambiando UNICAMENTE la
descripcion del robot, para montarle el LiDAR encima. Dock, nodos del Create 3
y controladores quedan exactamente como en el oficial.

No se incluye create3_spawn.launch.py directamente porque ese launch trae su
propio robot_state_publisher cableado al create3.urdf.xacro oficial; dos nodos
con el mismo nombre compiten por /robot_description y gana uno arbitrario.
"""

import os
from pathlib import Path

from ament_index_python.packages import get_package_share_directory

from irobot_create_common_bringup.namespace import GetNamespacedName
from irobot_create_common_bringup.offset import OffsetParser, RotationalOffsetX, RotationalOffsetY

from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, GroupAction,
                            IncludeLaunchDescription, SetEnvironmentVariable)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (Command, EnvironmentVariable, LaunchConfiguration,
                                  PathJoinSubstitution, PythonExpression)
from launch_ros.actions import Node, PushRosNamespace
from launch_ros.parameter_descriptions import ParameterValue


ARGUMENTS = [
    DeclareLaunchArgument('use_rviz', default_value='true',
                          choices=['true', 'false'],
                          description='Abrir RViz junto con Gazebo, con la '
                                      'configuracion de rviz/dock_challenge.rviz. '
                                      'false para lanzar solo la simulacion.'),
    DeclareLaunchArgument('use_gazebo_gui', default_value='true',
                          choices=['true', 'false'],
                          description='false para correr Gazebo headless.'),
    DeclareLaunchArgument('lidar_x', default_value='-0.050502',
                          description='Pose del LiDAR en x respecto a base_link. '
                                      'Cotas reales del RRBOT (rbot_description).'),
    DeclareLaunchArgument('lidar_y', default_value='-0.017960',
                          description='Pose del LiDAR en y respecto a base_link.'),
    DeclareLaunchArgument('lidar_z', default_value='0.1775',
                          description='Altura del CENTRO del LiDAR sobre '
                                      'base_link. 0.1775 = tapa del robot '
                                      '(0.092) + caja soporte (0.065) + medio '
                                      'sensor (0.0205).'),
    DeclareLaunchArgument('lidar_yaw', default_value='3.14',
                          description='Yaw del LiDAR. 3.14 = montado del reves, '
                                      'como en el robot real.'),
    DeclareLaunchArgument('visualize_lidar', default_value='false',
                          choices=['true', 'false'],
                          description='Dibujar el haz del LiDAR en Gazebo. '
                                      'Apagado por defecto: cuesta rendimiento '
                                      'y tapa la escena. true para depurar.'),
    DeclareLaunchArgument('visualize_rays', default_value='false',
                          choices=['true', 'false'],
                          description='Dibujar los conos IR del Create 3 y del dock.'),
    DeclareLaunchArgument('safety_override', default_value='full',
                          choices=['none', 'backup_only', 'full'],
                          description='Modo de seguridad del Create 3, aplicado '
                                      'automaticamente al arrancar. none = sin '
                                      'retroceso; backup_only = permite '
                                      'retroceder; full = ademas sin cliffs y '
                                      'velocidad maxima 0.46 m/s.'),
    DeclareLaunchArgument('lidar_noise', default_value='0.001',
                          description='Ruido gaussiano del LiDAR (stddev en m). '
                                      '0.001 = 1 mm. Subelo para simular un '
                                      'sensor peor, o 0.0 para ruido nulo.'),
    DeclareLaunchArgument('spawn_dock', default_value='true',
                          choices=['true', 'false'],
                          description='Spawnear la estacion de carga.'),
    DeclareLaunchArgument('world_path', default_value='',
                          description='Mundo a cargar. Vacio = empty.world.'),
    DeclareLaunchArgument('namespace', default_value='',
                          description='Namespace del robot.'),
    DeclareLaunchArgument('dock_x', default_value='',
                          description='Pose absoluta del dock en x. Vacio = '
                                      '0.157 m delante del robot (oficial).'),
    DeclareLaunchArgument('dock_y', default_value='0.0',
                          description='Pose absoluta del dock en y. Solo se '
                                      'usa si dock_x tiene valor.'),
    DeclareLaunchArgument('dock_yaw', default_value='3.1416',
                          description='Yaw absoluto del dock. Solo se usa si '
                                      'dock_x tiene valor.'),
]

for pose_element in ['x', 'y', 'z', 'yaw']:
    ARGUMENTS.append(DeclareLaunchArgument(pose_element, default_value='0.0',
                     description=f'Componente {pose_element} de la pose del robot.'))

os.environ['LC_NUMERIC'] = 'en_US.UTF-8'


def _cargar_guarda():
    """Importa sim_guard.py del directorio launch instalado."""
    import importlib.util

    ruta = os.path.join(
        get_package_share_directory('create3_dock_challenge'),
        'launch', 'sim_guard.py')
    spec = importlib.util.spec_from_file_location('sim_guard', ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def generate_launch_description():
    _cargar_guarda().abortar_si_ya_hay_simulacion()
    pkg_challenge = get_package_share_directory('create3_dock_challenge')
    pkg_common_bringup = get_package_share_directory('irobot_create_common_bringup')
    pkg_gazebo_bringup = get_package_share_directory('irobot_create_gazebo_bringup')

    # Gazebo Classic resuelve las URI package://<pkg>/... buscando <pkg> dentro
    # de los directorios de GAZEBO_MODEL_PATH. gazebo.launch.py del paquete
    # oficial solo añade el share/ de /opt/ros, asi que el mesh del LiDAR
    # (package://create3_dock_challenge/meshes/rplidar_c1.dae) no se encuentra.
    #
    # El separador va AL FINAL, no al principio: esta accion se evalua antes
    # que la del launch oficial, y aquella concatena su valor detras sin poner
    # ':'. Con el separador delante quedaba
    #   .../create3_dock_challenge/share/usr/share/gazebo-11/models/
    # o sea las dos rutas pegadas, y se perdia /usr/share/gazebo-11/models/.
    # Sin esa ruta Gazebo no encuentra sun ni ground_plane en local e intenta
    # descargarlos de internet, que es lo que hacia lentisima la carga.
    gz_model_path = SetEnvironmentVariable(
        name='GAZEBO_MODEL_PATH',
        value=[EnvironmentVariable('GAZEBO_MODEL_PATH', default_value=''),
               str(Path(pkg_challenge).parent.resolve()), ':'])

    # Sin base de datos remota: si algun modelo no esta en local, que falle
    # rapido en vez de quedarse esperando a gazebosim.org.
    gz_model_db = SetEnvironmentVariable(name='GAZEBO_MODEL_DATABASE_URI', value='')

    robot_xacro = PathJoinSubstitution([pkg_challenge, 'urdf', 'robot.urdf.xacro'])
    gazebo_launch = PathJoinSubstitution(
        [pkg_gazebo_bringup, 'launch', 'gazebo.launch.py'])
    dock_description_launch = PathJoinSubstitution(
        [pkg_common_bringup, 'launch', 'dock_description.launch.py'])
    create3_nodes_launch = PathJoinSubstitution(
        [pkg_common_bringup, 'launch', 'create3_nodes.launch.py'])
    rviz_config = PathJoinSubstitution(
        [pkg_challenge, 'rviz', 'dock_challenge.rviz'])

    namespace = LaunchConfiguration('namespace')
    use_rviz = LaunchConfiguration('use_rviz')
    spawn_dock = LaunchConfiguration('spawn_dock')
    visualize_rays = LaunchConfiguration('visualize_rays')
    x, y, z = (LaunchConfiguration('x'), LaunchConfiguration('y'),
               LaunchConfiguration('z'))
    yaw = LaunchConfiguration('yaw')

    robot_name = GetNamespacedName(namespace, 'create3')
    dock_name = GetNamespacedName(namespace, 'standard_dock')

    # Pose del dock. Con dock_x vacio (por defecto) se coloca 0.157 m delante
    # del robot mirandolo de frente, igual que el launch oficial. Si se le pasa
    # un valor, se usa como pose absoluta: hace falta cuando el dock debe
    # quedar fijo en el escenario (pegado a la pared de las cajas) y el robot
    # arranca lejos de el.
    dock_x = LaunchConfiguration('dock_x')
    dock_y = LaunchConfiguration('dock_y')
    dock_yaw = LaunchConfiguration('dock_yaw')

    x_dock_rel = OffsetParser(x, RotationalOffsetX(0.157, yaw))
    y_dock_rel = OffsetParser(y, RotationalOffsetY(0.157, yaw))
    yaw_dock_rel = OffsetParser(yaw, 3.1416)

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([gazebo_launch]),
        launch_arguments=[
            ('world_path', LaunchConfiguration('world_path')),
            ('use_gazebo_gui', LaunchConfiguration('use_gazebo_gui')),
        ]
    )

    spawn_group = GroupAction([

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([dock_description_launch]),
            launch_arguments={'gazebo': 'classic'}.items(),
            condition=IfCondition(spawn_dock),
        ),
        # Dock relativo al robot (comportamiento oficial, dock_x vacio)
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            name='spawn_standard_dock',
            arguments=['-entity', dock_name,
                       '-topic', 'standard_dock_description',
                       '-x', x_dock_rel, '-y', y_dock_rel,
                       '-z', z, '-Y', yaw_dock_rel],
            output='screen',
            condition=IfCondition(
                PythonExpression(["'", spawn_dock, "' == 'true' and '",
                                  dock_x, "' == ''"])),
        ),
        # Dock en pose absoluta (cuando se pasa dock_x)
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            name='spawn_standard_dock',
            arguments=['-entity', dock_name,
                       '-topic', 'standard_dock_description',
                       '-x', dock_x, '-y', dock_y, '-z', z, '-Y', dock_yaw],
            output='screen',
            condition=IfCondition(
                PythonExpression(["'", spawn_dock, "' == 'true' and '",
                                  dock_x, "' != ''"])),
        ),

        # NO se lanza joint_state_publisher a proposito, aunque el launch
        # oficial de iRobot si lo haga.
        #
        # En simulacion, joint_state_broadcaster (de ros2_control, dentro de
        # Gazebo) ya publica /joint_states con la posicion REAL de las ruedas.
        # joint_state_publisher publica ademas las mismas juntas a 0.0 porque
        # no tiene fuente. robot_state_publisher recibe las dos y alterna:
        # medido 6416 msgs con la posicion real contra 71 msgs a cero, y ese
        # reset intermitente hace que las ruedas peguen saltos en RViz.
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            parameters=[
                {'use_sim_time': True},
                # Command DESNUDO, sin ParameterValue: es el patron del
                # robot_description.launch.py oficial. Envolverlo hace que el
                # URDF entero viaje como argumento de linea de comandos a
                # gazebo_ros2_control, rcl lo trunca a medio atributo y el
                # plugin muere ("Couldn't parse parameter override rule").
                # Sin PushRosNamespace por encima, launch ya no necesita el
                # ParameterValue.
                # ParameterValue(..., value_type=str) es OBLIGATORIO.
                # Sin el, launch_ros intenta interpretar el URDF como YAML y
                # cualquier ':' suelto (dentro de un comentario, por ejemplo)
                # tumba el launch entero con 'Unable to parse the value of
                # parameter robot_description as yaml'.
                {'robot_description': ParameterValue(Command([
                    'xacro', ' ', robot_xacro, ' ',
                    'gazebo:=', 'classic', ' ',
                    'lidar_x:=', LaunchConfiguration('lidar_x'), ' ',
                    'lidar_y:=', LaunchConfiguration('lidar_y'), ' ',
                    'lidar_z:=', LaunchConfiguration('lidar_z'), ' ',
                    'lidar_yaw:=', LaunchConfiguration('lidar_yaw'), ' ',
                    'visualize_lidar:=', LaunchConfiguration('visualize_lidar'), ' ',
                    'lidar_noise:=', LaunchConfiguration('lidar_noise'), ' ',
                    'visualize_rays:=', visualize_rays, ' ',
                    'namespace:=', namespace]), value_type=str)},
            ],
            remappings=[('/tf', 'tf'), ('/tf_static', 'tf_static')],
        ),

        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            name='spawn_create3',
            arguments=['-entity', robot_name,
                       '-topic', 'robot_description',
                       '-x', x, '-y', y, '-z', z, '-Y', yaw],
            output='screen',
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([create3_nodes_launch]),
            launch_arguments=[('namespace', namespace)],
        ),

        # El Create 3 arranca con safety_override='none', que NO deja
        # retroceder. Este nodo espera a motion_control y le aplica el valor
        # de safety_override; termina solo en cuanto lo consigue.
        Node(
            package='create3_dock_challenge',
            executable='set_safety_override.py',
            name='set_safety_override',
            output='screen',
            parameters=[{
                'use_sim_time': True,
                'value': LaunchConfiguration('safety_override'),
            }],
        ),

        # RViz con la configuracion de este paquete (rviz/dock_challenge.rviz),
        # no con rviz2.launch.py del paquete oficial: aquella carga la config de
        # iRobot, que no trae el LaserScan ni los frames del LiDAR.
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config],
            parameters=[{'use_sim_time': True}],
            output='screen',
            condition=IfCondition(use_rviz),
            remappings=[('/tf', 'tf'), ('/tf_static', 'tf_static')],
        ),
    ])

    ld = LaunchDescription(ARGUMENTS)
    # Antes de arrancar Gazebo, para que encuentre los meshes del paquete.
    ld.add_action(gz_model_path)
    ld.add_action(gz_model_db)
    ld.add_action(gazebo)
    ld.add_action(spawn_group)
    return ld
