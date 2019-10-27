import pytube
import subprocess
import os

def get_input():
    lst = []
    while True:
        s = input()
        if s == "done":
            break
        lst.append(s)
    return lst

def download_video(url):
    # Get streams
    print("Fetching video streams...", end="", flush=True)
    yt = pytube.YouTube(url)
    youtube_title = yt.streams.first().default_filename[0:-4]
    video_title = youtube_title + "_video"
    audio_title = youtube_title + "_audio"
    print("Done", flush=True)

    # Download video
    print("Video download...", end="", flush=True)
    v_s = yt.streams.filter(adaptive=True, only_video=True).first()
    v_s.download(filename=video_title)
    print("Done", flush=True)

    # Download audio
    print("Audio download...", end="", flush=True)
    a_s = yt.streams.filter(only_audio=True).first()
    a_s.download(filename=audio_title)
    print("Done", flush=True)

    # Merge video and audio and delete files
    print("Merging download...", end="", flush=True)
    cmd = "ffmpeg -i \"{0}.mp4\" -i \"{1}.mp4\" -c copy -map 0:v -map 1:a -shortest -hide_banner -loglevel panic \"{2}.mp4\"".format(video_title, audio_title, youtube_title)
    subprocess.call(cmd, shell=True)
    os.remove("{0}.mp4".format(video_title))
    os.remove("{0}.mp4".format(audio_title))
    print("Done", flush=True)

    print("Finished", flush=True)

def download_list_of_urls(lst):
    length = len(lst)
    fails = 0
    for i in range(length):
        url = lst[i]
        print("Beginning download {0} out of {1} ({2})".format(i + 1, length, url))
        try:
            download_video(url)
        except:
            fails += 1
            print("Failed")
        else:
            print("Success")
        finally:
            print()
    return fails

if __name__ == "__main__":
    lst = get_input()
    fails = download_list_of_urls(lst)
    print("Fails: {0}".format(fails))
