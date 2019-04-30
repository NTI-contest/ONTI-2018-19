function sign(num) { return num >= 0 ? 1 : -1}
function motors(mL, mR){ mR = mR || mL; brick.motor('M4').setPower(mL); brick.motor('M3').setPower(mR) }

function move(cm, turn){
	var L = (cm / (Math.PI * robot.D)) * robot.cpr
	L += encL()
	var sgn = sign(cm)
	motors(100 * sgn)
	if (sgn == 1){
		while (encL() <= L) script.wait(10)
	} else {
		while (encL() >= L) script.wait(10)
	}
	
	if (turn == undefined){
		step += 1
		switch (robot.a){
			case 0: robot.x--; break;
			case 1: robot.y++; break;
			case 2:	robot.x++; break;
			case 3:	robot.y--; break;
		}
	}
	motors(0)
}

robot = {
	D: 5.6,
	track: 17.5,
	x: 0,
	y: 0,
	a: 1,
	cpr: 360
}

cellLength = 17.5 * 4

sensF = brick.sensor('A1').read
sensL = brick.sensor('A2').read
encL  = brick.encoder('E4').read
encR  = brick.encoder('E3').read

wait = script.wait

steps = script.readAll('input.txt')
step = 0

function turn (angle){
	var sgn = sign(angle)
	move(17.5 * 0.5, true)
	var lAngle = ((robot.track * angle) / (robot.D * 360)) * robot.cpr
	lAngle += encL()
	
	motors(50 * sgn, -50 * sgn)
	
	if (sgn == 1){
		while (encL() <= lAngle) wait(10)
		robot.a++
	} else {
		while (encL() >= lAngle) wait(10)
		robot.a--
	}
	
	if (robot.a > 3) robot.a = 0
	if (robot.a < 0) robot.a = 3
	
	motors(0)
	move(17.5 * -0.5, true)
}


while (true){
	if (sensL() > cellLength){
		turn(-90)
		move(cellLength)
	} else {
		if (sensF() > cellLength)
			move(cellLength)
		else
			turn (90)
	}
	script.wait(100)
	if (step == steps)
		break
}
motors(0)

// test
a = 1

out = '(' + robot.x + ',' + robot.y + ')'
brick.display().addLabel(out, 1, 1)
brick.display().redraw()