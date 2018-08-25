#!/usr/bin/env python
# -*- coding: utf-8 -*

import mysql.connector
from mysql.connector import Error
import signal
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

while True:
    input_state = GPIO.input(18)
    if input_state == False:
        print('Button Pressed')
        time.sleep(0.2)
        try:
            conn = mysql.connector.connect(host='localhost',
                                           database='Door',
                                           user='root',
                                           password='test1234')
            if conn.is_connected():
                    sql_insert = "INSERT INTO `action`(`actionID`, `deviceID`) VALUES (1,1)"
                    cursor1 = conn.cursor()
                    cursor1.execute(sql_insert)
                    conn.commit()
                    print('Added')
        except Error as e:
            print(e)
        finally:
            conn.close()        
