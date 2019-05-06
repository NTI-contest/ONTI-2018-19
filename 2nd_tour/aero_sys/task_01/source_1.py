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
            self.angels +=1