import rospy, math

from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

class Turtle(object):

    def __init__(self):
        self.pub = rospy.Publisher('/turtle1/cmd_vel', Twist, queue_size=10)
        self.last_pose = Pose()
        self.turtle_state = 'START'
        self.pose = Pose()
        self.angles = 0

    def move(self):

        if self.turtle_state == 'FORWARD':
            if(self.needMove()):
                self.turtleForward()
            else :
                self.turtle_state = 'TURN'
                self.last_pose = self.pose
                self.turtleStop()
        
        if self.turtle_state == 'TURN':
            if(self.needRotate()):
                self.turtleRotate()
            else :
                self.turtle_state = 'FORWARD'
                self.last_pose = self.pose
                rospy.loginfo("Point x:%s,y:%s", self.pose.x, self.pose.y)
                self.turtleStop()
                self.angles +=1

    def turtleForward(self):
        pub_twist = Twist()
        pub_twist.linear.x = 0.5
        self.pub.publish(pub_twist)

    def turtleRotate(self):
        pub_twist = Twist()
        pub_twist.angular.z = 0.5
        self.pub.publish(pub_twist)

    def turtleStop(self):
        pub_twist = Twist()
        self.pub.publish(pub_twist)
  

    def needMove(self):

        dist = math.sqrt(math.pow(self.pose.x-self.last_pose.x,2)+
            math.pow(self.pose.y-self.last_pose.y,2))
        rospy.logdebug("Dist :%s", dist)
        if dist < 3:
            return True
        else :
            return False

    def needRotate(self):
        deg = self.pose.theta - self.last_pose.theta
        rospy.logdebug("Degrees :%s", deg)

        if (deg >= 0 and deg < math.pi/2):
            return True
        else :     
            return False        


def pose_callback(pose, turtle):

    if turtle.turtle_state == 'START':
        rospy.loginfo("Start x:%s,y:%s", pose.x, pose.y)
        turtle.turtle_state = 'FORWARD'
        turtle.last_pose = pose

    turtle.pose = pose
    turtle.move()

    if (turtle.angles == 4): rospy.signal_shutdown('STOP') # sys.exit()    

if __name__ == '__main__':
    try:
        turtle = Turtle()
        rospy.init_node('draw_square')
        rospy.loginfo("Start Node")
        rospy.Subscriber("turtle1/pose", Pose, pose_callback, turtle)
        rospy.spin()

    except KeyboardInterrupt, e:
        pass
    print "exiting"
