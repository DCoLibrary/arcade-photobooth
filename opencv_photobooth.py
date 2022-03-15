#sudo apt-get install python3-opencv
#sudo pip3 install python-escpos
#lsusb
#Bus 001 Device 005: ID 04b8:0202 Seiko Epson Corp. Receipt Printer M129C/TM-T70
#receipt = printer.Usb(0x04b8,0x0202)
#https://python-escpos.readthedocs.io/en/latest/user/usage.html
import pygame
from pygame.locals import *
import cv2
import numpy as np
from time import sleep
import picamera
import picamera.array
from escpos import *
from gpiozero import Button
from pathlib import Path

receipt = printer.Usb(0x04b8,0x0202)
#screen_width = 640
#screen_width = 720
screen_width=480
screen_height = 480
pic_dim = (480, 480)

#Set GPIO button variable
picBtn = Button(4)



black = 0,0,0
white = 255,255,255

camera = picamera.PiCamera()
camera.resolution = (screen_width, screen_height)

pygame.init()
pygame.display.set_caption("OpenCV camera stream on Pygame")

#import audio
#https://pythonprogramming.net/adding-sounds-music-pygame/
#https://stackoverflow.com/questions/14845896/pygame-cannot-open-sound-file
#sound_folder = Path("\home\pi\sounds\button.wav")
#btn_folder = sound_folder / "button.wav"
btn_sound = pygame.mixer.Sound("sounds/coin.wav")
sound_three = pygame.mixer.Sound("sounds/three.wav")
sound_two = pygame.mixer.Sound("sounds/two.wav")
sound_one = pygame.mixer.Sound("sounds/one.wav")
sound_click = pygame.mixer.Sound("sounds/camera_snap.wav")
sound_countdown = pygame.mixer.Sound("sounds/countdown.wav")

FPS = 25
fpsClock = pygame.time.Clock()

#Change bg color
#https://www.geeksforgeeks.org/how-to-change-screen-background-color-in-pygame/
bg_color = (66, 135, 245)
screen = pygame.display.set_mode([screen_width, screen_height], pygame.FULLSCREEN)
#screen = pygame.display.set_mode([screen_width, screen_height], pygame.RESIZABLE)
video = picamera.array.PiRGBArray(camera)
font = pygame.font.SysFont('Consolas', 100)
layer1 = pygame.Surface((480, 480))
layer2= pygame.Surface((480, 480))
xCount = 0
camTimer = 4

