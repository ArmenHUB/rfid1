#!/usr/bin/env python

import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import mysql.connector

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

        mydb = mysql.connector.connect(
           host="10.11.1.188",
           user="root",
           passwd="test1234",
           database="Door"
        )

       mycursor = mydb.cursor()

       sql = "SELECT UID FROM cards WHERE UID =  %s"

       val = (UIDcode)

       rows_count = mycursor.execute(sql, val)        
        # Если карта есть в списке
         if rows_count > 0:
        # то дверь открывается
        # предполагается, что замок открывается при подаче на
        # него (на реле, управляющее замком), напряжения
        # т.е. им управляет переключаемое реле
        # т.е. замок открывается при высоком значении пина doorlock
        # при этом, горит зеленая, тухнет красная и пищит динамик

                GPIO.output((green), (1))
                print "Door open"

                # успеть дернуть за 1 секунду
                time.sleep(1)
                GPIO.output((green), (0))

                # потом дверь закрывается, о чем нас извещают
                print "Door closed"

        # А если карты в списке нет, то моргаем и пищим
        else:
                GPIO.output((green), (0))
                print "Unrecognised Card"
