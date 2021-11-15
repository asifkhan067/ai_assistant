import speech_recognition as sr
import pyttsx3
import functions
import SoundRecorder
import FaceDetection
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)


class Assistant:
    def take_command(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            r.pause_threshold = 1
            audio = r.listen(source)

        try:
            query = r.recognize_google(audio, language='en-in')

        except Exception as e:
            print(e)
            return "None"
        return query

    def speak(self, audio):
        engine.say(audio)
        engine.runAndWait()

    def tell_date(self):
        return functions.date()

    def tell_time(self):
        return functions.get_time()

    def launch_app(self, path_of_app):
        return functions.launch_app(path_of_app)

    def weather(self, city):
        try:
            res = functions.weather(city)
        except Exception as e:
            print(e)
            res = False
        return res

    def tell_me(self, topic):
        return functions.wikipedia(topic)

    def news(self):
        return functions.news()

    def send_mail(self, email_to, email_content):
        return functions.send_email(email_to, email_content)

    def system_info(self):
        return functions.system_stats()

    def location(self, destination):
        return functions.location(destination)

    def play_song(self, name):
        return functions.play(name)

    def join_class(self, class_name):
        return functions.join_class(class_name)

    def send_message(self, _to, message):
        functions.whats_msg(message, _to)

    def guess_my_emotion(self):
        return SoundRecorder.guess_emotion()[0]

    def who_is_this_person(self):
        return FaceDetection.get_name()
