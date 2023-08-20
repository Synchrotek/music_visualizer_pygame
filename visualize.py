import pygame
import pyaudio
import numpy as np

pygame.init()

width, height = 800, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Real-time Sound Visualization")

p = pyaudio.PyAudio()

for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    if "stereo mix" in info["name"].lower():
        stereo_mix_device_index = i
        break
else:
    raise ValueError("Stereo Mix device not found")

print(f"stereo_mix_device_index : {stereo_mix_device_index}")

# Set the audio parameters
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# Open the microphone stream
stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=stereo_mix_device_index,
                frames_per_buffer=CHUNK)

# Start the Pygame main loop
running = True
while running:
    # Read audio data from the stream
    data = stream.read(CHUNK)
    # Convert the data to a numpy array
    samples = np.frombuffer(data, dtype=np.int16)
    
    # Clear the Pygame screen
    screen.fill((0, 0, 0))
    
    # Calculate the y-position of each sample
    y = (samples + 32768) * height / 65536
    
    # Draw the sound waves on the Pygame screen
    for i in range(1, len(y)):
        pygame.draw.line(screen, (255, 255, 255), (i - 1, y[i - 1]), (i, y[i]), 1)
    
    # Update the Pygame display
    pygame.display.flip()
    
    # Check for Pygame events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

# Stop and close the microphone stream
stream.stop_stream()
stream.close()

# Terminate Pyaudio
p.terminate()

# Quit Pygame
pygame.quit()
