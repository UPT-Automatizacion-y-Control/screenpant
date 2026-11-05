#!/usr/bin/env python3
import rclpy
import time
from rclpy.node import Node
from geometry_msgs.msg import PointStamped   # Usamos PointStamped en lugar de Point
from evdev import InputDevice, ecodes

class TouchscreenNode(Node):
    def __init__(self):
        super().__init__('touchscreen_node')

        # Publicador: ahora publicamos PointStamped (incluye header con tiempo)
        self.publisher_ = self.create_publisher(PointStamped, 'touch_coords', 10)

        # Ruta del dispositivo táctil
        self.dev = InputDevice('/dev/input/event19')

        # Rango de tu pantalla
        self.Xmin, self.Xmax = 1, 4095
        self.Ymin, self.Ymax = 400, 3680
        self.width_cm, self.height_cm = 20.5, 12.8

        self.current_x = 0.0
        self.current_y = 0.0

        # Crear un timer que ejecute spin_once cada 10 ms (0.01 s)
        self.timer = self.create_timer(0.01, self.spin_once)

        self.get_logger().info("Nodo Touchscreen inicializado. Escuchando eventos...")

    def spin_once(self):
        event = self.dev.read_one()
        if event is None:
            return  # No hay evento en este instante

        if event.type == ecodes.EV_ABS:
            if event.code == ecodes.ABS_X:
                self.current_x = (event.value - self.Xmin) / (self.Xmax - self.Xmin) * self.width_cm
                if self.current_x < 0:
                    self.current_x = 0

            elif event.code == ecodes.ABS_Y:
                self.current_y = (event.value - self.Ymin) / (self.Ymax - self.Ymin) * self.height_cm
                if self.current_y < 0:
                    self.current_y = 0

                # Crear el mensaje con timestamp
                msg = PointStamped()
                msg.header.stamp = self.get_clock().now().to_msg()   # Tiempo ROS2
                msg.header.frame_id = "touchscreen_frame"            # Frame para RViz
                msg.point.x = self.current_x
                msg.point.y = self.current_y
                msg.point.z = 0.0

                # Publicar mensaje
                self.publisher_.publish(msg)
                self.get_logger().info(
                    f"[{msg.header.stamp.sec}.{msg.header.stamp.nanosec:09d}] "
                    f"Touch: X={msg.point.x:.2f} cm, Y={msg.point.y:.2f} cm"
                )

def main(args=None):
    rclpy.init(args=args)
    node = TouchscreenNode()
    try:
        # Ahora ROS se encarga del bucle principal
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
