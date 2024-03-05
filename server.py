import socket
from  threading import Thread
from pynput.mouse import Button, Controller
from screeninfo import get_monitors
#import autopy
import pygetwindow as gw


from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen

import socket
from  threading import Thread
import json

SERVER = None
PORT = 8000
IP_ADDRESS = input("Enter your computer IP ADDR : ").strip()
screen_width = None
screen_height = None

keyboard = Controller()

def setup():
    print("\n\t\t\t\t\t*** Welcome To Remote Keyboard ***\n")


    global SERVER
    global PORT
    global IP_ADDRESS


    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))

    SERVER.listen(10)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMMING CONNECTIONS...\n")

    getDeviceSize()
    acceptConnections()

def acceptConnections():
    global SERVER

    while True:
        client_socket, addr = SERVER.accept()

        print(f"Connection established with {client_socket} : {addr}")

        thread1 = Thread(target = recvMessage, args=(client_socket,))
        thread1.start()

def getDeviceSize():
    global screen_width
    global screen_height
    for m in get_monitors():
        screen_width = int(str(m).split(",")[2].strip().split('width=')[1])
        screen_height = int(str(m).split(",")[3].strip().split('height=')[1])


def recvMessage(client_socket):
    global keyboard

    while True:
        try:
            message = client_socket.recv(2048).decode()
            if(message):
                new_message  = eval(message)
                if(new_message["data"] == 'left_click'):
                    keyboard.press(Button.left)
                    keyboard.release(Button.left)
                elif(new_message["data"] == 'right_click'):
                    keyboard.press(Button.right)
                    keyboard.release(Button.right)
                else:
                    xpos =  new_message["data"][0] * screen_width
                    ypos = screen_height * (1 - (new_message["data"][1] - 0.2) / 0.6 )
                    keyboard.position = (int(xpos), int(ypos))

        except Exception as error:
            pass

def acceptConnections():
    global SERVER

    while True:
        client_socket, addr = SERVER.accept()

        print(f"Connection established with {client_socket} : {addr}")

        thread1 = Thread(target = recvMessage, args=(client_socket,))
        thread1.start()
