def needMove(self):
    dist = math.sqrt(math.pow(self.pose.x-self.last_pose.x,2)+math.pow(self.pose.y-self.last_pose.y,2))
    rospy.logdebug("Dist :%s", dist)
    if dist < 3:
        return True
    else :
        return False