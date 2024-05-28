#!/usr/bin/env python
import rospy
from std_msgs.msg import String
# Brings in the SimpleActionClient
import actionlib
# Brings in the .action file and messages used by the move base action
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def movebase_client(data):

   # Create an action client called "move_base" with action definition file "MoveBaseAction"
    a=data.data
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    
   # Waits until the action server has started up and started listening for goals.
    client.wait_for_server()

   # Creates a new goal with the MoveBaseGoal constructor
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    print(a)
    if(a == "0"):
   # Move 0.5 meters forward along the x axis of the "map" coordinate frame 
        goal.target_pose.pose.position.x = 5.0
        goal.target_pose.pose.position.y= -2.82
   # No rotation of the mobile base frame w.r.t. map frame
        goal.target_pose.pose.orientation.w = 0.5
    elif(a == "1"):
   # Move 0.5 meters forward along the x axis of the "map" coordinate frame 
        goal.target_pose.pose.position.x = 0.8
        goal.target_pose.pose.position.y= 4.0
   # No rotation of the mobile base frame w.r.t. map frame
        goal.target_pose.pose.orientation.w = 0.5
    elif(a == "2"):
   # Move 0.5 meters forward along the x axis of the "map" coordinate frame 
        goal.target_pose.pose.position.x = -2.4
        goal.target_pose.pose.position.y= -2.7
   # No rotation of the mobile base frame w.r.t. map frame
        goal.target_pose.pose.orientation.w = 0.5
    else:
   # Move 0.5 meters forward along the x axis of the "map" coordinate frame 
        goal.target_pose.pose.position.x = -7.5   
        goal.target_pose.pose.position.y= 5.0
   # No rotation of the mobile base frame w.r.t. map frame
        goal.target_pose.pose.orientation.w = 0.5
   # Sends the goal to the action server.
    client.send_goal(goal)
   # Waits for the server to finish performing the action.
    wait = client.wait_for_result()
   # If the result doesn't arrive, assume the Server is not available
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    #else:
    # Result of executing the action
        #return client.get_result()   

# If the python node is executed as main process (sourced directly)
if __name__ == '__main__':
    rospy.init_node('movebase_client_py')
    while not rospy.is_shutdown():
        try:
       # Initializes a rospy node to let the SimpleActionClient publish and subscribe
            rospy.Subscriber('biogoal',String,movebase_client)
        except rospy.ROSInterruptException:
            rospy.loginfo("Navigation test finished.")
