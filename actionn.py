from kivy.app import App
from kivy.uix.actionbar import ActionItem, ActionToggleButton, ActionButton, ActionSeparator
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen, RiseInTransition, FadeTransition, SlideTransition
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
from datetime import datetime, timedelta
from main1 import chat
from random import choice as ch
from time import sleep
from selenium import webdriver
import win32gui, win32con, win32com.client

## Global Things

import pyttsx3
engine = pyttsx3.init() # object creation
import sys
sys.path.append('\\PythonVersion\\lib\\site-packages\\win32')
sys.path.append('\\PythonVersion\\lib\\site-packages\\win32\\lib')

rate = engine.getProperty('rate')
engine.setProperty('rate', 125)
volume = engine.getProperty('volume')
engine.setProperty('volume',1.0)
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

import speech_recognition as sr
r = sr.Recognizer()
mic = sr.Microphone()

sm1, main, response, image, querry, mic_status, browser, cont_flag, sc = None, None, None, None, None, 0, None, 1, 'home'
timep, timenow, counter, popupWindow, main_text, act_check, home_flag = None, None, None, None, None, None, 1
ans_text = main_text

def speak(res, mic_status):
    if mic_status:
        engine.say(res)
        engine.runAndWait()
        engine.stop()

def show_popup():
    global popupWindow
    def windowEnumerationHandler(hwnd, top_windows):
        top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))
    results = []
    top_windows = []
    win32gui.EnumWindows(windowEnumerationHandler, top_windows)
    for i in top_windows:
        if ("rait assisstant" in i[1].lower() and "command" not in i[1].lower()):
            print(i[1])
            win32gui.ShowWindow(i[0], win32con.SW_MAXIMIZE)
            shell = win32com.client.Dispatch("WScript.Shell")
            shell.SendKeys('%')
            win32gui.SetForegroundWindow(i[0])
            break
    show = content()
    popupWindow = Popup(title="No User Activity!!!", content=show, size_hint=(None,None),size=(600,200), auto_dismiss=False)
    popupWindow.open()

def check_activity(dt):
    global timep, mic_status, timenow
    timenow = datetime.now()
    if ((timenow > timep + timedelta(seconds=180))):
        print('User is idle, timenow = ', timenow)
        show_popup()
        res = 'No user activity detected since '+str((timenow - timep).seconds//60)+' minutes'
        speak(res, mic_status)
        #timep = timenow

def exxit():
    ## RPi GPIO 'done' signal (add here)
    try:
        popupWindow.dismiss()
    except Exception:
        pass
    global main, mic_status, browser
    try:
        browser.close()
    except Exception:
        pass
    main.ids['txt'].text = 'Bye'
    speak('Bye', mic_status)
    sm1.transition = FadeTransition(duration = 1)
    sm1.current = 'exit'
    Clock.unschedule(act_check)

def home(text):
    global main, mic_status, ans_text, browser, home_flag, sc
    try:
        popupWindow.dismiss()
        home_flag = 0
    except Exception:
        pass
    try:
        browser.close()
    except Exception:
        pass

    if text == 'UserManual':
        sm1.transition = SlideTransition(direction = 'right', duration = 0.5)
        sm1.current = 'UserManual'
    else:
        main.ids['txt'].text = text
        sm1.transition = SlideTransition(direction = 'right', duration = 0.5)
        sm1.current = 'main'
    sc = 'home'
    #speak(main_text, mic_status)

def continuee():
    global cont_flag
    cont_flag = 0
    popupWindow.dismiss()
    def windowEnumerationHandler(hwnd, top_windows):
        top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))
    results = []
    top_windows = []
    win32gui.EnumWindows(windowEnumerationHandler, top_windows)
    try:
        for i in top_windows:
            if ("google" in i[1].lower()):
                print(i[1])
                win32gui.ShowWindow(i[0], win32con.SW_MAXIMIZE)
                win32gui.SetForegroundWindow(i[0])
                break
    except Exception:
        pass

## End global things

class ExitWindow(Screen):
    pass

class MainWindow(Screen):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        global querry, act_check
        act_check = Clock.schedule_interval(check_activity, 60)
        querry = ActionText()
        with mic as source:
            r.adjust_for_ambient_noise(source, duration = 2)

        self.ids.abu.action_view.add_widget(PreviousButton())
        #self.ids.abu.action_view.add_widget(ActionSeparator())
        self.ids.abu.action_view.add_widget(querry)
        self.ids.abu.action_view.add_widget(SearchButton())
        self.ids.abu.action_view.add_widget(SpeakerButton())
      
        self.ids.abd.action_view.add_widget(ExitButton())
        self.ids.abd.action_view.add_widget(ActionSeparator())
        #self.ids.abd.action_view.add_widget(Separator())
        self.ids.abd.action_view.add_widget(ClickButton())
        self.ids.abd.action_view.add_widget(ActionSeparator())
        self.ids.abd.action_view.add_widget(VolumeButton())

class ImageWindow(Screen):
    def __init__(self, *args, **kwargs):
        super(ImageWindow, self).__init__(*args, **kwargs)
        self.ids.abi.action_view.add_widget(PreviousButton())
        self.ids.abi.action_view.add_widget(Separator())
        

