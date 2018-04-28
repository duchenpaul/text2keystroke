#!/usr/bin/env python
from pynput.keyboard import Key, Controller, Listener
import time, configparser, os, sys

try:
	config = configparser.ConfigParser()
	config.read('config.ini')

	# Load key config
	key_dict = {}
	for key, value in config['Key'].items():
		key_dict[key] = value
except Exception as e:
	print("Error read config file, check config.ini")

keyboard = Controller()

def print_config():
	for (each_key, each_val) in config['Key'].items():
		print(each_key + ': ' + each_val)


def text_to_keystroke():
	text = input('Convert these text into keystroke:\n')
	if text == 'f':
		# sys.stdout.flush()
		print("Enter function mode", flush=True)
		print_config()
		time.sleep(.5)
		print('-------------------')
		with Listener(on_release=on_release) as listener:
			listener.join()
		return
	print('sleep 3 seconds...')
	time.sleep(3)
	keyboard.type(text)

def on_release(key):
	print('{0} release'.format(key))
	if key == Key.esc:
		print('Stop listener')
		os._exit(0)
	func_key = str(key).replace('Key.', '')
	if func_key in key_dict:
		print("Typing")
		print('sleep 3 seconds...')
		time.sleep(3)
		keyboard.type(key_dict[func_key])
	return False


if __name__ == '__main__':
	while 1:
		text_to_keystroke()
		time.sleep(1)
		# Collect events until released
		# with Listener(on_release=on_release) as listener:
		# 	listener.join()
