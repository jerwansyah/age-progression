import dlib
import cv2


class FeatureDetection:
    def __init__(self, predictor_path, detector_path):
        self.predictor = dlib.shape_predictor('data/shape_predictor_68_face_landmarks.dat')
        self.detector = dlib.get_frontal_face_detector()

    def detect(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.detector(gray)
        for face in faces:
            shape = self.predictor(gray, face)
            return shape

    def save_points(self, shape, path, filename):
        with open(path, 'w') as file:
            file.write(filename)
            for i in range(0, 68):
                x = shape.part(i).x
                y = shape.part(i).y
                file.write(' ' + str(x) + ' ' + str(y))
            file.write('\n')


if __name__ == '__main__':
    DEBUG = False

    detector = FeatureDetection('shape_predictor_68_face_landmarks.dat', 'mmod_human_face_detector.dat')
    image = cv2.imread('data/img_01.jpg')
    # image = cv2.imread('data/UTKFace/12_1_0_20170109204113685.jpg.chip.jpg')
    shape = detector.detect(image)
    detector.save_points(shape, 'data/test/points_img_01.txt', 'img_01')

    for i in range(0, 68):
        x = shape.part(i).x
        y = shape.part(i).y
        cv2.circle(image, (x, y), 2, (0, 255, 0), -1)

    if DEBUG:
        cv2.imshow('image', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()