class UserManualWindow(Screen):
    def __init__(self, *args, **kwargs):
        super(UserManualWindow, self).__init__(*args, **kwargs)
        self.ids.abm.action_view.add_widget(PreviousButton())
        self.ids.abm.action_view.add_widget(ActionLabel1())
        self.ids.abm.action_view.add_widget(NextButton())

class ReadMeWindow(Screen):
    def __init__(self, *args, **kwargs):
        super(ReadMeWindow, self).__init__(*args, **kwargs)
        self.ids.abr.action_view.add_widget(PreviousButton())
        self.ids.abr.action_view.add_widget(ActionLabel2())

class IncrediblyCrudeClock(Label, FloatLayout):
    def __init__(self, *args, **kwargs):
        super(IncrediblyCrudeClock, self).__init__(*args, **kwargs)
               
    a = NumericProperty(30)  # seconds

    def start(self):
        Animation.cancel_all(self)  # stop any current animations
        self.anim = Animation(a=0, duration=self.a)
        def finish_callback(animation, incr_crude_clock):
            incr_crude_clock.text = "0"
            popupWindow.dismiss()
            global cont_flag, home_flag
            if (cont_flag and home_flag):
                cont_flag, home_flag = 1, 1
                exxit()
        self.anim.bind(on_complete=finish_callback)
        self.anim.start(self)

    def on_a(self, instance, value):
        counter.text = str(round(value))+' seconds remaining...'
        self.pos_hint = {'x': 0, 'top': 1}
        self.size_hint = (0,0.2)

