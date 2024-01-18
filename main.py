import cv2
import numpy as np
import dlib
from imutils import face_utils
import kivy
from kivy.app import App
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import pygame

pygame.mixer.init()

class TiredDetectionApp(App):
    def build(self):
        self.img1 = Image()
        Clock.schedule_interval(self.update, 1.0 / 30.0)  # 30 FPS

        # Initializing the camera and taking the instance
        self.cap = cv2.VideoCapture(0)

        # Initializing the face detector and landmark detector
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor("assets\shape_predictor_68_face_landmarks.dat")

        # Initializing status variables
        self.sleep = 0
        self.drowsy = 0
        self.active = 0
        self.status = ""
        self.color = (0, 0, 0)

        return self.img1

    def update(self, dt):
        _, frame = self.cap.read()
        gray = cv2.flip(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.flip(frame, 1)
        faces = self.detector(gray)
        face_frame = frame.copy()

        for face in faces:
            x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
            face_frame = frame.copy()
            cv2.rectangle(face_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            landmarks = self.predictor(gray, face)
            landmarks = face_utils.shape_to_np(landmarks)

            left_blink = self.blinked(landmarks[36], landmarks[37],
                                      landmarks[38], landmarks[41], landmarks[40], landmarks[39])
            right_blink = self.blinked(landmarks[42], landmarks[43],
                                       landmarks[44], landmarks[47], landmarks[46], landmarks[45])

            if left_blink == 0 or right_blink == 0:
                self.sleep += 1
                self.drowsy = 0
                self.active = 0
                if self.sleep > 6:
                    self.status = "SLEEP !!!"
                    self.color = (255, 0, 0)
                    pygame.mixer.music.load("assets\warning.wav")
                    pygame.mixer.music.play()

            elif left_blink == 1 or right_blink == 1:
                self.sleep = 0
                self.active = 0
                self.drowsy += 1
                if self.drowsy > 6:
                    self.status = "Tired Alert !"
                    self.color = (0, 0, 255)

            else:
                self.drowsy = 0
                self.sleep = 0
                self.active += 1
                if self.active > 6:
                    self.status = "Active :)"
                    self.color = (0, 255, 0)
                    pygame.mixer.music.pause()

            cv2.putText(frame, self.status, (370, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.2, self.color, 3)

            for n in range(0, 68):
                (x, y) = landmarks[n]
                cv2.circle(face_frame, (x, y), 1, (255, 255, 255), -1)

        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        self.img1.texture = texture1

    def on_stop(self):
        self.cap.release()

    def compute(self, ptA, ptB):
        dist = np.linalg.norm(ptA - ptB)
        return dist

    def blinked(self, a, b, c, d, e, f):
        up = self.compute(b, d) + self.compute(c, e)
        down = self.compute(a, f)
        ratio = up / (2.0 * down)

        if ratio > 0.25:
            return 2
        elif 0.21 < ratio <= 0.25:
            return 1
        else:
            return 0

if __name__ == '__main__':
    TiredDetectionApp().run()
