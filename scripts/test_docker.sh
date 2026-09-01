#!/usr/bin/env bash
# Valida la instalacion en un contenedor limpio de ROS 2 Humble.
#
# Reproduce exactamente lo que hara un participante que sigue el README: parte
# de una imagen sin nada, deja que rosdep resuelva las dependencias del
# package.xml y comprueba que el paquete compila y que el escenario levanta.
#
#   uso:  ./test_docker.sh              usa el repo local (copia src/)
#         ./test_docker.sh --from-git   clona desde GitHub, como el alumno
#
# Requiere Docker. En WSL hay que activar la integracion:
#   Docker Desktop > Settings > Resources > WSL Integration > tu distro

set -euo pipefail

IMAGEN="ros:humble-ros-base"
PKG="create3_dock_challenge"
REPO="https://github.com/Kalman-Robotics/create3_dock_challenge.git"
DESDE_GIT="${1:-}"

if ! command -v docker >/dev/null 2>&1; then
    echo "docker no esta disponible en esta shell."
    echo "En WSL: Docker Desktop > Settings > Resources > WSL Integration"
    exit 1
fi

# Raiz del paquete, subiendo desde scripts/
PKG_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "=== Validando en $IMAGEN ==="
echo

# El contenedor corre headless: no hay X, asi que la simulacion se lanza con
# use_gazebo_gui:=false y use_rviz:=false. Lo que se valida es que rosdep
# resuelva, que compile y que los topicos aparezcan.
GUION='
set -e
echo "--- 1. rosdep update ---"
apt-get update -qq
rosdep update --rosdistro humble >/dev/null 2>&1

echo "--- 2. rosdep install (esto instala Gazebo y el Create 3) ---"
cd /ws
rosdep install --from-paths src --ignore-src -r -y

echo "--- 3. colcon build ---"
source /opt/ros/humble/setup.bash
colcon build --symlink-install --packages-select PKG_NAME

echo "--- 4. lanzar headless y comprobar topicos ---"
source install/setup.bash
ros2 launch PKG_NAME challenge_world.launch.py \
     use_gazebo_gui:=false use_rviz:=false > /tmp/sim.log 2>&1 &
LANZADO=$!

OK_SCAN=0; OK_DOCK=0
for i in $(seq 1 40); do
    sleep 3
    if [ $OK_SCAN -eq 0 ] && ros2 topic list 2>/dev/null | grep -qx "/scan"; then
        echo "    /scan publicando"; OK_SCAN=1
    fi
    if [ $OK_DOCK -eq 0 ] && ros2 topic list 2>/dev/null | grep -qx "/dock_status"; then
        echo "    /dock_status publicando"; OK_DOCK=1
    fi
    [ $OK_SCAN -eq 1 ] && [ $OK_DOCK -eq 1 ] && break
done

kill $LANZADO 2>/dev/null || true

echo
if [ $OK_SCAN -eq 1 ] && [ $OK_DOCK -eq 1 ]; then
    echo "RESULTADO: OK - instalacion limpia funcional"
    exit 0
else
    echo "RESULTADO: FALLO - scan=$OK_SCAN dock_status=$OK_DOCK"
    echo "--- ultimas lineas del log ---"
    tail -30 /tmp/sim.log
    exit 1
fi
'
GUION="${GUION//PKG_NAME/$PKG}"

if [ "$DESDE_GIT" = "--from-git" ]; then
    echo "Modo: clonando desde GitHub (como lo hara el participante)"
    docker run --rm "$IMAGEN" bash -c "
        apt-get update -qq && apt-get install -y -qq git python3-colcon-common-extensions >/dev/null
        mkdir -p /ws/src && cd /ws/src && git clone -q $REPO
        $GUION"
else
    echo "Modo: usando el repo local"
    docker run --rm \
        -v "$PKG_DIR":/ws/src/"$PKG":ro \
        "$IMAGEN" bash -c "
        apt-get install -y -qq python3-colcon-common-extensions >/dev/null 2>&1 || true
        $GUION"
fi