class content(FloatLayout):
    def __init__(self, *args, **kwargs):
        super(content, self).__init__(*args, **kwargs)
        global counter, timenow, timep
        res = 'No user activity detected since '+str((timenow - timep).seconds//60)+' minutes...\nDo you want to continue?'
        self.add_widget(Label(text = res, size_hint = (0.3, 0.4), pos_hint = {"x":0.1, "top":1}))
        counter = Label(size_hint = (0.3, 0.2), pos_hint = {"x":0, "top":0.7})
        self.add_widget(counter)
        crudeclock = IncrediblyCrudeClock()
        crudeclock.start()
        self.add_widget(Button(text = "Continue", size_hint = (0.3, 0.2), pos_hint = {"x":0, "y":0.1}, on_release = lambda *args: continuee()))
        self.add_widget(Button(text = "Home", size_hint = (0.3, 0.2), pos_hint = {"x":0.35, "y":0.1}, on_release = lambda *args: home(main_text)))
        self.add_widget(Button(text = "Exit", size_hint = (0.3, 0.2), pos_hint = {"x":0.7, "y":0.1}, on_release = lambda *args: exxit()))


class ActionText(TextInput, ActionItem):
    def __init__(self, *args, **kwargs):
        super(ActionText, self).__init__(*args, **kwargs)
        self.multiline = False
        self.size_hint_x =  0.1
        self.size_hint_y =  0.7
        self.font_size = 20
        self.pos_hint =  {'x': 1, 'top': 0.8}
        self.hint_text = 'Type Here...'
        self.important = True
        focus = True

    def on_text_validate(self, *args):
        global timep, main, response, image, mic_status, ans_text, sc
        timep = datetime.now()
        #print(timep)
        response = chat(self.text)

        if str(response[0][-3::]) == 'jpg':
            sc = 'not home'
            res = ch(response[1:])
            main.ids['txt'].text, ans_text = str(res), str(res)
            speak(res, mic_status)
            image.ids['image'].source = response[0]
            sm1.transition = SlideTransition(direction = 'left', duration = 0.5)
            sm1.current = 'image'

        elif str(response[0]) == 'manual.png':
            sc = 'not home'
            res = ch(response[1:])
            main.ids['txt'].text, ans_text = str(res), str(res)
            speak(res, mic_status)
            sm1.transition = SlideTransition(direction = 'left', duration = 0.5)
            sm1.current = 'UserManual'

        elif str(response[0][:4]) == 'http':
            #res = response[1]
            res = ch(['Check this link out', "Here's the answer to your querry", 'Navigating to RAIT website...'])
            main.ids['txt'].text, ans_text = str(res), str(res)
            speak(res, mic_status)
            #webbrowser.open(response[0])
            global browser
            browser = webdriver.Chrome(executable_path = r'C:/Users/admin/Downloads/chromedriver_win32/chromedriver.exe')
            browser.get(str(response[0]))
            browser.maximize_window()

        elif (self.text.lower() in ['bye', 'ok bye', 'thankyou','see you later','Goodbye']) or (ch(response) in ["Have a nice day", "Bye!"]):
            res = ch(["Have a nice day", "Bye!"])
            speak(res, mic_status)
            main.ids['txt'].text = str(res)
            exxit()
        else:
            res = ch(response)
            main.ids['txt'].text = str(res)
            speak(res, mic_status)

    def on_focus(self, instance, value):
        global timep
        timep = datetime.now()
        #print(timep)

class SearchButton(ActionButton):
    def __init__(self, *args, **kwargs):
        super(SearchButton, self).__init__(*args, **kwargs)
        self.icon = 'search1.png'
        self.text = 'Search'

    def on_release(self):
        querry.on_text_validate()


class SpeakerButton(ActionButton):
    def __init__(self, *args, **kwargs):
        super(SpeakerButton, self).__init__(*args, **kwargs)
        self.icon = 'mic1.png'
        self.text = 'Voice'

    def on_release(self):
        global mic_status
        res = 'Listening...'
        main.ids['txt'].text = str(res)
        speak(res, mic_status)
        with mic as source:
            try:
                audio = r.listen(source, timeout = 5)
            except sr.WaitTimeoutError:
                res = 'Error due to timeout!!'
                main.ids['txt'].text = str(res)
                speak(res, mic_status)
                res = ' Try again'
                main.ids['txt'].text += str(res)
                speak(res, mic_status)
        try:
            t=r.recognize_google(audio, language='en')
            print(t)
            querry.text = str(t)
            main.ids['txt'].text = ''
            querry.on_text_validate()
        except sr.UnknownValueError:
            res = "Unable to recognize speech.."
            main.ids['txt'].text = str(res)
            speak(res, mic_status)
            res = ' Try again'
            main.ids['txt'].text += str(res)
            speak(res, mic_status)
        except IndexError:                                  # the API key didn't work
            res = "Please check your internet connection"
            main.ids['txt'].text = str(res)
            speak(res, mic_status)
        except NameError:
            pass
       

class PreviousButton(ActionButton):
    def __init__(self, *args, **kwargs):
        super(PreviousButton, self).__init__(*args, **kwargs)
        self.icon = 'chevron-left.png'
        self.text = 'Home'
    def on_release(self):
        global sc, main_text, ans_text
        if sc == 'home' or sc is None:
            home(main_text)
        elif sc == 'readme' :
            home('UserManual')
        else:
            home(ans_text)

class NextButton(ActionButton):
    def __init__(self, *args, **kwargs):
        super(NextButton, self).__init__(*args, **kwargs)
        self.icon = 'chevron-right.png'
        self.text = 'Next'
    def on_release(self):
        global sc 
        sc = 'readme'
        sm1.transition = SlideTransition(direction = 'left', duration = 0.5)
        sm1.current = 'ReadMe'
        

class ExitButton(ActionButton):
    def __init__(self, *args, **kwargs):
        super(ExitButton, self).__init__(*args, **kwargs)
        self.text = 'Exit'
    def on_release(self):
        exxit()


class ClickButton(ActionButton):
    def __init__(self, *args, **kwargs):
        super(ClickButton, self).__init__(*args, **kwargs)
        self.text = 'User Guide'
        self.size_hint_x =  0.9
    def on_release(self):
         sm1.transition = SlideTransition(direction = 'left', duration = 0.5)
         sm1.current = 'UserManual'
        

class VolumeButton(ActionToggleButton):
    def __init__(self, *args, **kwargs):
        super(VolumeButton, self).__init__(*args, **kwargs)
        self.icon = 'mutevolume1.png'
              
    def on_state(self, tb, state):
        global mic_status, main_text, main
        if state == 'down':
            self.icon = 'volume1.png'
            mic_status = 1
            if (main.ids['txt'].text == main_text):
                speak(main_text, mic_status)
        else:
            self.icon = 'mutevolume1.png'
            mic_status = 0
        
        
class Separator(ActionSeparator):
    def __init__(self, *args, **kwargs):
        super(Separator, self).__init__(*args, **kwargs)
        self.size_hint_x = 0.00001
        self.important = True
        #self.background_image = 'background.png'

class ActionLabel2(Label, ActionItem):
    def __init__(self, *args, **kwargs):
        super(ActionLabel2, self).__init__(*args, **kwargs)
        self.font_size = 40
        self.multiline = False
        self.size_hint_x = 1
        self.h_align = 'center'
        self.text = 'Read Me'

class ActionLabel1(Label, ActionItem):
    def __init__(self, *args, **kwargs):
        super(ActionLabel1, self).__init__(*args, **kwargs)
        self.font_size = 40
        self.multiline = False
        self.size_hint_x = 1
        self.h_align = 'center'
        self.text = 'User Manual'
        
        
class ActionApp(App):
    def build(self):
        self.title = 'RAIT ASSISSTANT'
        Window.borderless = True
        Window.fullscreen = True
        #Window.size = (800, 500)
        Builder.load_file('actionn.kv')
        global timep, sm1, main, image, main_text
        timep = datetime.now()
        print(timep)
        sm1 = ScreenManager()
        main = MainWindow(name='main')
        sm1.add_widget(main)
        sm1.add_widget(ExitWindow(name='exit'))
        image = ImageWindow(name='image')
        sm1.add_widget(image)
        main_text = main.ids['txt'].text
        sm1.add_widget(UserManualWindow(name='UserManual'))
        sm1.add_widget(ReadMeWindow(name='ReadMe'))
        return sm1
       
ActionApp().run()

