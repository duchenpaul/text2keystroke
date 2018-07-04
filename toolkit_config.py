'''
Retrun the config in dict
'''

import configparser, os.path

config_file = os.path.dirname(os.path.realpath(__file__)) + os.sep + 'config.ini'


def read_config():
	try:
		print('Read config file: ' + config_file )
		configRead = configparser.ConfigParser()
		configRead.read("config.ini")

		config = {}
		profile = {}
		for sectionName in configRead.sections():
			if sectionName == 'config':
				options = [ i.upper() for i in configRead.options(sectionName) ]
				for j in options:
					config[j] = configRead[sectionName][j]

			if sectionName.startswith('Shortcut_'):
				profile[sectionName] = {}
				options = [ i.upper() for i in configRead.options(sectionName) ]
				for j in options:
					profile[sectionName][j] = configRead[sectionName][j]

	except Exception as e:
		print("Error read config file, check config.ini")
		print(e)
		raise
	return config, profile



if __name__ == '__main__':
	config, profile = read_config()
	print(profile)
