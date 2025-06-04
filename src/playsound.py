import os
from playsound3 import playsound

# Get the absolute path of the directory where this script is located
base_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the audio files
clean_path = os.path.abspath(os.path.join(base_dir, '..', 'audio', 'clean.mp3'))
dirty_path = os.path.abspath(os.path.join(base_dir, '..', 'audio', 'dirty.mp3'))

# Play the audio files
playsound(clean_path)
playsound(dirty_path)