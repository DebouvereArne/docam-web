import sys
import bluetooth
import pygame                           # Afspelen audio via bluetooth-speaker
import RPi.GPIO as GPIO                 # GPIO
import time                             # Time
from picamera import PiCamera           # Pi camera-module
from datetime import datetime           # Datetime
from subprocess import call
import mysql.connector as connector

class PIRCamera():

    camera = PiCamera()

    def __init__(self, pir, led, knop, speaker):
        self.__pir = pir
        self.__led = led
        self.__knop = knop
        self.__speaker = speaker

        self.__setup()
        self.__bluetoothScan()

    def __setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.input(self.__pir, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(self.__knop, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(self.__led, GPIO.OUT)
        GPIO.setup(self.__speaker, GPIO.OUT)

    def __bluetoothScan(self):
        call('killall -9 pulseaudio', shell=True)
        time.sleep(3)
        call('pulseaudio --start', shell=True)
        time.sleep(2)
        call('~/scripts/autopair', shell=True)
        time.sleep(2)
        call('pacmd set-default-sink bluez_sink.30_21_36_04_04_6C', shell=True)

    def cameraSettings():
        PIRCamera.camera.resolution = (default_width, default_height)
        PIRCamera.camera.brightness = brightness