# Class design van programma (schakeling Docam)

import bluetooth
from datetime import datetime           # Datetime
from DbClass import DbClass
import mysql.connector as connector
import os
from picamera import PiCamera           # Pi camera-module
import pygame                           # Afspelen audio via bluetooth-speaker
import RPi.GPIO as GPIO                 # GPIO
from subprocess import call
import sys
import time                             # Time

class PIRCamera():

    camera = PiCamera()

    def __init__(self, pir, led, knop, speaker):
        self.__pir = pir
        self.__led = led
        self.__knop = knop
        self.__speaker = speaker

        self.__video_duration = 30

        self.__aangebeld = False
        self.__motion_detected = False

        self.__ringtone_name = ""

        self.__setup()
        self.__bluetoothScan()

        self.__framerate = "30"

    def __setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.__pir, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.setup(self.__knop, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(self.__led, GPIO.OUT)
        GPIO.setup(self.__speaker, GPIO.OUT)
        GPIO.add_event_detect(self.__knop, GPIO.RISING, callback=self.knop_callback, bouncetime=200)
        GPIO.add_event_detect(self.__pir, GPIO.RISING, callback=self.pir_callback, bouncetime=200)

    def knop_callback(self, channel):
        if (GPIO.input(self.__knop)):
            self.__aangebeld = True
            pygame.mixer.init()
            pygame.mixer.music.load("/home/pi/Music/Ringtones/" + self.__ringtone_name + ".mp3")
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy() == True:
                continue

    def pir_callback(self, channel):
        if (GPIO.input(self.__pir)):
            self.takePicture()

    def __bluetoothScan(self):
        call('killall -9 pulseaudio', shell=True)
        time.sleep(3)
        call('pulseaudio --start', shell=True)
        time.sleep(2)
        call('~/scripts/autopair', shell=True)
        time.sleep(2)
        call('pacmd set-default-sink bluez_sink.30_21_36_04_04_6C', shell=True)

    def getStatusMotionSensor(self):
        statusMotionSensor = GPIO.input(self.__pir)
        if (statusMotionSensor == 0):
            self.__motion_detected = False
        elif (statusMotionSensor == 1):
            self.__motion_detected = True

    def cameraSettings(self, default_width, default_height, brightness, framerate=30):
        PIRCamera.camera.resolution = (default_width, default_height)
        PIRCamera.camera.brightness = brightness
        PIRCamera.camera.framerate = framerate
        self.__framerate = framerate

    def setRingtone(self, ringtone_name):
        self.__ringtone_name = ringtone_name

    def setVideoDuration(self, video_duration):
        self.__video_duration = video_duration

    def takePicture(self):
        status_sensor = GPIO.input(self.__pir)
        if status_sensor == 0:
            GPIO.output(self.__led, GPIO.LOW)
        elif status_sensor == 1:
            self.__motion_detected = True
            filename = "image-" + str(datetime.now().strftime("%d-%m-%Y_%H.%M.%S"))
            print("Infrarood gedetecteerd, foto aan het nemen, even geduld")
            GPIO.output(self.__led, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(self.__led, GPIO.LOW)
            PIRCamera.camera.start_preview()
            time.sleep(2)
            PIRCamera.camera.capture('/home/pi/examen/datacom/Pycharm/static/img/photos/' + filename + '.jpg')
            print("Foto genomen")
            filesize = round(os.path.getsize('/home/pi/examen/datacom/Pycharm/static/img/photos/' + filename + '.jpg') / 1024, 1)
            DB_layer = DbClass()
            time.sleep(10)
            if (self.__aangebeld == True):
                DB_layer.addMedia(filename + '.jpg', filesize, True)
            else:
                DB_layer.addMedia(filename + '.jpg', filesize, False)
            time.sleep(20)
            self.__motion_detected = False
            self.__aangebeld = False

    def recordVideo(self):
        status_sensor = GPIO.input(self.__pir)
        if status_sensor == 0:
            GPIO.output(self.__led, GPIO.LOW)
        elif status_sensor == 1:
            filename = "video-" + str(datetime.now().strftime("%d-%m-%Y_%H.%M.%S"))
            print("Infrarood gedetecteerd, video aan het opnemen, even geduld")
            self.__motion_detected = True
            GPIO.output(self.__led, GPIO.HIGH)
            time.sleep(0.5)
            GPIO.output(self.__led, GPIO.LOW)
            PIRCamera.camera.start_recording('/home/pi/Videos/' + filename + '.h264')
            time.sleep(self.__video_duration)
            PIRCamera.camera.stop_recording()
            cmd = "MP4Box -add /home/pi/Videos/" + filename + ".h264:fps=" + str(
                self.__framerate) + "-new /home/pi/examen/datacom/Pycharm/static/img/videos/" + filename + ".mp4"
            call([cmd], shell=True)
            print("Video opgenomen")
            filesize = round(os.path.getsize('/home/pi/examen/datacom/Pycharm/static/img/photos/' + filename + '.mp4') / 1024, 1)
            DB_layer = DbClass()
            if (self.__aangebeld == True):
                DB_layer.addMedia(filename + '.mp4', filesize, True)
            else:
                DB_layer.addMedia(filename + '.mp4', filesize, False)
            call('rm /home/pi/Videos/' + filename + '.h264', shell=True)
            time.sleep(3)
            self.__motion_detected = False

