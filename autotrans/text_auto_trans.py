import pynput
import time
from translate import Translator
from pynput.keyboard import Key, KeyCode

target_language = input("Enter target language (e.g. 'fr', 'de', 'ja', etc.): ")
sentence = ""

def on_press(key):
    global sentence
    end_mark = ""
    try:
        char = key.char
        sentence += char
        if char in ['.', '!', '?']:
            end_mark = char
    except AttributeError:
        if key == Key.backspace:
            sentence = sentence[:-1]
            return
        elif key == Key.space:
            sentence += " "
            return
        char = ""
    if not end_mark:
        return
    if not sentence:
        return
    try:
        translator = Translator(to_lang=target_language)
        translated_sentence = translator.translate(sentence)
    except Exception as e:
        print("Translation failed:", e)
        translated_sentence = sentence
    
    keyboard = pynput.keyboard.Controller()
    for i in range(len(sentence)):
        keyboard.press(Key.backspace)
        time.sleep(0.2)
        keyboard.release(Key.backspace)
    keyboard.type(translated_sentence)
    sentence = ""

with pynput.keyboard.Listener(on_press=on_press) as keyboard_listener:
    keyboard_listener.join()