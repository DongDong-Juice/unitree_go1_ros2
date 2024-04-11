import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
import pcl
import pclpy


class PcdToPointCloudNode(Node):
    def __init__(self):
        super().__init__('pcd_to_pointcloud_node')
        self.publisher_ = self.create_publisher(PointCloud2, 'point_cloud', 10)
        self.convert_and_publish()

    def convert_and_publish(self):
        # Load PCD file
        cloud = pcl.PointCloud.PointXYZ()
        if pcl.io.loadPCDFile("/home/dong/map.pcd", cloud) == -1:
            self.get_logger().error('Couldn\'t read PCD file')
            rclpy.shutdown()
        
        # Convert PCL point cloud to ROS 2 point cloud message
        msg = cloud.to_msg()
        msg.header.frame_id = "velodyne"
        # Publish the point cloud message
        self.publisher_.publish(msg)
        self.get_logger().info('Published PointCloud2 message')


def main(args=None):
    rclpy.init(args=args)
    node = PcdToPointCloudNode()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()

