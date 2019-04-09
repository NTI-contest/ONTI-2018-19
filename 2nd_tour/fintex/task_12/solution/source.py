import cognitive_face as CF

KEY = '<your Face API subscription key>'
CF.Key.set(KEY)

# regional Cognitive Service URL
BASE_URL = 'https://westeurope.api.cognitive.microsoft.com/face/v1.0'
CF.BaseUrl.set(BASE_URL)

for i in range(40):
    img_url = './photos/{0}.jpg'.format(i)
    result = CF.face.detect(img_url, False, False, 'headPose')

    roll = result[0]['faceAttributes']['headPose']['roll']
    yaw = result[0]['faceAttributes']['headPose']['yaw']

    #roll left
    if roll > 15: # roll < -15 or yaw > 15 or yaw < -15
        print(i, end=' ')
