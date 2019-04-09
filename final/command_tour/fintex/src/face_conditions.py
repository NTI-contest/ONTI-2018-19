import cv2

from detector_util import landmarks, left_eye_open, right_eye_open, mouth_open

DEFAULT_ANGLE_DELTA = 3


class FaceConditions:
    def __init__(self, label, yaw=None, roll=None, delta=DEFAULT_ANGLE_DELTA,
                 left_eye=None, right_eye=None, mouth=None):
        self.label = label
        self.completed = False

        self.yaw = yaw
        self.yaw_delta = delta
        self.roll = roll
        self.roll_delta = delta
        self.left_eye = left_eye
        self.right_eye = right_eye
        self.mouth = mouth

    def check_face(self, image, face_api_response=None):
        if self.completed:
            return

        if self.yaw is not None and self.roll is not None and face_api_response is not None:
            yaw_value = face_api_response['faceAttributes']['headPose']['yaw']
            roll_value = face_api_response['faceAttributes']['headPose']['roll']

            if self.yaw is not None and (yaw_value < self.yaw - self.yaw_delta or yaw_value > self.yaw + self.yaw_delta):
                return
            if self.roll is not None and (
                    roll_value < self.roll - self.roll_delta or roll_value > self.roll + self.roll_delta):
                return

        points = landmarks(image)
        if points is None:
            return False

        if self.left_eye is not None and self.left_eye != left_eye_open(points):
            return
        if self.right_eye is not None and self.right_eye != right_eye_open(points):
            return
        if self.mouth is not None and self.mouth != mouth_open(points):
            return

        self.completed = True

        return True
