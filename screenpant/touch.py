#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
from evdev import InputDevice, categorize, ecodes

class TouchscreenNode(Node):
    def __init__(self):
        super().__init__('touchscreen_node')

        # Publicador: publicamos coordenadas X, Y, Z (Z fijo = 0)
        self.publisher_ = self.create_publisher(Point, 'touch_coords', 10)

        # Ruta del dispositivo táctil (ajústala si no es event14)
        self.dev = InputDevice('/dev/input/event14')

        # Rango de tu pantalla
        self.Xmin, self.Xmax = 1, 4095
        self.Ymin, self.Ymax = 400, 3680
        self.width_cm, self.height_cm = 20.5, 12.8

        self.current_x = 0.0
        self.current_y = 0.0

        self.get_logger().info("Nodo Touchscreen inicializado. Escuchando eventos...")
        
    def spin_once(self):
        event = self.dev.read_one()
        if event is None:
            return  # No hay evento en este instante

        if event.type == ecodes.EV_ABS:
            if event.code == ecodes.ABS_X:
                self.current_x = (event.value - self.Xmin) / (self.Xmax - self.Xmin) * self.width_cm
                if self.current_x < 0:
                    self.current_x = 0.0

            elif event.code == ecodes.ABS_Y:
                self.current_y = (event.value - self.Ymin) / (self.Ymax - self.Ymin) * self.height_cm
                if self.current_y < 0:
                    self.current_y = 0.0

                msg = Point()
                msg.x = self.current_x
                msg.y = self.current_y
                msg.z = 0.0
                self.publisher_.publish(msg)
                self.get_logger().info(f"Touch: X={msg.x:.2f} cm, Y={msg.y:.2f} cm")

def main(args=None):
    rclpy.init(args=args)
    node = TouchscreenNode()
    try:
        while rclpy.ok():
            node.spin_once()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
