#!/usr/bin/env python
# -*- coding: utf-8 -*

import RPi.GPIO as GPIO
import MFRC522
import signal
import time
#import mysql.connector

#red = 11
green = 18
# speaker = 16
# doorlock = 12


#Настройка портов вывода
GPIO.setmode(GPIO.BOARD) # Это значит, что считаем пины по порядку с левого верхнего (3v3 - первый)
#GPIO.setup(red, GPIO.OUT, initial=1) # Устанавливаем пин 18 на вывод
GPIO.setup(green, GPIO.OUT, initial=0) # тоже самое с пином 11
#GPIO.setup(speaker, GPIO.OUT, initial=0) # пин 16
#GPIO.setup(doorlock, GPIO.OUT, initial=0) # пин 12

continue_reading = True

def end_read(signal,frame): # что делать, если программу прервать и как её прервать
	global continue_reading
	print "Ctrl+C captured, ending read."
	continue_reading = False
	GPIO.cleanup()

# Create an object of the class MFRC522 (??)
MIFAREReader = MFRC522.MFRC522()

while continue_reading:

# Сканируем карты - считываем их UID
	(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

	# Если карту удалось считать, пишем "карта найдена"
	if status == MIFAREReader.MI_OK:
		print "Card detected"

	# Считываем UID карты
	(status,uid) = MIFAREReader.MFRC522_Anticoll()

	# Если считали UID, то идем дальше
	if status == MIFAREReader.MI_OK:
		# выводим UID карты на экран
		UIDcode = str(uid[0])+str(uid[1])+str(uid[2])+str(uid[3])
		print UIDcode
