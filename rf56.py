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

lock = 8


# Настройка портов вывода1
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(lock,GPIO.OUT)
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
        print UIDcode
        try:
            conn = mysql.connector.connect(host='localhost', database='Door', user='root', password='test1234')
            if conn.is_connected():
                cursor = conn.cursor()
                sql = "SELECT `userID` FROM `cards` WHERE `UID` = '%s'" % (UIDcode)
                cursor.execute(sql)
                row = cursor.fetchone()
                while row is not None:
                    GPIO.output(lock, GPIO.HIGH)
                    print "Door open"
                    time.sleep(2)
                    print "Door close"
                    GPIO.output(lock, GPIO.LOW)
                    conn1_1 = mysql.connector.connect(host='localhost', database='Door', user='root', password='test1234')
                    if conn1_1.is_connected():
                        cursor1_1 = conn1_1.cursor()
                        sql_insert_log = "INSERT INTO `log`(`userID`, `deviceID`) VALUES (%s,%s)"
                        val = (row[0], "1")
                        cursor1_1.execute(sql_insert_log, val)
                        conn1_1.commit()
                        time.sleep(0.2)
                        row = None
        except Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
