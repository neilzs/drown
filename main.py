# coding:utf-8
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import cv2


class KivyCamera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        self.capture = capture
        self.fps = fps
        self.is_capturing = False

    def start_capture(self):
        Clock.schedule_interval(self.update, 1.0 / self.fps)
        self.is_capturing = True

    def stop_capture(self):
        Clock.unschedule(self.update)
        self.is_capturing = False

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture


class CameraApp(App):
    def build(self):
        self.capture = cv2.VideoCapture(0)
        self.my_camera = KivyCamera(capture=self.capture, fps=30)

        # Add a start button
        self.start_button = Button(text='Start Camera', on_press=self.start_camera)

        # Create a layout to hold the button and camera preview
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.start_button)
        layout.add_widget(self.my_camera)

        return layout

    def on_stop(self):
        # without this, the app will not exit even if the window is closed
        self.capture.release()

    def start_camera(self, instance):
        # Start the camera when the button is pressed
        self.my_camera.start_capture()


if __name__ == '__main__':
    CameraApp().run()
