def turtleForward(self):
    pub_twist = Twist()
    pub_twist.linear.x = 0.5
    self.pub.publish(pub_twist)