import json
import math
import smtplib
import subprocess
import psutil as psutil
import requests
import Credentials
import datetime
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from Credentials import Google
import pywhatkit

user_credentials = Google().user_credentials


def get_time():
    str_time = datetime.datetime.now().strftime("% H:% M:% S")
    return str_time


def date():
    str_date = datetime.datetime.now().strftime("%b %d %Y")
    return str_date


def launch_app(path_of_app):
    try:
        subprocess.call([path_of_app])
        return True
    except Exception as e:
        print(e)
        return False


def weather(city):
    api_key = Credentials.weather_api
    format_ = "&units=metric"
    base_url = "http://api.openweathermap.org/data/2.5/weather?q="
    url = base_url + city + "&appid=" + api_key + format_
    response = requests.get(url)
    city_weather_data = response.json()
    if city_weather_data["cod"] != "404":
        main_data = city_weather_data["main"]
        weather_description_data = city_weather_data["weather"][0]
        weather_description = weather_description_data["description"]
        current_temperature = main_data["temp"]
        current_pressure = main_data["pressure"]
        current_humidity = main_data["humidity"]
        wind_data = city_weather_data["wind"]
        wind_speed = wind_data["speed"]

        final_response = f"""
The weather in {city} 
is currently {weather_description} 
with a temperature of {current_temperature} degree Celsius.
        """
        return final_response
    else:
        return "Sorry Sir, I couldn't find the city right now. Please try again"


def wikipedia(topic):
    results = wikipedia.summary(topic, sentences=3)
    return results


def news():
    url = 'http://newsapi.org/v2/top-headlines?sources=the-times-of-india&apiKey='
    url += Credentials.news_api
    news_data = requests.get(url).text
    news_dic = json.loads(news_data)
    articles = news_dic['articles']
    try:
        return articles
    except:
        return False


def send_email(self, email_to, email_content):
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    server = smtp
    server.ehlo()
    server.starttls()
    server.login(Credentials.Google.user_credentials['email'], Credentials.Google.user_credentials['password'])
    server.sendmail(Credentials.Google.user_credentials['email'], email_to, email_content)
    server.close()


def join_class(class_name):
    try:
        code = Credentials.class_codes[class_name]
        browser = webdriver.Firefox()
        browser.get('https://meet.google.com/')
        browser.find_element(By.XPATH, '/html/body/header/div[1]/div/div[3]/div[1]/div/span[1]/a').click()
        time.sleep(0.2)
        browser.find_element(By.XPATH, '//*[@id="identifierId"]').send_keys(user_credentials['email'])
        xpath = '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button'
        browser.find_element(By.XPATH, xpath).click()
        time.sleep(2)
        xpath = '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/' \
                'span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input'
        browser.find_element(By.XPATH, xpath).send_keys(user_credentials['password'])
        xpath = '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button'
        time.sleep(1)
        browser.find_element(By.XPATH, xpath).click()
        xpath = '//*[@id="i3"]'
        time.sleep(2)
        browser.find_element(By.XPATH, xpath).send_keys(code)
        time.sleep(0.1)
        xpath = '/html/body/c-wiz/div/div[2]/div/div[1]/div[3]/div/div[2]/div[2]/button/span'
        browser.find_element(By.XPATH, xpath).click()
        time.sleep(5)
        xpath = '/html/body/div[1]/c-wiz/div/div/div[9]/div[3]/div/div/div[3]/div/' \
                'div/div[2]/div/div[2]/div/div/div[1]/span'
        browser.find_element(By.XPATH, xpath).click()
    except Exception as e:
        print(e)


def location(destination):
    try:
        browser = webdriver.Firefox()
        browser.get('https://www.google.com/')
        xpath = '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input'
        browser.find_element(By.XPATH, xpath).send_keys(destination + Keys.ENTER)
        time.sleep(2)
        xpath = '/html/body/div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div' \
                '/div/div[1]/div/div[2]/div/div/div[1]/div/div/div[4]/div[3]/div/div/div[2]/div[1]/div[1]/a'
        browser.find_element(By.XPATH, xpath).click()
        time.sleep(2)
        xpath = '//*[@id="section-directions-trip-0"]'
        browser.find_element(By.XPATH, xpath).click()
    except Exception as e:
        pass


def calculate(query):
    browser = webdriver.Firefox()
    browser.get('https://www.google.com/')
    xpath = '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input'
    browser.find_element(By.XPATH, xpath).send_keys(query + Keys.ENTER)
    time.sleep(2)
    xpath = '/html/body/div[7]/div/div[9]/div[1]/div/div[2]/div[2]/div/div/div[1]/div' \
            '/div/div[1]/div/div/div[1]/div[2]/div[2]/div/div/span'
    ans = browser.find_element(By.XPATH, xpath).text
    return ans


def whats_msg(message_to_send, number):
    try:
        pywhatkit.sendwhatmsg_instantly(number, message_to_send)
    except Exception:
        pass


def convert_size(size_bytes):
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    print("%s %s" % (s, size_name[i]))
    return "%s %s" % (s, size_name[i])


def system_stats():
    cpu_stats = str(psutil.cpu_percent())
    battery_percent = psutil.sensors_battery().percent
    memory_in_use = convert_size(psutil.virtual_memory().used)
    total_memory = convert_size(psutil.virtual_memory().total)
    final_res = f"Currently {cpu_stats} percent of CPU, {memory_in_use} of RAM out of total {total_memory}  is being used and battery level is at {battery_percent} percent"
    return final_res
