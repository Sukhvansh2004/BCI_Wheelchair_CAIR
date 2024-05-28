import socket
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import PoseStamped

def create_pose_stamped(position, orientation):
    # Create a PoseStamped object
    pose_stamped = PoseStamped()

    # Fill in the header information (only frame_id, ignore seq)
    pose_stamped.header.frame_id = "map"
    
    # Fill in the pose position
    pose_stamped.pose.position.x = position['x']
    pose_stamped.pose.position.y = position['y']
    pose_stamped.pose.position.z = position['z']

    # Fill in the pose orientation
    pose_stamped.pose.orientation.x = orientation['x']
    pose_stamped.pose.orientation.y = orientation['y']
    pose_stamped.pose.orientation.z = orientation['z']
    pose_stamped.pose.orientation.w = orientation['w']

    return pose_stamped

# Initialize the ROS node (if needed)
# rospy.init_node('pose_stamped_publisher')

# Create PoseStamped messages and store them in a dictionary
pose_dict = {
    'A': create_pose_stamped(
        position={'x': 0.6528778076171875, 'y': -9.443294525146484, 'z': 0.0},
        orientation={'x': 0.0, 'y': 0.0, 'z': -0.10462528907649193, 'w': 0.9945117138001244}
    ),
    'B': create_pose_stamped(
        position={'x': 3.485126495361328, 'y': -10.366340637207031, 'z': 0.0},
        orientation={'x': 0.0, 'y': 0.0, 'z': -0.07834007727801531, 'w': 0.996926693539738}
    ),
    'C': create_pose_stamped(
        position={'x': 6.407230377197266, 'y': -10.769105911254883, 'z': 0.0},
        orientation={'x': 0.0, 'y': 0.0, 'z': 0.1302762801218584, 'w': 0.9914777308833573}
    ),
    'D': create_pose_stamped(
        position={'x': 8.975214004516602, 'y': -11.080821990966797, 'z': 0.0},
        orientation={'x': 0.0, 'y': 0.0, 'z': 0.04022247167390605, 'w': 0.999190748942584}
    ),
    'E': create_pose_stamped(
        position={'x': -1.9735279083251953, 'y': -10.615152359008789, 'z': 0.0},
        orientation={'x': 0.0, 'y': 0.0, 'z': 0.008742422256530357, 'w': 0.9999617842963242}
    )
}

def tcp_server():
    # Initialize ROS node
    rospy.init_node('tcp_to_ros_node', anonymous=True)
    pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)

    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the address and port
    server_address = ('172.18.43.214', 8000)  # Use an appropriate IP address and port
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen(1)

    rospy.loginfo("TCP server listening on %s:%s", server_address[0], server_address[1])

    while not rospy.is_shutdown():
        # Wait for a connection
        connection, client_address = server_socket.accept()

        try:
            rospy.loginfo('Connection from %s', client_address)

            # Receive the data
            data = connection.recv(1024)
            rospy.loginfo('Received data: %s', data.decode())


            # Publish the data to the ROS topic
            pub.publish(pose_dict[data.decode()])

        except Exception as e:
            rospy.logerr('Error: %s', e)

        finally:
            # Clean up the connection
            connection.close()

if __name__ == '__main__':
    try:
        tcp_server()
    except rospy.ROSInterruptException:
        pass
