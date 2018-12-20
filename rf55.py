#!/usr/bin/env python
# -*- coding: utf-8 -*

import mysql.connector
from mysql.connector import Error
import MFRC522
import signal
import mysql.connector
import RPi.GPIO as GPIO
import time
import os


bell = 12
lock = 8

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(lock,GPIO.OUT)
GPIO.setup(bell, GPIO.IN, pull_up_down=GPIO.PUD_UP)
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

    input_state = GPIO.input(bell)
    if input_state == False:
        try:
            conn = mysql.connector.connect(host='localhost', database='Door', user='root', password='test1234')
            if conn.is_connected():
                    sql_insert = "INSERT INTO `action`(`actionID`, `deviceID`) VALUES (1,1)"
                    cursor1 = conn.cursor()
                    cursor1.execute(sql_insert)
                    conn.commit()
                    print "bell pressed"                   
        except Error as e:
            print(e)
        finally:
            cursor1.close()
            conn.close()

    try:
        conn1 = mysql.connector.connect(host='localhost', database='Door', user='root', password='test1234')
        if conn1.is_connected():
                sql_open = "SELECT * FROM `action` WHERE actionID = 2"
                cursor = conn1.cursor()
                cursor.execute(sql_open)
                row = cursor.fetchone()
                while row is not None:
                    GPIO.output(lock, GPIO.HIGH)
                    print "Door open"
                    time.sleep(2)
                    print "Door close"
                    GPIO.output(lock, GPIO.LOW)
                    conn11 = mysql.connector.connect(host='localhost', database='Door', user='root', password='test1234')
                    if conn11.is_connected():
                        cursor11 = conn11.cursor()
                        sql_remove = "DELETE  FROM `action` WHERE actionID = 2"
                        cursor11.execute(sql_remove)
                        conn11.commit()
                        row = None

    except Error as e:
        print(e)
    finally:
        conn1.close()
