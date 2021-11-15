import re
import os
import random
import pprint
import datetime
import sys
import pyjokes
import time
import pyautogui
import pywhatkit
import wolframalpha
import Assistant
import Credentials
import GUI
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

assistant_name = 'Redskull'
username = 'MR KHAN'
assistant = Assistant.Assistant()
Call = [f"hello {assistant_name}", f"{assistant_name}"]
Reply = ["i am ready sir", "how can i help you sir?"]
wol_app = Credentials.wol_app


def speak(sentence):
    assistant.speak(sentence)


def calculate(question):
    try:
        client = wolframalpha.Client(wol_app)
        answer = client.query(question)
        answer = next(answer.results).text
        print(answer)
        return answer
    except Exception:
        speak("Sorry sir I don't know the answer ")
        return None


def greet():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak(f"Good Morning {username} !")

    elif 12 <= hour < 18:
        speak(f"Good Afternoon {username} !")

    else:
        speak(f"Good Evening {username} !")

    speak(f"I am {assistant_name}, Your assistant ")
    speak("How can i Help you, Sir")


class MainThread(QThread):
    textChanged = QtCore.pyqtSignal(str)

    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.task_run()

    def task_run(self):
        greet()
        # print('')
        while True:
            time.sleep(2)
            self.textChanged.emit('Listening....')
            command = assistant.take_command().lower()
            self.textChanged.emit(f'Listening....\nUser said: {command}')
            if re.search('date', command):
                date = assistant.tell_date()
                self.textChanged.emit(date)
                speak(date)

            elif "time" in command:
                time_c = assistant.tell_time()
                self.textChanged.emit(time_c)
                speak(f"Sir the time is {time_c}")
            elif re.search('emotion', command):
                speech = "Ok sir, talk for 10 seconds then I'll guess."
                self.textChanged.emit(speech)
                speak(speech)
                emotion = assistant.guess_my_emotion()
                speech = f"You're {emotion},sir"
                self.textChanged.emit(speech)
                speak(speech)

            elif re.search('start', command):
                app = command.split(' ', 1)[1]
                path = Credentials.app_dic.get(app)
                if path is None:
                    self.textChanged.emit('Application path not found')
                    speak('Application path not found')
                else:
                    self.textChanged.emit(f'Starting: {app}, sir!')
                    speak(f'Starting: {app}, sir!')
                    assistant.launch_app(path)

            elif command in Call:
                reply = random.choice(Reply)
                self.textChanged.emit(reply)
                speak(reply)

            elif re.search('weather', command):
                city = command.split(' ')[-1]
                weather_res = assistant.weather(city)
                self.textChanged.emit(weather_res)
                speak(weather_res)

            elif re.search('tell me about', command):
                topic = command.split(' ')[-1]
                if topic:
                    wiki_res = assistant.tell_me(topic)
                    self.textChanged.emit(wiki_res)
                    speak(wiki_res)
                else:
                    sentence = "Sorry sir. I don't know what are you talking about"
                    self.textChanged.emit(sentence)
                    speak(sentence)

            elif "news" in command or "headlines" in command:
                news_res = assistant.news()
                speak('Todays Headlines are..')
                for index, articles in enumerate(news_res):
                    pprint.pprint(articles['title'])
                    speak(articles['title'])
                    if index == len(news_res) - 2:
                        break
                speak('These were the top headlines, Have a nice day Sir!!..')

            elif 'play' in command or "play music" in command or "hit some music" in command or 'youtube' in command:
                video = command.replace('play', '')
                video = video.replace('on youtube', '')
                video = video.replace('search', '')
                speak(f"Okay sir, playing {video} on youtube")
                pywhatkit.playonyt(video)

            elif "email" in command or "send email" in command:
                try:
                    speak("Whom do you want to email sir ?")
                    _to = assistant.take_command()
                    to_email = Credentials.email_list.get(_to)
                    if to_email:
                        speak("What is the subject sir ?")
                        subject = assistant.take_command()
                        speak("What should I say?")
                        message = assistant.take_command()
                        msg = 'Subject: {}\n\n{}'.format(subject, message)
                        assistant.send_mail(to_email, message)
                        speak("Email has been successfully sent")
                        time.sleep(2)
                    else:
                        speak("I coudn't remember the requested person's email.")

                except:
                    speak("Sorry sir. Couldn't send your mail. Please try again")

            elif "calculate" in command:
                question = command
                answer = calculate(question)
                speak(answer)

            elif "what is" in command or "who is" in command:
                question = command
                answer = calculate(question)
                speak(answer)

            elif "send a message" in command:
                try:
                    speak('To whom you want to send a message')
                    name = assistant.take_command()
                    contact = Credentials.contact_list.get(name.lower())
                    print(name)
                    if contact:
                        speak('what should I write in the message')
                        message = assistant.take_command()
                        assistant.send_message(contact, message)
                    else:
                        speak(
                            f"sorry sir, I don't remember {name}'s contact number")
                except Exception:
                    pass

            elif "joke" in command:
                joke = pyjokes.get_joke()
                print(joke)
                speak(joke)

            elif "system" in command:
                sys_info = assistant.system_info()
                print(sys_info)
                speak(sys_info)

            elif "where is" in command:
                place = command.split('where is ', 1)[1]
                assistant.location(place)

            elif "take screenshot" in command or "take a screenshot" in command or "capture the screen" in command:
                speak("what should be the name of screenshot?")
                name = assistant.take_command()
                speak("Alright sir, taking the screenshot")
                img = pyautogui.screenshot()
                name = f"{name}.png"
                img.save(name)
                speak("The screenshot has been successfully saved")

            elif "hide all files" in command or "hide this folder" in command:
                os.system("attrib +h /s /d")
                speak("Sir, all the files in this folder are now hidden")

            elif "goodbye" in command or "offline" in command or "bye" in command:
                speak("Alright sir, going offline. It was nice working with you")
                sys.exit()
            elif "join" in command or "class" in command:
                command = command.split()[-2]
                if command:
                    speak(f'joining {command} class')
                    try:
                        assistant.join_class(command.lower())
                        speak('Joined the class')
                    except Exception:
                        speak("Sorry Can't join right now")

            elif "do you know this person" in command or "do you know him" in command or "do you know her" in command:
                speech = 'Okay sir! opening camera'
                self.textChanged.emit(speech)
                speak(speech)
                try:
                    name = assistant.who_is_this_person()
                    if not name:
                        speech = "Sorry sir, I don't know this person"
                    else:
                        speech = f'This is {name}'
                except Exception:
                    speech = "Sorry! I can't open the camera right now"
                self.textChanged.emit(speech)
                speak(speech)

            else:
                speak("Sorry! can't recognize this command")


startExecution = MainThread()


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = GUI.uIMainWindow
        self.ui.setupUi(self=self.ui, MainWindow=self)
        self.ui.run.clicked.connect(self.start_task)
        self.ui.stop.clicked.connect(self.close)

    def __del__(self):
        sys.stdout = sys.__stdout__

    def start_task(self):
        self.ui.movie = QtGui.QMovie("resources/deepLearning.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        startExecution.textChanged.connect(self.ui.commands.setText)
        timer = QTimer(self)
        timer.timeout.connect(self.show_time)
        timer.start(1000)
        startExecution.start()

    def show_time(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.date.setText(label_date)
        self.ui.time.setText(label_time)


app = QApplication(sys.argv)
object = Main()
object.show()
exit(app.exec_())
