#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PointStamped, TransformStamped
import tf2_ros


class TouchToTFNode(Node):
    def __init__(self):
        super().__init__('touch_to_tf_subscriber')

        # Suscriptor al tópico de coordenadas
        self.subscription = self.create_subscription(
            PointStamped,
            'touch_coords',
            self.listener_callback,
            10
        )

        # Broadcaster de TF
        self.tf_broadcaster = tf2_ros.TransformBroadcaster(self)

        self.get_logger().info("Nodo TouchToTF inicializado. Escuchando /touch_coords ...")

    def listener_callback(self, msg: PointStamped):
        # Crear transform
        t = TransformStamped()

        # Header con el tiempo y frame padre
        t.header.stamp = self.get_clock().now().to_msg()
        t.header.frame_id = "touch_point"                # 🔑 Frame de referencia
        t.child_frame_id = "map"         # 🔑 Nombre del frame hijo

        # Traslación: lo que recibimos del touchscreen
        t.transform.translation.x = msg.point.x
        t.transform.translation.y = msg.point.y
        t.transform.translation.z = msg.point.z

        # Rotación identidad (sin rotación)
        t.transform.rotation.x = 0.0
        t.transform.rotation.y = 0.0
        t.transform.rotation.z = 0.0
        t.transform.rotation.w = 1.0

        # Publicar en TF
        self.tf_broadcaster.sendTransform(t)

        self.get_logger().info(
            f"Publicado TF: (x={msg.point.x:.2f}, y={msg.point.y:.2f}, z={msg.point.z:.2f})"
        )


def main(args=None):
    rclpy.init(args=args)
    node = TouchToTFNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
