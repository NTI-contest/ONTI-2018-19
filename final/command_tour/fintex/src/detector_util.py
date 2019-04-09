import cv2
import os
import dlib

from output_util import print_error

PREDICTOR_PATH = '/opt/shape_predictor_68_face_landmarks.dat' if os.path.exists(
    '/opt/shape_predictor_68_face_landmarks.dat') else './shape_predictor_68_face_landmarks.dat'
EYE_THRESHOLD = 0.22
MOUTH_THRESHOLD = 0.3

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(PREDICTOR_PATH)


class FileLike:
    def __init__(self, image):
        self.image = image

    def read(self):
        return self.image


def shape_to_list(shape):
    coords = [None] * 68

    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)

    return coords


def right_eye_open(points):
    eye = points[36:42]
    return aspect_ratio(eye) > EYE_THRESHOLD


def left_eye_open(points):
    eye = points[42:48]
    return aspect_ratio(eye) > EYE_THRESHOLD


def mouth_open(points):
    mouth = [points[60], points[61], points[63], points[64], points[65], points[67]]
    return aspect_ratio(mouth) > MOUTH_THRESHOLD


def aspect_ratio(eye):
    return (dist(eye[1], eye[5]) + dist(eye[2], eye[4])) / (2 * dist(eye[0], eye[3]))


def dist(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def landmarks(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    dets, scores, idx = detector.run(gray, 0, -1)

    if len(dets) == 0:
        return None

    return shape_to_list(predictor(image, dets[0]))


def image_to_jpeg(image):
    status, encoded_image = cv2.imencode('.jpeg', image)
    if not status:
        print_error('Failed to encode frame into jpeg')
    return encoded_image.tostring()

