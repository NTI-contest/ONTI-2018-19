def mag_calibrated(magx,magy,magz):
	magx_cal = 1.06*(magx + -7.49) + -0.01*(magy + -23.59) + 0.07*(magz + -108.24)
	magy_cal = -0.01*(magx + -7.49) + 1.11*(magy + -23.59) + 0.09*(magz + -108.24)
	magz_cal = 0.07*(magx + -7.49) + 0.09*(magy + -23.59) + 1.00*(magz + -108.24)
	return magx_cal, magy_cal, magz_cal