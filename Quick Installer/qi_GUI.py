from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserListView
import subprocess



class LeftBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        label = Label(text="Hello, World!")
        self.add_widget(label)
        
class RightBox(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        add_prgm_but = Button(text="Add Program...")
        add_batch_but = Button(text="Add Batch File...")
        install_but = Button(text = "Install")
        
        add_batch_but.bind(on_press=self.open_explorer)
        
        self.add_widget(add_prgm_but)
        self.add_widget(add_batch_but)
        self.add_widget(install_but)
     
    def open_explorer(self, instance):
        file_path = filechooser.open_file(on_selection=self.handle_selection)
        if file_path:
            file_info = extract_file_info(file_path)
            file_info_label.text = f"Selected file: {file_info}"

class MyApp(App):
    def build(self):
        main_box = BoxLayout(orientation="horizontal")
        left_half=LeftBox()
        right_half=RightBox(orientation="vertical")
        main_box.add_widget(left_half)
        main_box.add_widget(right_half)
        return main_box


if __name__ == "__main__":
    MyApp().run()
