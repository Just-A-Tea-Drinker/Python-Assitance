
#code adapted from :https://blenderartists.org/t/circle-sound-visualizer-all-with-python/652850
import sys
import os
import numpy as np
import librosa
import math
import os
import sounddevice as sd
import soundfile as sf

#GETTING RID OF THE WELCOME TO PYGAME MSGS
# Save the current stdout so we can restore it later
original_stdout = sys.stdout

# Redirect stdout to null
sys.stdout = open(os.devnull, 'w')
import pygame
pygame.init()
sys.stdout.close()
sys.stdout = original_stdout

MAX_RANGE = 360
RADIUS = 200
WINDOW_SIZE = (800, 800)
CENTER = (WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2)
DECAY_RATE = 0.1  # Rate at which the bars shrink after audio ends
BACKGROUND_COLOR = (32,32,32)
SONG_PATH = r"buffer\output.wav"
def setup():
    # Pygame setup
  
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Audio Visualizer")
    clock = pygame.time.Clock()
    running = True
    start_ticks = pygame.time.get_ticks()
    last_mod_time = os.path.getmtime(r"buffer\output1.wav")
    # Load audio
    y, sr = librosa.load(SONG_PATH, sr=None)
    hop_length = 512
    n_fft = 2048

    # Calculate the Short-Time Fourier Transform (STFT)
    stft = np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop_length))
    frequencies = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
    times = librosa.frames_to_time(np.arange(stft.shape[1]), sr=sr, hop_length=hop_length, n_fft=n_fft)

    # Normalize the STFT results
    stft_db = librosa.amplitude_to_db(stft, ref=np.max)

    # Initialize angles for the bars
    step_angle = (2 * math.pi) / MAX_RANGE
    angles = [i * step_angle for i in range(MAX_RANGE)]
    # Calculate the duration of the audio file
    audio_duration = 0
    total_frames = len(times)

    return screen,clock,running,start_ticks,last_mod_time,y,sr,hop_length,n_fft,stft,frequencies,times,stft_db,step_angle,angles,audio_duration,angles,total_frames
 
def run(ev):
    screen,clock,running,start_ticks,last_mod_time,y,sr,hop_length,n_fft,stft,frequencies,times,stft_db,step_angle,angles,audio_duration,angles,total_frames =setup()
    ev.set()
    

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        ##checking whether or not a file has been changed to check/start
    
        current_mod_time = os.path.getmtime(r"buffer\output1.wav")
        if current_mod_time != last_mod_time:
            start_ticks = pygame.time.get_ticks()


            # Load audio
            y, sr = librosa.load(SONG_PATH, sr=None)
            hop_length = 512
            n_fft = 2048

            # Calculate the Short-Time Fourier Transform (STFT)
            stft = np.abs(librosa.stft(y, n_fft=n_fft, hop_length=hop_length))
            frequencies = librosa.fft_frequencies(sr=sr, n_fft=n_fft)
            times = librosa.frames_to_time(np.arange(stft.shape[1]), sr=sr, hop_length=hop_length, n_fft=n_fft)

            # Normalize the STFT results
            stft_db = librosa.amplitude_to_db(stft, ref=np.max)

            step_angle = (2 * math.pi) / MAX_RANGE
            angles = [i * step_angle for i in range(MAX_RANGE)]

            audio_duration = librosa.get_duration(y=y, sr=sr)
            total_frames = len(times)

            data, samplerate = sf.read(SONG_PATH)
            sd.play(data, samplerate)

            
            last_mod_time = current_mod_time
        else:
            screen.fill(BACKGROUND_COLOR)
            
            elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000.0
            if elapsed_time < audio_duration:
                current_frame = int((elapsed_time / audio_duration) * total_frames)
                magnitudes = stft_db[:, current_frame]
            else:
                # Feed the visualizer with low values after the audio ends
                magnitudes = np.full(MAX_RANGE, -80.0)

            # Create a transparent surface for drawing
            overlay = pygame.Surface(WINDOW_SIZE, pygame.SRCALPHA)

            points = []
            avg_magnitude = 0 
            for i, angle in enumerate(angles):
                mag = magnitudes[i]
                bar_length = (mag + 80) * 2  
                avg_magnitude += mag
                end_x = CENTER[0] + (RADIUS + bar_length) * math.cos(angle)
                end_y = CENTER[1] + (RADIUS + bar_length) * math.sin(angle)
                points.append((end_x, end_y))

            # Draw the polygon with gradient color
            color_intensity = min(max(int((avg_magnitude / MAX_RANGE + 80) * 3), 0), 255)
            color = (color_intensity, 255 - color_intensity, 255, 128)  
            pygame.draw.polygon(overlay, color, points)

            avg_magnitude /= MAX_RANGE
            circle_radius = 197 + (avg_magnitude + 80) * 0.5  

            # Draw the pulsing circle
            pygame.draw.circle(overlay, BACKGROUND_COLOR, CENTER, int(circle_radius))

            
            screen.blit(overlay, (0, 0))

            pygame.display.flip()
            clock.tick(60)

    pygame.quit()