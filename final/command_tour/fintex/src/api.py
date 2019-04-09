from config import get
import cognitive_face as cf
from detector_util import FileLike, image_to_jpeg
from output_util import handle_error, print_error

KEY = get('faceapi.key')
cf.Key.set(KEY)

BASE_URL = get('faceapi.serviceUrl')
cf.BaseUrl.set(BASE_URL)

CONFIDENCE_THRESHOLD = 0.5

GROUP_ID = get('faceapi.groupId')


def create_group_if_not_exists():
    try:
        cf.person_group.create(GROUP_ID)
    except cf.CognitiveFaceException:
        pass


def list_groups():
    return handle_error(cf.person_group.lists())


def list_people_ids():
    try:
        return list(map(lambda person: person['personId'], cf.person.lists(GROUP_ID)))
    except cf.CognitiveFaceException as err:
        if err.code == 'PersonGroupNotFound':
            print_error('The group does not exist')


def is_group_up_to_date():
    try:
        response1 = cf.person_group.get_status(GROUP_ID)
        response2 = cf.person_group.get(GROUP_ID)

        return response1['status'] == 'succeeded' and response2['userData'] == 'ok'
    except cf.CognitiveFaceException:
        return False


def check_same_person(face_id):
    try:
        response = cf.face.identify([face_id], person_group_id=GROUP_ID, threshold=CONFIDENCE_THRESHOLD)
        candidates = response[0]['candidates']

        return len(candidates) != 0
    except cf.CognitiveFaceException:
        return False


def identify_person_id(faces_ids):
    if not is_group_up_to_date():
        print_error('The service is not ready')

    responses = cf.face.identify(faces_ids, person_group_id=GROUP_ID, threshold=CONFIDENCE_THRESHOLD)
    person_id = ''
    for response in responses:
        candidates = response['candidates']
        if len(candidates) != 1 or person_id not in ['', candidates[0]['personId']]:
            return None
        person_id = candidates[0]['personId']
    return person_id


def identify_person_id_old(image):
    response = cf.face.detect(FileLike(image_to_jpeg(image)), True, False)
    if len(response) != 1:
        print_error('There should be exactly 1 person on image')
    face_id = response[0]['faceId']
    response = cf.face.identify([face_id], person_group_id=GROUP_ID, threshold=CONFIDENCE_THRESHOLD)
    candidates = response[0]['candidates']

    print(candidates)

    if len(candidates) == 0:
        print_error('Cannot identify face')

    return candidates[0]['personId']


# Return face if there is exactly one face on the image
def detect(image):
    faces = cf.face.detect(FileLike(image_to_jpeg(image)), True, True, 'headPose')
    if len(faces) == 1:
        return faces[0]

    return None


def mark_group(status):
    cf.person_group.update(GROUP_ID, user_data=status)


def create_person(name, data=None):
    try:
        response = cf.person.create(GROUP_ID, name, data)
        mark_group('dirty')
        return response['personId']
    except cf.CognitiveFaceException as err:
        if err.code == 'PersonGroupNotFound':
            print_error('The group does not exist')


def delete_person(person_id):
    try:
        cf.person.delete(GROUP_ID, person_id)
        mark_group('dirty')
    except cf.CognitiveFaceException as err:
        if err.code == 'PersonGroupNotFound':
            print_error('The group does not exist')
        if err.code == 'PersonNotFound':
            print_error('The person does not exist')


def add_face(image, person_id):
    return cf.person.add_face(FileLike(image_to_jpeg(image)), GROUP_ID, person_id)['persistedFaceId']


def update_person_data(person_id, name, address):
    cf.person.update(GROUP_ID, person_id, name, address)
    print('Updated person %s data, name %s, address %s' % (person_id, name, address))


def get_person_address(person_id):
    response = cf.person.get(GROUP_ID, person_id)
    return response['userData']


def train():
    try:
        if is_group_up_to_date():
            print_error('Already trained')
        if len(cf.person.lists(GROUP_ID)) == 0:
            print_error('There is nothing to train')
        cf.person_group.train(GROUP_ID)
        mark_group('ok')
    except cf.CognitiveFaceException as err:
        if err.code == 'PersonGroupNotFound':
            print_error('There is nothing to train')


# Returns 0 <= confidence <= 1
def verify_person(person_id, face_id):
    response = cf.face.verify(face_id, person_group_id=GROUP_ID, person_id=person_id)
    return response['confidence']
