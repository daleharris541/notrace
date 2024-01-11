#No Trace
#Version 0.1
#Created by Dale Harris
#January 20th, 2021
#Description: 
#Generate random first/last name, username, password, and generate alias email

import random
import string
import secrets
import atexit #used to properly catch any escape of the program to ensure options are saved or wiped
import json

#Setup variables (to pull from txt file for permanent settings)
if ('options.ini'):
	with open("options.ini", "r") as configfile:
		config = json.load(configfile)
# read values from options.ini file
if (config):
	preferred_first = config["preferred_first"]
	preferred_last = config['preferred_last']
	preferred_email = config['preferred_email']
	preferred_animal = config['preferred_animal']
	preferred_adjective = config['preferred_adjective']
	preferred_username = config['preferred_username']
	preferred_vault = config['preferred_vault']
	save_preferences = config['save_preferences']
	wipe_options_upon_exit = config['wipe_options_upon_exit']
else:
	print("No config file found... loading defaults")
	save_preferences = True

#instantiate variables
choice = ""
domain = ""

# Function to properly close out the app
def goodbye(save_preferences,wipe_options_upon_exit):
	print("Performing cleanup")
	if (save_preferences):
		config['preferred_first'] = preferred_first
		config['preferred_last'] = preferred_last
		config['preferred_email'] = preferred_email
		config['preferred_animal'] = preferred_animal
		config['preferred_adjective'] = preferred_adjective
		config['preferred_username'] = preferred_username
		config['preferred_vault'] = preferred_vault
		with open("options.ini","w") as configfile:
			json.dump(config, configfile)
	else:
		config['preferred_first'] = "wiped"
		config['preferred_last'] = "clean"
		config['preferred_email'] = ""
		config['preferred_animal'] = ""
		config['preferred_adjective'] = ""
		config['preferred_username'] = ""
		config['preferred_vault'] = ""
		with open("options.ini","w") as configfile:
			json.dump(config, configfile)
	return


#register atexit function to 1) save the options 2) delete the options
atexit.register(goodbye,save_preferences,wipe_options_upon_exit)

#Read in adjectives text file
file = open("adjectives.txt")
adjectives = file.read().splitlines()
file.close()

#Read in animals text file
file = open("animals.txt")
animals = file.read().splitlines()
file.close()

#Read in surnames text file
file = open("firstnames.txt")
firstnames = file.read().splitlines()
file.close()

#Read in surnames text file
file = open("surnames.txt")
surnames = file.read().splitlines()
file.close()

#Randomly Generate Username
def username():
	#grab an adjective
	if (preferred_adjective == ""):
		adjective = adjectives[random.randint(0,len(adjectives)-1)]
	else:
		adjective = preferred_adjective

	#parse first letter of selected adjective
	start_letter = adjective[:1].lower()
	matching_animals = [x for x in animals if x[0].lower() == start_letter]
	animal = matching_animals[random.randint(0,len(matching_animals)-1)]
	username = adjective+animal+str(random.randint(000,999))
	#Grab an animal matching the same first letter
	#print("Username: ",str(adjective,animal))
	return username

def last():
	#randomly grab from list of surnames.txt
	if (preferred_last == ""):
		last = surnames[random.randint(0,len(surnames)-1)]
	else:
		last = preferred_last
	return last

def first():
	#randomly grab from list of firstnames.txt
	if (preferred_first == ""):
		first = firstnames[random.randint(0,len(firstnames)-1)]
	else:
		first = preferred_last
	return first

#Create Menu to loop until exit
def menu():
	print("1) Generate new Alias")
	print("2) Supply your own Adjective")
	print("3) Change preferred Email Suffix")
	print("Q) Quit")
	print("")
	print("Default (hit Enter)")
	choice=input()
	return choice

def password():
	# Feel free to use any type of password creation module you'd like
	# password is returned but not assigned to a global variable
	# and will be discarded/replaced and not logged anywhere
	alphabet = string.ascii_letters + string.digits
	while True:
		password = ''.join(secrets.choice(alphabet) for i in range(10))
		if (any(c.islower() for c in password)
			and any(c.isupper() for c in password)
			and sum(c.isdigit() for c in password) >= 3):
			return password

while choice.lower() != 'q':
	choice = menu()
	if choice == "1":
		print("Username: " + username())
		print("First Name: " + first())
		print("Last Name: " + last())
		print("Aliased Email Address: <website>" + preferred_email)
		print("password: " + password())
		print("")
		print("")
	elif choice == "2":
		preferred_adjective = input("What is your preferred Adjective? Hit Enter if none:")
		print("")
		print("Every new alias will include the adjective " + preferred_adjective + ".")
		print("")
	elif choice == "3":
		preferred_email = input("What is your email suffix (e.g. @xyz.anonaddy.com)")
	elif choice.lower() == "q":
		choice = "q"
	elif choice.lower() == "":
		print("Username: " + username())
		print("First Name: " + first())
		print("Last Name: " + last())
		print("Aliased Email Address: <website>" + preferred_email)
		print("password: " + password())
		print("")
		print("")
		choice = "1"
	else:
		print("Input not allowed, try again")
		choice = ""