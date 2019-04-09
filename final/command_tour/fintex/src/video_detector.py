import cv2
import imutils

from config import get, set, clear
from api import detect, verify_person, check_same_person, identify_person_id
from face_conditions import FaceConditions
from output_util import print_error

WIDTH = 1000
CONDITIONS_TO_VERIFY = 3

def detect_all(video):
    faces_images = []

    cap = cv2.VideoCapture(video)
    success, frame = cap.read()
    count = 0

    while success:
        if count % 5 == 0:
            frame = imutils.resize(frame, width=WIDTH)

            face_api_response = detect(frame)

            if face_api_response is not None:
                if check_same_person(face_api_response['faceId']):
                    print_error('The same person already exists')

                faces_images.append(frame)

                if len(faces_images) == 5:
                    return faces_images

        count += 1
        success, frame = cap.read()

    return None


def detect_by_conditions(video, conditions, face_api=True):
    cur = 0
    faces_images = []

    cap = cv2.VideoCapture(video)
    success, frame = cap.read()
    count = 0

    while success:
        if count % 3 == 0:
            frame = imutils.resize(frame, width=WIDTH)

            face_api_response = detect(frame) if face_api else 0
            if face_api_response is not None and conditions[cur].check_face(frame, face_api_response):
                if face_api_response != 0 and check_same_person(face_api_response['faceId']):
                    print_error('The same person already exists')

                faces_images.append(frame)
                cur += 1

                if cur == len(conditions):
                    return faces_images

        count += 1
        success, frame = cap.read()

    return None


def detect_by_conditions_in_any_order(video, conditions, face_api=True):
    completed = 0
    faces_images = []

    cap = cv2.VideoCapture(video)
    success, frame = cap.read()

    while success:
        frame = imutils.resize(frame, width=WIDTH)
        face_api_response = detect(frame) if face_api else 0
        if face_api_response is not None:
            for condition in conditions:
                if condition.check_face(frame, face_api_response):
                    faces_images.append(frame)
                    completed += 1
                    break

            if completed == len(conditions):
                return faces_images

        success, frame = cap.read()

    return None


def detect_middle_faces(video):
    return detect_by_conditions(video, [
        FaceConditions('middle_face1', yaw=0, roll=0, delta=5),
        FaceConditions('middle_face2', yaw=0, roll=0, delta=5),
        FaceConditions('middle_face3', yaw=0, roll=0, delta=5),
        FaceConditions('middle_face4', yaw=0, roll=0, delta=5),
        FaceConditions('middle_face5', yaw=0, roll=0, delta=5)
    ])


def detect_roll_faces(video):
    return detect_by_conditions(video, [
        FaceConditions('roll_left_30', roll=30),
        FaceConditions('roll_left_15', roll=15),
        FaceConditions('roll_middle_0', roll=0),
        FaceConditions('roll_right_15', roll=-15),
        FaceConditions('roll_right_30', roll=-30)
    ])


def detect_yaw_faces(video):
    return detect_by_conditions(video, [
        FaceConditions('yaw_left_20', yaw=20),
        FaceConditions('yaw_left_10', yaw=10),
        FaceConditions('yaw_middle', yaw=0),
        FaceConditions('yaw_right_10', yaw=-10),
        FaceConditions('yaw_right_20', yaw=-20)
    ])


def detect_open_mouth_faces(video):
    return detect_by_conditions(video, [
        FaceConditions('open_mouth', mouth=True)
    ], face_api=False)


def detect_open_eyes_faces(video):
    return detect_by_conditions_in_any_order(video, [
        FaceConditions('closed_left_eye', left_eye=False, right_eye=True),
        FaceConditions('closed_right_eye', left_eye=True, right_eye=False),
    ], face_api=False)


def simple_identify(video):
    cap = cv2.VideoCapture(video)
    success, frame = cap.read()
    count = 0

    faces_ids = []

    while success:
        if count % 5 == 0:
            frame = imutils.resize(frame, width=WIDTH)

            face_api_response = detect(frame)

            if face_api_response is not None:
                faces_ids += [face_api_response['faceId']]

                if len(faces_ids) == 5:
                    break

        count += 1
        success, frame = cap.read()

    if len(faces_ids) < 5:
        print_error('The video does not follow requirements')

    person_id = identify_person_id(faces_ids)

    if person_id is None:
        print_error('The person was not found')

    return person_id


def action_to_face_condition(action):
    return action


def identify(video, actions):
    cap = cv2.VideoCapture(video)
    success, frame = cap.read()

    actions = list(map(action_to_face_condition, actions))

    count = 0
    cur = 0

    faces_ids = []

    while success:
        if count % 5 == 0:
            frame = imutils.resize(frame, width=WIDTH)

            face_api_response = detect(frame)

            if face_api_response is not None and actions[cur].check(frame, face_api_response):
                faces_ids += [face_api_response['faceId']]

                cur += 1
                if cur == len(actions):
                    break

        count += 1
        success, frame = cap.read()

    if cur < len(actions):
        print_error('The video does not follow requirements')

    person_id = identify_person_id(faces_ids)

    if person_id is None:
        print_error('The person was not found')

    return person_id
