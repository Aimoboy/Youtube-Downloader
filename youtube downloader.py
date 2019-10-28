import pytube
import subprocess
import os

def get_input():
    print("Enter the YouTube urls (type \"help\" for a tutorial):")
    lst = []
    while True:
        s = input()
        if s.lower() == "done":
            break
        elif s.lower() == "edit":
            edit_input(lst)
        elif s.lower() == "help":
            print("- Enter the YouTube urls of the videos you want to download separated by new lines.")
            print("- Type \"done\" when you are finished entering urls and want to start downloading.")
        lst.append(s)
    return lst

def print_lst_with_numbers(lst):
    for i in range(len(lst)):
        print("{0}: {1}".format(i + 1, lst[i]))

def edit_input(lst):
    print_lst_with_numbers(lst)
    while True:
        return


def download_video(url):
    # Get streams
    print("Fetching video streams...", end="", flush=True)
    yt = pytube.YouTube(url)
    youtube_title = yt.streams.first().default_filename[0:-4]
    video_title = youtube_title + "(video)"
    audio_title = youtube_title + "(audio)"
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

    # Merge video and audio and delete the downloaded files
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
    #print(lst)
    fails = download_list_of_urls(lst)
    print("Fails: {0}".format(fails))
