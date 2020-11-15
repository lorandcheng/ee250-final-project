# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# 
# Author: Lorand Cheng https://github.com/lorandcheng
# Date: Nov 15, 2020
# Project: USC EE250 Final Project, Morse Code Translator and Messenger
# 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Grovepi pins
BUTTON = 2 #D2
LED = 3 #D3
BUZZER = 4 #D4

# Define press lengths (s)
DASH = 0.3
SEND = 3

# Define pause lengths (s)
END = 0.7
SPACE = 3

# Server info
HOST = '35.239.226.249'
PORT = '4200'
SERVER = f'{HOST}:{PORT}'