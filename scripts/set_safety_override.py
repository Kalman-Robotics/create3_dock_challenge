#!/usr/bin/env python3
"""Pone safety_override en motion_control al arrancar la simulacion.

Por defecto el Create 3 arranca con safety_override='none', que NO permite
retroceder. Este nodo espera a que motion_control levante y le aplica el valor
pedido, para no tener que hacerlo a mano en cada lanzamiento.

Valores (del propio parametro del nodo):
  none         por defecto, sin retroceso
  backup_only  permite retroceder, sin seguridad de cliff hacia atras
  full         ademas desactiva cliffs por completo y sube la velocidad
               maxima a 0.46 m/s (frente a 0.306 en los otros modos)

Nota: kalman_dock aplica 'full' por su cuenta antes del approach, asi que en
ese flujo esto es redundante. Sirve para mover el robot con teleop o /cmd_vel
fuera del action.
"""

import sys

import rclpy
from rcl_interfaces.msg import Parameter, ParameterType, ParameterValue
from rcl_interfaces.srv import SetParameters
from rclpy.node import Node


class SetSafetyOverride(Node):

    def __init__(self):
        super().__init__('set_safety_override')
        self.declare_parameter('value', 'full')
        self.declare_parameter('target_node', '/motion_control')
        self.declare_parameter('timeout', 60.0)

    def run(self):
        value = self.get_parameter('value').value
        target = self.get_parameter('target_node').value
        timeout = float(self.get_parameter('timeout').value)

        cli = self.create_client(SetParameters, f'{target}/set_parameters')
        self.get_logger().info(f'esperando a {target}...')
        if not cli.wait_for_service(timeout_sec=timeout):
            self.get_logger().warn(
                f'{target} no aparecio en {timeout:.0f}s — safety_override sin aplicar')
            return 1

        req = SetParameters.Request()
        p = Parameter()
        p.name = 'safety_override'
        p.value = ParameterValue(type=ParameterType.PARAMETER_STRING,
                                 string_value=value)
        req.parameters = [p]

        future = cli.call_async(req)
        rclpy.spin_until_future_complete(self, future, timeout_sec=10.0)
        res = future.result()

        if res is None:
            self.get_logger().warn('sin respuesta al set_parameters')
            return 1
        if res.results and not res.results[0].successful:
            self.get_logger().warn(
                f'rechazado: {res.results[0].reason}')
            return 1

        self.get_logger().info(f'safety_override = {value}  (retroceso permitido)')
        return 0


def main():
    rclpy.init()
    node = SetSafetyOverride()
    try:
        code = node.run()
    finally:
        node.destroy_node()
        rclpy.shutdown()
    sys.exit(code)


if __name__ == '__main__':
    main()
