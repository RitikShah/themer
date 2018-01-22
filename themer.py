##############################################################
# 						START OF FILE 						 #
##############################################################
from shutil import get_terminal_size

'''
Script made by: shraavan97
01/15/18

Aids in theme making for Shulker Box

'''
print(chr(27) + "[2J")

with open('template.mcfunction', 'r') as file:
	template = file.read().split('\n')

with open('themer.config', 'r') as file:
	templateconfig = file.read().split('\n')

with open('template-helper.mcfunction', 'r') as file:
	template_helper = file.read().split('\n')

version = templateconfig.pop(0)

#############################################################
# | | | | | | | | | | | | | | | | | | | | | | | | | | | | | #
#############################################################

def convert_to_dict(themeconfig):
	themedict = {}
	for item in themeconfig:
		if item == '':
			continue
		print(item)
		templist = item.split('=')
		themedict[templist[0]] = templist[1]
	return themedict

#############################################################

def check_version(themeconfig):
	#global version
	if themeconfig[0] != version:
	  	return False
	else:
		return True

#############################################################

def save_config(filename, themedict):
	global template
	global templateconfig
	print('Saving ' + filename + '.config')

	themeconfig = ''.join('{0}={1}\n'.format(key, val) for key, val in themedict.items())
	themeconfig = (version + '\n') + themeconfig

	with open('configs/' + filename + '.config', 'w') as file:
		file.write(themeconfig)

	print('Config Saved! Saving config file to ' + filename + '.config\n')
	return

#############################################################

def save_theme(filename, themedict, template):
	global templateconfig
	print('Saving ' + filename + '.mcfunction')

	if themedict['> spruce_axis'] == 'false':
		template[80] = template_helper[0]
		template[81] = template_helper[1]
		template[82] = template_helper[2]
	elif themedict['> oak_axis'] == 'false':
		template[90] = template_helper[3]
		template[91] = template_helper[4]
		template[92] = template_helper[5]

	template = '\n'.join(template).format_map(themedict)

	with open('themes/' + filename + '.mcfunction', 'w') as file:
		file.write(template)

	print('Theme Saved! Saving theme file to ' + filename + '.mcfunction\n')

	return

#############################################################
# | | | | | | | | | | | | | | | | | | | | | | | | | | | | | #
#############################################################

def help():
	print('-' * get_terminal_size()[0])
	print('''
			Welcome to the Shulker Theming Program
			With this, you can easily create themes for the dungeon minigame
		

			There are two main files that store the default themeing blocks and commands:
				template.mcfunction
				themer.config
			
			Only edit these files if you are adding commands or theming blocks

			Option 2:
			To make a new theme, enter a valid minecraft id for each theme block
			These themes are then stored in a .config file along with your requested .mcfunction file

			These config files can also be manipulated

			Option 3-4:
			Config files store the theming blocks and their values
			Each theme has a cooresponding theming config that holds the 'theme'
			
			With Option 3, you can edit an old config, and automatically update your theme
			With Option 4, you can convert a config into a .mcfunction theme
			
			Option 5:
			As we develop the Shulker Box, we will probably add and change blocks.
			This program allows you to change the template.mcfunction and themer.config in order for you
				to add and change commands and blocks.
			Run this option after making changes to automatically update old themes.

			Returning to main menu
			''')
	print('-' * get_terminal_size()[0])
	input()
	main()

############################################################

def new_theme():
	global template
	global templateconfig
	filename = input('What is this theme\'s name: ')

	print('\n')

	input('''
		Program is ready to set theme blocks!\n
		Just enter the cooresponding mc valid block name next to the key.\n
		Empty spots are considered as air to prevent bugs.\n
		> axis:  require a true or false\n
		Press enter when you are ready.
		''')

	print('\n')
	print('-' * get_terminal_size()[0])
	print('\n')

	themedict = {}

	for item in templateconfig:
		value = input(item + ': ')
		if value == '':
			value = 'air'
		themedict[item] = value

	print('\n')
	print('-' * get_terminal_size()[0])

	save_config(filename, themedict)

	save_theme(filename, themedict, template)

	print('Program has executed successfully. Goodbye!')

