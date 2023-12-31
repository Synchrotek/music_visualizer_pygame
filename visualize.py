import pygame
import pyaudio
import numpy as np

# IF "stereo mix" not avialable 
# then write your availabe mic name in micInpt
micInpt = "stereo mix" 

pygame.init()

width, height = 800, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Real-time Sound Visualization")

p = pyaudio.PyAudio()

for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    if micInpt in info["name"].lower():
        mic_index = i
        break
else:
    raise ValueError("Specified mic not found")

# print(f"mic index : {mic_index}")

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

stream = p.open(format=FORMAT,channels=CHANNELS,
                rate=RATE,input=True,
                input_device_index=mic_index,
                frames_per_buffer=CHUNK)

while True:
    data = stream.read(CHUNK)
    samples = np.frombuffer(data, dtype=np.int16)
    
    screen.fill((0, 0, 0))
    
    y = (samples + 32768) * height / 65536
    
    for i in range(1, len(y)):
        pygame.draw.line(screen, (255, 255, 255), (i - 1, y[i - 1]), (i, y[i]), 1)
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

stream.stop_stream()
stream.close()
p.terminate()
pygame.quit()
