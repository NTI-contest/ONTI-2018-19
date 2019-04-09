from argparse import ArgumentParser
from threading import Thread
from time import sleep

from api import list_people_ids, delete_person, train, create_person, add_face, create_group_if_not_exists
from output_util import print_error
from video_detector import detect_all, detect_middle_faces, detect_roll_faces, detect_yaw_faces, \
    detect_open_mouth_faces, detect_open_eyes_faces

parser = ArgumentParser(prog='Faces management')

parser.add_argument('--simple-add',
                    nargs=1,
                    metavar='VIDEO',
                    help='Adds 5 faces from video')
parser.add_argument('--add',
                    nargs='+',
                    metavar='VIDEO',
                    help='Adds only needed faces from 1-5 videos')
parser.add_argument('--list',
                    action='store_true',
                    help='Prints all registered person ids')
parser.add_argument('--del',
                    nargs=1,
                    metavar='ID',
                    dest='delete',
                    help='Deletes person')
parser.add_argument('--train',
                    action='store_true',
                    help='Starts training')

args = parser.parse_args()

if args.simple_add:
    video = args.simple_add[0]

    faces = detect_all(video)
    if faces is None:
        print_error('Video does not contain any face')

    create_group_if_not_exists()

    print('%d frames extracted' % len(faces))

    person_id = create_person('1')

    print('PersonId: %s' % person_id)
    print('FaceIds')
    print('=======')

    for face in faces:
        print(add_face(face, person_id))

if args.add:
    person_id = ''
    faces = []

    done = 0
    results = [0, 0, 0, 0, 0]
    if len(args.add) > 0:
        def target(video):
            global results, done
            results[0] = detect_middle_faces(video)
            done += 1

        video = args.add[0]

        t = Thread(target=target, args=(video,))
        t.run()

    if len(args.add) > 1:
        def target(video):
            global results, done
            results[1] = detect_roll_faces(video)
            done += 1

        video = args.add[1]

        t = Thread(target=target, args=(video,))
        t.run()

    if len(args.add) > 2:
        def target(video):
            global results, done
            results[2] = detect_yaw_faces(video)
            done += 1

        video = args.add[2]

        t = Thread(target=target, args=(video,))
        t.run()

    if len(args.add) > 3:
        def target(video):
            global results, done
            results[3] = detect_open_mouth_faces(video)
            done += 1

        video = args.add[3]

        t = Thread(target=target, args=(video,))
        t.run()

    if len(args.add) > 4:
        def target(video):
            global results, done
            results[4] = detect_open_eyes_faces(video)
            done += 1

        video = args.add[4]

        t = Thread(target=target, args=(video,))
        t.run()

    while len(args.add) > done:
        sleep(0.5)

    if len(args.add) > 0:
        if results[0] is None:
            print_error('Base video does not follow requirements')

        faces += results[0]

    if len(args.add) > 1:
        if results[1] is None:
            print_error('Roll video does not follow requirements')

        faces += results[1]

    if len(args.add) > 2:
        if results[2] is None:
            print_error('Yaw video does not follow requirements')

        faces += results[2]

    if len(args.add) > 3:
        if results[3] is None:
            print_error('Video to detect open mouth does not follow requirements')

        faces += results[3]

    if len(args.add) > 4:
        if results[4] is None:
            print_error('Video to detect open eyes does not follow requirements')

        faces += results[4]

    create_group_if_not_exists()
    person_id = create_person('1')

    print('%d frames extracted' % len(faces))
    print('PersonId: %s' % person_id)
    print('FaceIds')
    print('=======')

    for face in faces:
        print(add_face(face, person_id))

if args.list:
    list_ids = list_people_ids()

    if len(list_ids) == 0:
        print_error('No persons found')

    print('Persons IDs:')

    for id in list_ids:
        print(id)

if args.delete:
    id = args.delete[0]

    delete_person(id)

    print('Person deleted')

if args.train:
    train()

    print('Training successfully started')
