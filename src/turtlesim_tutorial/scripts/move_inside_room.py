#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import sys

robot_x = 0
robot_y = 0

def pose_callback(pose): # pose te x, y, z
    global robot_x, robot_y
    robot_x = pose.x # posicio en x
    robot_y = pose.y # posicio en y
    rospy.loginfo("Robot X = %f\t Robot Y = %f\n",pose.x, pose.y)

def move_turtle(lin_vel,ang_vel,distance):
    global robot_x, robot_y
    pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10) # defineix publisehr
    rospy.Subscriber('/turtle1/pose',Pose, pose_callback) # Subcriu a turtel1/pose al missatges de tipus pose
    # al rebre el missatge executa pose_callback
    rate = rospy.Rate(10) # 10hz
    vel = Twist() # Publica el twist
    while not rospy.is_shutdown(): # mentres no es pari
        vel.linear.x = lin_vel
        vel.linear.y = 0
        vel.linear.z = 0
        vel.angular.x = 0
        vel.angular.y = 0
        vel.angular.z = ang_vel

        if (robot_x != 0 and robot_y != 0):
            if(robot_x >= 8 or robot_y >= 8 or robot_x <= 3 or robot_y <= 3): # comprova la posicio amb les distancies per no chocar
                print(robot_x, robot_y)
                rospy.loginfo("Robot hits a wall")
                rospy.logwarn("Stopping robot")
                break
            pub.publish(vel)
            rate.sleep()

if __name__ == '__main__':
    try:
        rospy.init_node('move_turtle', anonymous=False)#Has to be called here at the begining!
        v= rospy.get_param("~v")
        w= rospy.get_param("~w")
        d= rospy.get_param("~d")
        move_turtle(v,w,d)
    except rospy.ROSInterruptException:
        pass