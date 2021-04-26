import socket
import pyaudio
import threading
from gpiozero import Button
from time import sleep


FORMAT = pyaudio.paInt16
RATE = 44100
CHUNK = 8192

sound = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    global soc1
    soc1.sendall(in_data)
    return (None, pyaudio.paContinue)

istream = sound.open(rate=RATE, channels=1, format=FORMAT, input=True,frames_per_buffer=CHUNK, start=False, stream_callback=callback)

button = Button(18)

while True:
    if button.is_pressed:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as soc1:
                print('클라이언트 시작')
                host = '***.***.***.***'  #서버ip
                for port in range(49152,65535): # 동적포트 내에서만
                    try:
                        print('연결 시도 중인 포트 :'+str(port))
                        soc.connect((host, port))
                        soc1.connect((host, port))
                        print('Port:' + str(port) + '서버접속')
                        break
                    except:pass
                istream.start_stream()
                data = []

                while True:
                    data.append(soc.recv(CHUNK))
                    pass
                istream.stop_stream()
 else:
    sleep(0.1)
