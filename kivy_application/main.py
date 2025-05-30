import time, json
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen



class MainWindow(Screen):
    def __init__(self, **kwargs):
        '''
        Initializes window layout and widget
        args: None
        return: None
        '''
        super(MainWindow, self).__init__(**kwargs)
                
        self.display = MainWidget(size_hint = (1, 0.8), pos_hint = {"y": 0.1})
        self.add_widget(self.display)
        
        self.add_widget(Label(text = f"{self.display.months[time.localtime().tm_mon - 1]}, {time.localtime().tm_mon}/{self.display.my_time}/{time.localtime().tm_year}",
                              font_size = 45, 
                              size_hint = (1, 0.1), 
                              pos_hint = {'top': 1}))
        save = Button(text = "Save", size_hint = (1, 0.1), pos_hint = {'bottom': 0}, font_size = 35)
        self.add_widget(save)
        self.write_back()
        
        save.bind(on_press = self.switch_page)
        
    def switch_page(self, instance, file = "saves.json"):
        '''
        When switching pages, writes down everything into JSON
        args: saves.json 
        return: None
        '''
        with open(file, "w") as my_doc:
            data = {date: text_input.text for date, text_input in self.display.replies_list.items()}
            json.dump(fp=my_doc, obj=data, indent=4)
        my_doc.close()
            
        wm.transition.direction = "right"
        wm.current = "notepad"

    def write_back(self, file = "saves.json"):
        '''
        Pulls info from saves.json file and writes them down into calendar
        args: saves.json
        return: None
        '''
        with open(file) as my_doc:
            data = json.load(my_doc)
            for date, text_input in self.display.replies_list.items():
                text_input.text = data[str(date)]
        my_doc.close()
 
        
def first_again():
    '''
    Finds First Day of monts
    args: None
    return: List of integers representing first day of the month for next 3 months
    '''
    first_list = []
    month = time.localtime().tm_mon
    for _ in range(3):
        updated = time.strptime(f"{time.localtime().tm_year}-{month:02d}-01", "%Y-%m-%d").tm_wday
        first_list.append(updated)
        month += 1
    return first_list
vals = first_again()


        
class MainWidget(GridLayout):
    def __init__(self, **kwargs):
        '''
        Initializes mainwidget layout and widgets that appear under mainwindow
        args: None
        return: None
        '''
        super(MainWidget, self).__init__(**kwargs)
        self.cols = 7
        date = 1
        self.replies_list = {}
        
        self.my_time = time.localtime().tm_mday 
        days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        self.months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        
        for _ in range(7):
            self.add_widget(Label(text = f"{days[_]}", font_size = 25, size_hint = (1, 0.2)))
        
        self.indent()

        for _ in range(31):
            self.replies = TextInput(hint_text = f'Day {date}', 
                                     hint_text_color = (0, 0, 0, 1), 
                                     font_size = 15, 
                                     background_color = (1, 1, 1, 1) if date >= self.my_time else (1, 1, 1, 0.5))
            self.replies_list[date] = self.replies    
            self.add_widget(self.replies)    
            date += 1

    def first(self, month = time.localtime().tm_mon):
        '''
        Initializes layout and widget
        args: month
        return: Integer representing first day of week
        '''
        updated = time.strptime(f"{time.localtime().tm_year}-{month:02d}-01", "%Y-%m-%d").tm_wday
        print("Updated", updated)
        return updated

    def indent(self):
        '''
        Adds indent based on first day of month, meaning if Sunday there is no indent, and if another day, 
        moves forward necessary columns
        args: None
        return: None
        '''
        self.first_day = vals[0]
        if self.first_day != 6:
            for _ in range(self.first_day + 1):
                self.add_widget(Label())
                
    def updated(self):
        '''
        Updates to first day
        args: None
        return: None
        '''
        self.first_day = vals[1]
                

        
class Notepad(Screen):
    def __init__(self, **kwargs):
        '''
        Initializes layout and widget
        args: None
        return: None
        '''
        super(Notepad, self).__init__(**kwargs)
        self.add_widget(Label(text = "Notepad [Won't Save]", font_size = 40, size_hint = (1, 0.1), pos_hint = {"top": 1}))
        self.add_widget(TextInput(size_hint = (1, 0.9), pos_hint = {"bottom": 0}))
        back = Button(text = "Back", size_hint = (0.2, 0.2), pos_hint = {"x": 0.8}, font_size = 40)
        self.add_widget(back)
        back.bind(on_press = self.go_back)
        
    def go_back(self, instance):
        '''
        Function to return to prevous page
        args: None
        return: None
        '''
        wm.transition.direction = "left"
        wm.current = "main"       
  

# Initializing and naming all screens using screenmanager  
wm = ScreenManager()
mw = MainWindow(name = "main")
wm.add_widget(mw)
np = Notepad(name = "notepad")
wm.add_widget(np)


# Runs app using screenmanager
class CalendarApp(App):
    def build(self):
        return wm


if __name__ == '__main__':
    CalendarApp().run()