def countdown():
    #import global variables
    global xCount
    global camTimer
    pygame.mixer.Sound.play(btn_sound)
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(sound_countdown)
    pygame.mixer.music.stop()
    print("loop started " + str(xCount) +" , " + str(camTimer))
    while camTimer == 4:
        print("camtimer 3 " + str(xCount) +" , " + str(camTimer))
        if xCount < 26:
            print("camtimer 3 - xcount" + str(xCount) +" , " + str(camTimer))
            screen.fill(bg_color)
            bg_image = get_frame()
            dispTime = camTimer - 1
            label = font.render(str(dispTime), 1, white)
            labelpos = label.get_rect()
            labelpos.centerx = screen.get_rect().centerx
            labelpos.centery = screen.get_rect().centery
            screen.blit(bg_image, (0,0))
            screen.blit(label, labelpos)
            pygame.display.flip()
            xCount += 1
            fpsClock.tick(FPS)
        else:
            xCount = 0
            camTimer -= 1
            print("camtimer 3 - reset " + str(xCount) +" , " + str(camTimer))
    while camTimer == 3:
        print("camtimer 2 " + str(xCount) +" , " + str(camTimer))

        if xCount < 26:
            print("camtimer 2 - xcount" + str(xCount)+ " , " + str(camTimer))
            screen.fill(bg_color)
            bg_image = get_frame()
            dispTime = camTimer - 1
            label = font.render(str(dispTime), 1, white)
            labelpos = label.get_rect()
            labelpos.centerx = screen.get_rect().centerx
            labelpos.centery = screen.get_rect().centery
            screen.blit(bg_image, (0,0))
            screen.blit(label, labelpos)
            pygame.display.flip()
            xCount += 1
            fpsClock.tick(FPS)
        else:
            xCount = 0
            camTimer -= 1
            print("camtimer 2 - reset " + str(xCount) +" , " + str(camTimer))
    while camTimer == 2:
        print("camtimer 1 " + str(xCount) +" , " + str(camTimer))
        if xCount < 26:
            print("camtimer 1 - xcount " + str(xCount) +" , " + str(camTimer))
            screen.fill(bg_color)
            bg_image = get_frame()
            dispTime = camTimer - 1
            label = font.render(str(dispTime), 1, white)
            labelpos = label.get_rect()
            labelpos.centerx = screen.get_rect().centerx
            labelpos.centery = screen.get_rect().centery
            screen.blit(bg_image, (0,0))
            screen.blit(label, labelpos)
            pygame.display.flip()
            xCount += 1
            fpsClock.tick(FPS)
        else:
            xCount = 0
            camTimer -= 1
            print("camtimer 1 - reset" + str(xCount) +" , " + str(camTimer))
    while camTimer == 1:
        print("camtimer 0 " + str(xCount) +" , " + str(camTimer))
        
        print("taking picture!" + str(xCount) + ", " + str(camTimer))
        pygame.mixer.Sound.play(sound_click)
        pygame.mixer.music.stop()
        bg_image = get_raw()
        take_pic(bg_image)
        print_pic()
        return
    while camTimer == 0:
        print("taking picture!" + str(xCount) + ", " + str(camTimer))
        pygame.mixer.Sound.play(sound_click)
        pygame.mixer.music.stop()
        bg_image = get_raw()
        take_pic(bg_image)
        print_pic()
        return
    return
    
def take_pic(img_still):

    brt=40
    img_still_bw = cv2.resize(img_still, pic_dim)
    img_still_bw = cv2.cvtColor(img_still, cv2.COLOR_BGR2GRAY)
    img_still_bw = cv2.rotate(img_still_bw, cv2.ROTATE_90_CLOCKWISE)
    #Adjust brightness
    #https://stackoverflow.com/questions/50474302/how-do-i-adjust-brightness-contrast-and-vibrance-with-opencv-python
    img_still_bw[img_still_bw < 255-brt] += brt
    filename = 'cvImageBW.jpg'
    cv2.imwrite(filename, img_still_bw)
def print_pic():
    receipt.text("Durham County Library \n")
    receipt.image("cvImageBW.jpg")
    receipt.cut()
def get_frame():
    for frameBuf in camera.capture_continuous(video, format ="rgb", use_video_port=True):
        frame = np.rot90(frameBuf.array)
        video.truncate(0)
        img = pygame.surfarray.make_surface(frame)
        #screen.fill([0,0,0])
        return img
def get_raw():
    for frameBuf in camera.capture_continuous(video, format ="rgb", use_video_port=True):
        frame = np.rot90(frameBuf.array)
        video.truncate(0)
        img = pygame.surfarray.make_surface(frame)
        #screen.fill([0,0,0])
        return frame

try:
    while True:
   
        camTimer = 4
        cam_image = get_frame()
        screen.fill(bg_color)
        screen.blit(cam_image, (0,0))
        pygame.display.update()
        #check to see if GPIO button is pressed
        #https://gpiozero.readthedocs.io/en/stable/recipes.html
        if picBtn.is_pressed:
                print("button success")
                countdown()
        for event in pygame.event.get():
            #if event.type == pygame.KEYDOWN:
            #https://www.pygame.org/docs/ref/key.html
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    countdown()
                    #take_pic(frame)
                    #print_pic()
                elif event.key == pygame.K_ESCAPE:
                        raise KeyboardInterrupt
except (KeyboardInterrupt, SystemExit):
    pygame.quit()
    cv2.destroyAllWindows()