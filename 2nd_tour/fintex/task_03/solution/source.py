import numpy as np
from json import loads

ideal_landmarks = np.array([
  [252, 520, 782],
  [331, 634, 321],
  [1, 1, 1]
])

actual_landmarks = loads(input())[0]['faceLandmarks']

eye_left_outer = actual_landmarks.pop("eyeLeftOuter")
nose_tip = actual_landmarks.pop("noseTip")
eye_right_outer = actual_landmarks.pop("eyeRightOuter")

other_landmark = actual_landmarks[list(actual_landmarks.keys())[0]]
other_landmark = np.array([
    [other_landmark['x']],
    [other_landmark['y']],
    [1]
])

actual_landmarks = np.array([
  [eye_left_outer['x'], nose_tip['x'], eye_right_outer['x']],
  [eye_left_outer['y'], nose_tip['y'], eye_right_outer['y']],
  [1, 1, 1]
])

t = np.matmul(ideal_landmarks, np.linalg.inv(actual_landmarks))

result_landmark = np.matmul(t, other_landmark)
x, y = result_landmark[0][0], result_landmark[1][0]

print(int(x), int(y))