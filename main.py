# Import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout

# Membuat kelas aplikasi
class HelloWorldApp(App):
    def build(self):
        # Membuat tata letak (layout) dengan kotak (Box)
        layout = BoxLayout(orientation='vertical')

        # Menambahkan label ke layout
        label = Label(text='Hello, World!')
        layout.add_widget(label)

        # Menambahkan tombol ke layout
        button = Button(text='Click Me!', on_press=self.on_button_click)
        layout.add_widget(button)

        # Mengembalikan layout sebagai antarmuka pengguna aplikasi
        return layout

    # Fungsi yang akan dipanggil saat tombol ditekan
    def on_button_click(self, instance):
        print('Button Clicked!')

# Membuat instance aplikasi dan menjalankannya
if __name__ == '__main__':
    HelloWorldApp().run()
