from reddit.redditAPI import getPost
from TTS.TikTokTSS import TikTok
from get_screenshot.take_screenshot import PWscreenshort
from create_movie.createMovie import combine_audio_video
from create_movie.con_audio import combine_audio
from sanitize.voice import sanitize_text
from chopper.chopper import chopString
import os
import shutil
from datetime import datetime


if __name__ == "__main__":

    subreddit = 'confession'
    post_num = 5

    # Datetime used to create a unique id for the final render.
    now = datetime.now()
    dt_str = now.strftime("%d-%m-%Y_%H-%M-%S")

    # Getting post info
    try:
        title, post, url, is_nsfw, id = getPost(subreddit, post_num)
    except Exception as e:
        quit()
        
    # Creating initial dir's for 'create_movie' to access.
    while True:
        try:
            os.mkdir(f"./assets")
            os.mkdir(f"./assets/files_{dt_str}/")
            os.mkdir(f"./assets/files_{dt_str}/temp")
            break
        except FileExistsError:
            shutil.rmtree(f"./assets")
            continue

    # Takes screenshorts of title and post.
    PWscreenshort.takeScreenShot(url, dt_str, "title", id, is_nsfw)
    PWscreenshort.takeScreenShot(url, dt_str, "post", '[data-test-id="post-content"]',is_nsfw)

    # Cleans the title and post, return a string including the raw version with
    # swearwords, and a string with swearwords switched out with words in ./blacklisted.json.
    sanitized_text, black_listed = sanitize_text(post)

    # Chops the strings into blocks of about 250 chars each,
    # for screen subtitles and to prevent exceeding the TikTok TTS API string limit.
    chopped_sanitized = chopString(sanitized_text)
    chopped_blacklisted = chopString(black_listed)

    # iterates through the blacklisted list and generates the text-to-speech files.
    for index, value in enumerate(chopped_blacklisted):
        TikTok().run(value, f"./assets/files_{dt_str}/temp/{index}.mp3",1)

    # Combines the generated text-to-speech files into a single mp3 file.
    combine_audio(
        f"./assets/files_{dt_str}/temp",
        f"./assets/files_{dt_str}/post_{dt_str}.mp3"
    )

    # Returns a clean version of the pos t title.
    _, title_sanitezed = sanitize_text(title)

    # Generates TTS of title.
    TikTok().run(title_sanitezed, f"./assets/files_{dt_str}/title_{dt_str}.mp3",1)

    # Function for combining both the generated video and audio.
    combine_audio_video(dt_str, chopped_sanitized)

