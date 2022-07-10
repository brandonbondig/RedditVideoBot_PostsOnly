from moviepy.editor import *
import os, os.path

class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def combine_audio(filepath,writepath):
    num_files = 0

    for path in os.listdir(filepath):
        if os.path.isfile(os.path.join(filepath, path)):
            num_files += 1

    audioList = []

    for x in range(num_files):
        audio = AudioFileClip(f"{filepath}/{x}.mp3")
        audioList.append(audio)
        
    print(f"{bcolors.OKBLUE}Combined audio to : {bcolors.OKGREEN}{writepath}{bcolors.ENDC}")
    audioClip = concatenate_audioclips(audioList)
    audioClip.write_audiofile(f"{writepath}")