#############################################################

def edit_theme():
	global template
	global templateconfig
	print('-' * get_terminal_size()[0])

	filename = input('What theme would you like to edit: ')

	with open('configs/' + filename + '.config', 'r') as file:
		themeconfig = file.read().split('\n')

	if check_version(themeconfig) == True:
		print('Config is not latest version.\nQuiting program')
		return

	themeconfig.pop(0)

	print('Current Config: \n')
	themedict = convert_to_dict(themeconfig)

	print('\n')
	
	while True:
		changekey = input('Which key would you like to change (leave empty when done): ')
		if changekey == '':
			break
		changevalue = input(changekey + ": ")
		themedict[changekey] = changevalue

	save_config(filename, themedict)

	save_theme(filename, themedict, template)

	print('Program has executed successfully. Goodbye!')

#############################################################

def convert_config():
	global template
	global templateconfig
	print('-' * get_terminal_size()[0])

	filename = input('What config would you like to convert: ')

	with open('configs/' + filename + '.config', 'r') as file:
		themeconfig = file.read().split('\n')

	if check_version(themeconfig) == True:
		print('Config is not latest version.\nQuiting program')
		return

	themeconfig.pop(0)

	print('Converting to Config: \n')
	themedict = convert_to_dict(themeconfig)

	save_theme(filename, themedict, template)

	print('Program has executed successfully. Goodbye!')

#############################################################

def update_themes():
	import os
	import glob

	global template
	global templateconfig
	global version

	print('-' * get_terminal_size()[0])

	confirm = input('Updating themes will change old files.\
		\nPlease confirm with \'yes\' that you have made backups\n')
	if confirm != 'yes':
		return

	print('Updating Files: ')

	path = 'configs/'
	listing = os.listdir(path)

	for infile in glob.glob(os.path.join(path, '*.config')):
		with open(infile, 'r') as file:
	  		themeconfig = file.read().split('\n')

		if check_version(themeconfig) == True:
			print('Skipping ' + infile + '. Already latest version.')
			continue

		themeconfig.pop(0)
		themedict = convert_to_dict(themeconfig)
		
		tempthemedict = {}

		for key in templateconfig:
			try:
				tempthemedict[key] = themedict[key]
			except KeyError:
				print(key + ' does not exist in old config. Inserting air to avoid errors.')
				tempthemedict[key] = 'air'

		newthemeconfig = ''.join('{0}={1}\n'.format(key, val) for key, val in tempthemedict.items())

		newthemeconfig = (version + '\n') + newthemeconfig
		
		print('Updating Config File: ' + infile[8:])
		
		with open(infile, 'w') as file:
			file.write(newthemeconfig)

		print('Saving Theme File: ' + infile[8:])

		save_theme(infile[8:].split('.')[0], themedict, template)

	#### End File Loop ####
	
	print('All Files Updated!')

#############################################################

def main():
	global template
	global templateconfig
	print('-' * get_terminal_size()[0])

	print('''
		Welcome to the Shulker Box Themer Program.
		Version {}
		Created by: shraavan97
		'''.format(version))

	print('-' * get_terminal_size()[0])
	
	print('''
		Enter a number to call a function:
		1) Help
		2) Create New Theme
		3) Edit Old Theme (requires config)
		4) Convert Config to Theme
		5) Update Old Themes
		''')

	print('-' * get_terminal_size()[0])
	print('\n')

	userinput = input('> ')
	print('\n')

	if userinput == '1':
		help()
	elif userinput == '2':
		new_theme()
	elif userinput == '3':
		edit_theme()
	elif userinput == '4':
		convert_config()
	elif userinput == '5':
		update_themes()
	else:
		print('Invalid Option. Terminating program.\n')

#############################################################
# | | | | | | | | | | | | | | | | | | | | | | | | | | | | | #
#############################################################

main()

#############################################################
# 						END OF FILE 						#
#############################################################