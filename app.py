from cProfile import label
import kivy 
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.properties import NumericProperty 


Builder.load_string('''
<MainWidget>:
    BoxLayout:
        size: root.size
        orientation: 'vertical'

        Label:
            id: timeLabel
            text: str(round(root.overallTime, 2))
            font_size: 30
        
        Label:
            id: lapLabel
            text: str(round(root.lapTime, 2))
            font_size: 20
        
        GridLayout:
            cols: 3

            Label:
                text: 'Lap'

            Label:
                text: 'Lap times'

            Label:
                text: 'Overall Time'


        ScrollView:
            size_hint_y: 3
            pos_hint: {'x':0, 'y': .11}
            do_scroll_x: False
            do_scroll_y: True

            GridLayout:
                id: lapsGrid
                cols: 3
                size:(root.width, root.height)
                size_hint_x: None
                size_hint_y: None
                height: self.minimum_height
                row_default_height: 50
                row_force_default: True

        
        GridLayout:
            cols: 4

            Button:
                text: 'lap'
                on_press: root.lap()
            
            Button:
                text: 'restart'
                on_press: root.restart()

            Button:
                text: 'stop'
                on_press: root.stop()

            Button:
                text: 'start'
                on_press: root.start()


''')

class MainWidget(BoxLayout): 
    overallTime = NumericProperty()
    lapTime = NumericProperty()
    lapId = 1
    isRunning = False


    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        

    def increment_time(self, interval):
        self.overallTime += interval
        self.lapTime += interval

    def start(self):
        Clock.unschedule(self.increment_time)
        Clock.schedule_interval(self.increment_time, .1)
        self.isRunning = True

    def stop(self):
        Clock.unschedule(self.increment_time)
        self.isRunning = False

    def restart(self):
        self.overallTime = 0
        self.lapTime = 0
        self.lapId = 1
        labels = [i for i in self.ids.lapsGrid.children]
        for child in labels:
            self.ids.lapsGrid.remove_widget(child)
        self.stop()

    def lap(self):
        if not self.isRunning: return
        self.lapIdLabel = Label(text=str(self.lapId))
        self.lapTimeLabel = Label(text=str(round(self.lapTime, 2)))
        self.lapAllTimeLabel = Label(text=str(round(self.overallTime, 2)))
        self.ids.lapsGrid.add_widget(self.lapIdLabel)
        self.ids.lapsGrid.add_widget(self.lapTimeLabel)
        self.ids.lapsGrid.add_widget(self.lapAllTimeLabel)
        self.lapId += 1
        self.lapTime = 0


    

class MyApp(App):
    def build(self):
        return MainWidget()


if __name__ == '__main__':
    MyApp().run()