"""Guarda contra lanzar dos simulaciones a la vez.

Lanzar sobre una simulacion ya viva falla de forma confusa: el dock responde
"Entity [standard_dock] already exists", el spawner avisa "Controller already
loaded" y acaba muriendo, y los dos gzserver pelean por el mismo puerto. Mas
vale parar antes con un mensaje que diga que hacer.
"""

import subprocess


def abortar_si_ya_hay_simulacion():
    """Lanza RuntimeError si ya hay un gzserver corriendo."""
    try:
        salida = subprocess.run(
            ['pgrep', '-a', 'gzserver'],
            capture_output=True, text=True, timeout=5).stdout.strip()
    except Exception:
        # Si pgrep no esta disponible o falla, no bloqueamos el lanzamiento.
        return

    if not salida:
        return

    procesos = '\n'.join('    ' + linea for linea in salida.splitlines())
    raise RuntimeError(
        '\n'
        '\n  YA HAY UNA SIMULACION CORRIENDO\n'
        '\n'
        f'{procesos}\n'
        '\n  Lanzar otra encima falla: el dock ya existe y el controller_manager\n'
        '  esta ocupado. Limpia primero:\n'
        '\n'
        '    ros2 run create3_dock_challenge clean_sim.sh\n'
    )
