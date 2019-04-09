import dlib
import imutils as imutils

EYE_THRESHOLD = 0.2
MOUTH_THRESHOLD = 0.3

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


predictor_path = '<dlib predictor_68 path>'
faces_folder_path = '<faces folder path>'

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)

for i in range(100):
    # load current image
    img_url = faces_folder_path + '/{0}.jpg'.format(i)
    img = dlib.load_grayscale_image(img_url)

    # do some resizing operations
    if img.shape[1] < 300:
        img = imutils.resize(img, width=img.shape[1] * 2)
    elif img.shape[1] < 450:
        img = imutils.resize(img, width=450)
    else:
        img = imutils.resize(img, width=900)

    # detect faces
    dets, scores, idx = detector.run(img, 0, -1)

    # get list of points
    points = shape_to_list(predictor(img, dets[0]))

    if not left_eye_open(points) and right_eye_open(points):
        print(i, end=' ')
