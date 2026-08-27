#!/usr/bin/env bash
# Deja el entorno limpio antes de lanzar una simulacion.
#
# Gazebo y los nodos de ROS sobreviven a un Ctrl-C mal dado, y las instancias
# huerfanas se acumulan: dos gzserver pelean por el mismo puerto, y varios
# robot_state_publisher compiten por /robot_description sirviendo modelos
# distintos. Los sintomas son confusos (topicos que no publican, plugins que
# fallan, el robot que no responde), asi que conviene limpiar siempre.
#
#   uso:  ./clean_sim.sh          limpia
#         ./clean_sim.sh --check  solo informa, no mata nada

set -u

# lidar_dock_server incluido a proposito: dos instancias con el mismo nombre de
# nodo publican los mismos TF (corner_left, corner_right, dock_target) con
# detecciones distintas, y los frames saltan cientos de mm en RViz.
PATTERN='gzserver|gzclient|robot_state_publisher|joint_state_publisher|static_transform_publisher|irobot_create_nodes|gazebo_ros|spawn_entity|spawner|controller_manager|rviz2|robot_state|motion_control|ui_mgr|mock_publisher|kidnap_estimator|hazards_vector|ir_intensity_vector|wheel_status|lidar_dock_server|kalman_dock'

listar() {
    # -w evita que el propio script/grep salga en la lista
    ps -eo pid,etime,cmd 2>/dev/null \
        | grep -E "$PATTERN" \
        | grep -v -E "grep|clean_sim" \
        || true
}

contar() { listar | grep -c . || true; }

echo "=== procesos de simulacion encontrados ==="
n=$(contar)
if [ "$n" -eq 0 ]; then
    echo "  ninguno, entorno limpio"
else
    listar | awk '{printf "  %-8s %-10s %s\n", $1, $2, substr($0, index($0,$3), 60)}'
fi

if [ "${1:-}" = "--check" ]; then
    exit 0
fi

if [ "$n" -gt 0 ]; then
    echo
    echo "=== matando $n procesos ==="
    # SIGTERM primero para que cierren ordenadamente
    listar | awk '{print $1}' | while read -r p; do kill "$p" 2>/dev/null; done
    sleep 3
    # y SIGKILL a lo que siga vivo
    listar | awk '{print $1}' | while read -r p; do kill -9 "$p" 2>/dev/null; done
    sleep 2
fi

# El daemon cachea nodos muertos y los sigue listando: reinicio para que
# 'ros2 node list' refleje la realidad.
if command -v ros2 >/dev/null 2>&1; then
    echo "=== reiniciando daemon de ROS ==="
    ros2 daemon stop  >/dev/null 2>&1
    sleep 1
    ros2 daemon start >/dev/null 2>&1
fi

echo
restantes=$(contar)
if [ "$restantes" -eq 0 ]; then
    echo "LIMPIO - listo para lanzar"
else
    echo "AVISO: quedan $restantes procesos:"
    listar | awk '{printf "  %-8s %s\n", $1, substr($0, index($0,$3), 60)}'
fi
