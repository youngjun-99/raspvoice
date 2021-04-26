import socket
import pyaudio
import threading
import random
from gpiozero import Button
from time import sleep



FORMAT = pyaudio.paInt16
RATE = 44100
port = random.randrange(49152,65535) #동적포트만 할당
CHUNK = 8192

sound = pyaudio.PyAudio()
  
def callback(in_data, frame_count, time_info, status):
    global conn
    conn.sendall(in_data) 
    return (None, pyaudio.paContinue)

def speaker_thread():
    global data, ostream
    while True:
           if data:
            ostream.write(data[0])
            del data[0]

ostream = sound.open(rate=RATE, channels=1, format=FORMAT, output=True, frames_per_buffer=CHUNK, start=False)

button = Button(18)

while True:
    if button.is_pressed:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            print('서버시작 포트:'+str(port))
            host ='***.***.***.***' #서버ip
            soc.bind((host, port))
            soc.listen(1)
            conn, addr= soc.accept()
            conn1, addr1 = soc.accept()
            ostream.start_stream()
            data = []
            th = threading.Thread(target=speaker_thread)
            th.start()

            while True:
                data.append(conn1.recv(CHUNK))
            ostream.stop_stream()
 else:
    sleep(0.1)
