#!/usr/bin/env python
from pynput.keyboard import Key, Controller, Listener
import time
import os
import sys

import get_clipboard
import toolkit_config

profileModeKey = 'p'
fileModeKey = 'f'


def long_text_input_confirm(textInput, maxWordCount):
    if len(textInput) > maxWordCount:
        confirm = input(
            'Long text ({} > {}) detected, do you really want to input this text?  Y/N: '.format(len(textInput), maxWordCount))
        if confirm.upper() == 'N':
            return False
    return True


def print_config(printFlag=None):
    '''print and return config file in dict'''
    configDict = {}
    for shortcutName, shortcutValue in profile.items():
        # print(shortcutName, shortcutValue)
        # print(shortcutValue.get('KEY'))

        # if KEY in dict is None, cut the shortcut section name
        if not shortcutValue.get('KEY'):
            shortcutValue['KEY'] = shortcutName.replace('Shortcut_', '')

        if len(shortcutValue['KEY']) != 1:
            print('Error found in {}, key length cannot exceed 1, current: {} '.format(
                shortcutName, shortcutValue['KEY']))
        if printFlag:
            print('[%(KEY)s] %(TITLE)s: %(TEXT)s' % shortcutValue)
        configDict[shortcutValue['KEY']] = shortcutValue['TEXT']
    return configDict


def flash_caps_lock_light():
    keyboard = Controller()
    key = Key.caps_lock
    for i in range(4):
        keyboard.press(key)
        keyboard.release(key)
        time.sleep(.5)


def profile_mode():
    '''Read the text from config file, and called by key '''

    with Listener(on_release=on_release) as listener:
        listener.join()
    return


def type_text(text):
    for char in text:
        if char != '\n' and char != '\r\n':
            keyboard.press(char)
            keyboard.release(char)
            time.sleep(interval)


def wait(sleepTime):
    print('sleep {} seconds...'.format(sleepTime), end = '')
    time.sleep(sleepTime)
    print('Typing...')

def text_to_keystroke():
    global profileMode
    text = ''
    if profileMode == False:
        text = input('[*] Convert these text into keystroke, press <{}> to go to profile mode, <{}> to go to file mode :\n'.format(
            profileModeKey, fileModeKey))  # .strip()
    if not long_text_input_confirm(text, maxWordCount):
        return

    # print(profileMode)
    if text == profileModeKey or profileMode == True:
        profileMode = True
        print('-' * 40)
        print("Enter profile mode, <ESC> quit", flush=True)
        print('.' * 40)
        print_config(1)
        time.sleep(.5)
        print('-' * 40)
        profile_mode()
    elif text == fileModeKey:
        print('Start text file mode, reading file from {}...'.format(
            file_mode_src_file))
        wait(sleepTime)
        try:
            with open(file_mode_src_file, 'r') as f:
                for line in f.read().replace('\r\n', '\n').split('\n'):
                    type_text(line)
                    keyboard.press(Key.enter)
                    time.sleep(.1)
        except FileNotFoundError as e:
            print('File not found, create one')
            with open(file_mode_src_file, 'w') as f:
                f.write('')
        except UnicodeDecodeError as e:
            print('Cannot read file, binary??')
    else:
        text = get_clipboard.get_clipboard() if text == '\\' else text
        if not text or not long_text_input_confirm(text, maxWordCount):
            return
        wait(sleepTime)
        # print(text.strip())
        type_text(text)


def on_release(key):
    global profileMode
    print('{0} release'.format(key))
    if key == Key.esc:
        print('Quit profile mode')
        profileMode = False
        # return False
    # func_key = str(key).replace('\'', '').replace('Key.', '')
    func_key = str(key).split('.')[-1].replace('\'', '')
    print(len(func_key))

    if func_key in keyList:
        wait(sleepTime)
        print('Type {}'.format(configDict[func_key]))
        # keyboard.type(keyList[func_key])
        type_text(configDict[func_key])
    else:
        print('{} is not defined in config'.format(func_key))
        # print(func_key)
        # print('is not in')
        # print(keyList)
    return False


def endless_run():
    while 1:
        try:
            text_to_keystroke()
            flash_caps_lock_light()
            time.sleep(1)
        except KeyboardInterrupt as e:
            confirm = input('Quit?  Y/N: ')
            if confirm.upper() == 'Y':
                sys.exit(1)


profileMode = False
config, profile = toolkit_config.read_config()
keyboard = Controller()
configDict = print_config()
keyList = list(configDict.keys())

sleepTime = float(config['SLEEP_TIME'])
interval = float(config['KEY_PRESS_INTERVAL'])
maxWordCount = int(config['MAX_TEXT_COUNT'])
file_mode_src_file = config['FILE_MODE_SRC_FILE']

if __name__ == '__main__':
    endless_run()   # Endless run
    # text_to_keystroke()  # Run once
    # print(keyList)
    # on_release('4')
    # profile_mode()
    # Collect events until released
    # with Listener(on_release=on_release) as listener:
    #   listener.join()
