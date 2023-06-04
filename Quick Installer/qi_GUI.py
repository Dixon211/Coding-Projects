from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout


class MainWindow(GridLayout):
    def __init__(self):
        self.cols=2
        
        

class QuickInstall(App):
    def build(self):
        
        return MainWindow()


# to create the app as it is run
if __name__ == '__main__':
    QuickInstall().run()