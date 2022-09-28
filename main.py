from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from twitter_credentials import *
from selenium import common
from selenium.webdriver.support.select import Select
# import time

import speech_recognition as sr
import pyttsx3
import time

r = sr.Recognizer()


to_ask = ["name", "place of incident", "District", "complaint text"]
durations = [5, 5, 5, 20]


def speak_text(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


current_index = 0
stored_values = {}
# Loop infinitely for user to
# speak
flag = True
speak_text("Hello, I am your online F I R assistant.")
while current_index < len(to_ask):

    # Exception handling to handle
    # exceptions at the runtime
    try:
        text = f"Please tell me your {to_ask[current_index]}."
        speak_text(text)
        # use the microphone as source for input.
        with sr.Microphone() as source:
            time.sleep(1)
            speak_text("Speak Now")
            # wait for a second to let the recognizer
            # adjust the energy threshold based on
            # the surrounding noise level
            r.adjust_for_ambient_noise(source, duration=0.5)

            # listens for the user's input
            audio2 = r.record(source, duration=durations[current_index], offset=0)

            # Using google to recognize audio
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
            print(MyText)
            speak_text("Did you say")
            speak_text(MyText)
            speak_text("Please say yes or no")
            speak_text("Speak Now")
            audio_confirmation = r.record(source, duration=5, offset=0)
            confirmation_txt = r.recognize_google(audio_confirmation)
            confirmation_txt = confirmation_txt.lower()
            print(confirmation_txt)
            if "yes" in confirmation_txt:
                stored_values[to_ask[current_index]] = MyText
                current_index += 1
    except sr.RequestError as e:
        speak_text("Could not request results; {0}".format(e))

    except :
        speak_text("unknown error occurred")

print(stored_values)
timeout = time.time() + 60 * 4
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
s = Service("D:\Webservices ML\chromedriver.exe")
complaint_text = stored_values["complaint text"]
place_of_incident = stored_values["place of incident"]
District = stored_values["District"]
driver = webdriver.Chrome(service=s, options=chrome_options)


def online_fir_hp():
    driver.maximize_window()
    driver.get("http://citizenportal.hppolice.gov.in:8080/citizen/login.htm")
    driver.find_element(By.ID, value="close-btn").click()
    driver.find_element(By.ID, value="username").send_keys(fir_username)
    driver.find_element(By.ID, value="password").send_keys(fir_password)
    driver.find_element(By.ID, value="button").click()
    time.sleep(5)
    driver.get("http://citizenportal.hppolice.gov.in:8080/citizen/complaintregistration.htm")
    Select(driver.find_element(By.ID, value="nature1")).select_by_index(2)
    driver.find_element(By.LINK_TEXT, value="Incident Details").click()
    driver.find_element(By.ID, value="POI").send_keys(place_of_incident)
    driver.find_element(By.LINK_TEXT, value="Complaint Details").click()
    driver.find_element(By.ID, value="CompDep").send_keys(complaint_text)
    driver.find_element(By.LINK_TEXT, value="Complaint Submission Details").click()
    driver.find_element(By.ID, value="radioButtnId1").click()
    Select(driver.find_element(By.ID, value="Dist")).select_by_visible_text(District)


def tweet(body):
    driver.get("https://twitter.com/i/flow/login")
    element_found = False
    while not element_found:
        try:
            dd = driver.find_element(by=By.NAME, value="text")
            dd.send_keys(username)
            dd.send_keys(Keys.ENTER)
            element_found = True
            time.sleep(5)
        except NoSuchElementException:
            time.sleep(5)
            print("Element upload not found")
            continue

    element_found = False
    while not element_found:
        try:
            dd = driver.find_element(by=By.NAME, value='password')
            dd.send_keys(password)
            dd.send_keys(Keys.ENTER)
            element_found = True
        except NoSuchElementException:
            time.sleep(5)
            print("Element upload not found")
            continue
        time.sleep(15)
        compose_button = False
        while not compose_button:
            try:
                driver.find_element(by=By.XPATH,
                                    value='//*[@id="react-root"]/div/'
                                          'div/div[2]/header/div/div/div/div[1]/div[3]').click()
                compose_button = True
            except NoSuchElementException:
                time.sleep(5)
                print("Element not found")
                continue
        time.sleep(2)

        try:
            driver.find_element(by=By.XPATH, value="//div[@role='textbox']").send_keys(body)
        except common.exceptions.NoSuchElementException:
            time.sleep(3)
            driver.find_element(by=By.XPATH, value="//div[@role='textbox']").send_keys(body)

        time.sleep(4)
        driver.find_element(by=By.CLASS_NAME, value="notranslate").send_keys(Keys.ENTER)
        driver.find_element(by=By.XPATH, value="//div[@data-testid='tweetButton']").click()
        time.sleep(4)


try:
    online_fir_hp()
finally:
    tweet_text = f"I am {stored_values['name']}, I am from {stored_values['District']}. {stored_values['complaint text']}." \
                 f"This happened at {stored_values['place of incident']}. "
    tweet(tweet_text)
driver.quit()
