from moviepy.editor import *
import os, os.path
import random


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

def combine_audio_video(dt_str: str, post_list: list):
    num_files = 0

    # Gets the num of files in the temp dir.
    for path in os.listdir(f"./assets/files_{dt_str}/temp"):
        if os.path.isfile(os.path.join(f"./assets/files_{dt_str}/temp", path)):
            num_files += 1

    title_audio = AudioFileClip(f"./assets/files_{dt_str}/title_{dt_str}.mp3")

    title_screenshot = (
        ImageClip(f"./assets/files_{dt_str}/title_{dt_str}.png")
        .set_duration(title_audio.duration)
        .fx(vfx.resize, width=(720) * 0.8)
        .set_position(("center", "center"))
    )

    post_audio = AudioFileClip(f"./assets/files_{dt_str}/post_{dt_str}.mp3")

    audioList = [title_audio, post_audio]
    imageList = [title_screenshot]

    videoClip = concatenate_videoclips(imageList).set_position(("center", "center"))
    audioClip = concatenate_audioclips(audioList)

    videoClip.set_audio(audioClip)

    # Minecraft clip Credit to @bbswitzer.
    minecraft_clip = VideoFileClip("./minecraft_video/bbswitzer.mp4")

    # Selects a random startingpoint in the minecraft video.
    start_clp = random.randint(20, 3600)

    # Sets the minecraft clips length, to the length of the duration of the generated TTS audio.
    minecraft_clip = minecraft_clip.subclip(
        (start_clp), (start_clp + audioClip.duration)
    ).set_position(("center", "center"))
    minecraft_clip = minecraft_clip.resize(height=1280)

    clips_to_composite = [minecraft_clip, videoClip]

    # --------------- this block of code is to create the subtitles for the post, and to set the duration of each subtitle ---------------
    _audioList = []

    # 
    for x in range(num_files):

        audio = AudioFileClip(f"./assets/files_{dt_str}/temp/{x}.mp3")

        if len(_audioList) == 0:
            txt_clip = (
                TextClip(
                    post_list[x],
                    fontsize=45,
                    stroke_color="black",
                    color="white",
                    font="Arial-bold",
                    kerning=-2,
                    interline=-1,
                    size=(650, 1280),
                    method="caption",
                )
                .set_pos("center")
                .set_start(title_audio.duration)
                .set_duration(audio.duration)
            )
            clips_to_composite.append(txt_clip)
            _audioList.append(audio.duration)
            _audioList.append(title_audio.duration)
        else:
            txt_duration = sum(_audioList)

            txt_clip = (
                TextClip(
                    post_list[x],
                    fontsize=45,
                    stroke_color="black",
                    color="white",
                    font="Arial-bold",
                    kerning=-2,
                    interline=-1,
                    size=(650, 1280),
                    method="caption",
                )
                .set_pos("center")
                .set_start(txt_duration)
                .set_duration(audio.duration)
            )
            clips_to_composite.append(txt_clip)
            _audioList.append(audio.duration)
    # --------------- end of block ---------------

    # Create a watermark on the video.
    watermark = TextClip("@brandonbondig", fontsize=35, color="white", font="Arial-bold").set_pos(('left', 'bottom')).set_start(0).set_opacity(0.6)
    clips_to_composite.append(watermark)

    # Composites out video with all the provided audio and video.
    composite = CompositeVideoClip(clips_to_composite, (720, 1280))
    composite.audio = audioClip
    composite.duration = audioClip.duration

    # Renders the video to the ./rendered_videos dir. 
    try:
        composite.write_videofile(
            f"./rendered_videos/render_{dt_str}.mp4", threads=4, fps=30,
        )
    except Exception as e:
        print(e)

    print(f"{bcolors.OKBLUE}Movie is done rendering {bcolors.ENDC}")

