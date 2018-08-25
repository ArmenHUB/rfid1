#!/usr/bin/env python
# -*- coding: utf-8 -*

import mysql.connector
from mysql.connector import Error
import MFRC522
import signal
import mysql.connector
import RPi.GPIO as GPIO
import time


lock = 8


# Настройка портов вывода
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(lock,GPIO.OUT)
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

continue_reading = True

def end_read(signal, frame):  # что делать, если программу прервать и как её прервать
    global continue_reading
    print "Ctrl+C captured, ending read."
    continue_reading = False
    GPIO.cleanup()

# Create an object of the class MFRC522 (??)
MIFAREReader = MFRC522.MFRC522()

while continue_reading:
    # Сканируем карты - считываем их UID
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # Если карту удалось считать, пишем "карта найдена"
    if status == MIFAREReader.MI_OK:
        print "Card detected"

    # Считываем UID карты
    (status, uid) = MIFAREReader.MFRC522_Anticoll()

    # Если считали UID, то идем дальше
    if status == MIFAREReader.MI_OK:
        # выводим UID карты на экран
        UIDcode = "%s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3])
        try:
            conn = mysql.connector.connect(host='localhost',
                                           database='Door',
                                           user='root',
                                           password='test1234')
            if conn.is_connected():
                cursor = conn.cursor()
                sql = "SELECT `userID` FROM `cards` WHERE `UID` = '%s'" % (UIDcode)
                cursor.execute(sql)
                row = cursor.fetchone()
                while row is not None:
                    row = cursor.fetchone()
                    sql_insert = "INSERT INTO `action`(`actionID`, `deviceID`) VALUES (1,1)"
                    cursor1 = conn.cursor()
                    cursor1.execute(sql_insert)
                    GPIO.output(lock, GPIO.HIGH)
                    print "Door open"
                    time.sleep(2)
                    print "Door close"
                    GPIO.output(lock, GPIO.LOW)
        except Error as e:
            print(e)
        finally:
            conn.close()
    while True:
    input_state = GPIO.input(18)
    if input_state == False:
        print('Button Pressed')
        time.sleep(0.2)    
