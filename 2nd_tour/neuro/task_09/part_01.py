import os
import cv2
import dlib

class Solver:
    def __init__(self, path_to_dir):
        self.predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
        for file in os.listdir(path_to_dir):
            file_name = os.path.join(path_to_dir,file)
            image = cv2.imread(file_name)
          
    def predict(self, path_to_file):
        return False