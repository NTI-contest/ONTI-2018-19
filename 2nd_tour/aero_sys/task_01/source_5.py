def needRotate(self):
    deg = self.pose.theta - self.last_pose.theta
    rospy.logdebug("Degrees :%s", deg)

    if (deg >= 0 and deg < math.pi/2):
        return True
    else :     
        return False