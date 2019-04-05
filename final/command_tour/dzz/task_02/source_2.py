def angle_transformation(alpha, alpha_goal):
	if alpha<=(alpha_goal - 180):
		alpha = alpha + 360
	elif alpha>(alpha_goal +180):
		alpha = alpha - 360
	return alpha