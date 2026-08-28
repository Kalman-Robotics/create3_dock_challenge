"""Reto de docking con LiDAR: Create 3 + LiDAR en el escenario del laboratorio.

Envuelve create3_lidar.launch.py fijando el mundo con la pared, las cajas
marcadoras y el dock, mas una pose inicial de aproximacion.

ESCENARIO (cotas del montaje real, ver foto de referencia)
  cajas         8 x 8 cm de planta, 12 cm de alto, de z=0.13 a z=0.25
  hueco         9.5 cm entre caja y caja (17.5 cm entre centros)
  pared         cara interior en x = 1.95
  cajas         centro x = 1.9095, cara frontal en 1.8695
  dock          x = 1.85, al pie de las cajas
  LiDAR         plano de escaneo a z = 0.1775, dentro de la banda de las cajas
  soporte       caja blanca 16 x 11 x 6.5 cm sobre la tapa del robot

FIRMA QUE VE EL LASER (verificada a 46 cm de las cajas)
  dos escalones de ~8 cm de ancho que sobresalen ~8 cm sobre el fondo,
  separados por un hueco de 9.5 cm donde se ve la pared. El centro del
  hueco es el eje del dock.
"""

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution


ARGUMENTS = [
    DeclareLaunchArgument('use_rviz', default_value='true',
                          choices=['true', 'false'],
                          description='Abrir RViz junto con Gazebo, con la '
                                      'configuracion de rviz/dock_challenge.rviz. '
                                      'false para lanzar solo la simulacion.'),
    DeclareLaunchArgument('use_gazebo_gui', default_value='true',
                          choices=['true', 'false'],
                          description='false para correr Gazebo headless.'),
    DeclareLaunchArgument('lidar_z', default_value='0.1775',
                          description='Altura del CENTRO del LiDAR sobre '
                                      'base_link. 0.1775 = tapa del robot '
                                      '(0.092) + caja soporte (0.065) + medio '
                                      'sensor (0.0205).'),
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
]

# Pose inicial de aproximacion, tomada de la posicion en la que se dejo el
# robot tras las pruebas manuales: a ~1.44 m del dock y ligeramente descentrado
# y girado, para que la aproximacion no salga de una pose perfecta.
#
# No arranca acoplado a proposito: encima de la rampa del dock el robot queda
# inclinado ~6 grados y resbala. Desde aqui hay que cerrar la distancia
# guiandose solo por el LiDAR.
#
# Ojo con los waypoints del dock server: estan en [1.10, 0.75, 0.40] m del
# dock, asi que desde 1.44 m el robot los recorre todos hacia adelante.
ROBOT_X = '0.4113'
ROBOT_Y = '-0.1825'
ROBOT_YAW = '0.3601'   # 20.63 grados

# El dock va al pie de las cajas, centrado en el hueco. Pose absoluta, no
# relativa al robot: el robot arranca lejos y el dock debe quedarse fijo.
#
# x=1.85 deja 12.5 cm de holgura hasta la pared (cara interior en 1.95) y lo
# situa justo delante de las cajas (cara frontal en 1.885), como en la foto del
# montaje real. Ojo: el modelo visual del dock es bastante mayor que su caja de
# colision, asi que si se acerca mas parece incrustado en la pared aunque
# fisicamente no la toque.
DOCK_X = '1.85'
DOCK_Y = '0.0'
DOCK_YAW = '3.1416'   # mira hacia el centro de la sala

for name, default in [('x', ROBOT_X), ('y', ROBOT_Y), ('yaw', ROBOT_YAW)]:
    ARGUMENTS.append(DeclareLaunchArgument(
        name, default_value=default,
        description=f'Componente {name} de la pose inicial del robot.'))


def generate_launch_description():
    pkg = get_package_share_directory('create3_dock_challenge')

    base_launch = PathJoinSubstitution([pkg, 'launch', 'create3_lidar.launch.py'])
    world = PathJoinSubstitution([pkg, 'worlds', 'dock_challenge.world'])

    sim = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([base_launch]),
        launch_arguments=[
            ('world_path', world),
            ('use_rviz', LaunchConfiguration('use_rviz')),
            ('use_gazebo_gui', LaunchConfiguration('use_gazebo_gui')),
            ('lidar_z', LaunchConfiguration('lidar_z')),
            ('visualize_lidar', LaunchConfiguration('visualize_lidar')),
            ('visualize_rays', LaunchConfiguration('visualize_rays')),
            ('lidar_noise', LaunchConfiguration('lidar_noise')),
            ('safety_override', LaunchConfiguration('safety_override')),
            ('x', LaunchConfiguration('x')),
            ('y', LaunchConfiguration('y')),
            ('yaw', LaunchConfiguration('yaw')),
            # El dock va fijo al pie de las cajas, no relativo al robot.
            ('dock_x', DOCK_X),
            ('dock_y', DOCK_Y),
            ('dock_yaw', DOCK_YAW),
        ]
    )

    ld = LaunchDescription(ARGUMENTS)
    ld.add_action(sim)
    return ld
