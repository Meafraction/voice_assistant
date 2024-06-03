import webbrowser
from pyowm import OWM
from datetime import datetime, date, time

import speech_recognition
import pyttsx3

sr = speech_recognition.Recognizer()
sr.pause_threshold = 1  # создаем паузу, после которой ассистент примет нашу команду
commands_dict = {
    'commands': {
        'search_for_information_on_google': ['искать', 'гугл', 'найди', 'найти'],
        'weather': ['погода', 'пагода'],
        'clock': ['время', 'часы'],
        'bye': ['стоп', 'хватит']
    }
}


def listen_comand():
    # try:
    with speech_recognition.Microphone() as mic:
        print('Listening...')
        sr.adjust_for_ambient_noise(source=mic, duration=1)
        audio = sr.listen(source=mic)
    try:
        query = sr.recognize_google(audio_data=audio, language='ru-RU').lower()
        say_voice('Вы сказали: ' + query)
        return query

    except speech_recognition.UnknownValueError:
        return 'Я не понял что ты сказал'


def search_for_information_on_google():
    print('что надо найти?')
    try:
        print('listen...')
        with speech_recognition.Microphone() as mic:
            sr.adjust_for_ambient_noise(source=mic, duration=1)
            audio = sr.listen(source=mic)
            search_term = sr.recognize_google(audio_data=audio, language='ru-RU').lower()

    except speech_recognition.UnknownValueError:
        return 'Я не понял что ты сказал'

    url = f"https://www.google.com/search?q={search_term}"
    webbrowser.open(url)
    return 'Открываю'


def weather():
    owm = OWM('78fc9cb466b4aa6945d253a266eec9b5')
    manager = owm.weather_manager()
    place = manager.weather_at_place("Brest ,BY")
    res = place.weather
    value = int(res.temperature('celsius')['temp'])

    return f'In Brest {value}'


def clock():
    time_checker = datetime.now().strftime("%H:%M")
    return f'Now {time_checker}'


def bye():
    say_voice('Пока пока')
    quit()


def say_voice(text):
    engine = pyttsx3.init()
    test = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\TokenEnums\RHVoice\Anna'
    engine.setProperty('voice', test)
    engine.say(text)
    print(text)
    engine.runAndWait()
    engine.stop()


def test():
    while True:
        query = listen_comand()
        for k, v in commands_dict['commands'].items():
            if query in v:
                return globals()[k]()
        print(query)


if __name__ == '__main__':
    print(test())
    # engine = pyttsx3.init()
    # voices = engine.getProperty('voices')
    # for voice in voices:
    #     print(voice.name)
    #     print(voice.id)
    #     print(voice.languages)
