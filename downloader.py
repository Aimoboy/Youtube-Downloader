import os
import re
import pytube
import subprocess

class Downloader:
    def __init__(self):
        self.load_options()

        urls = self.read_lines("urls.txt")
        self.validate_input(urls)

        fails = self.download_list_of_urls(urls)
        print(f"Fails: {fails}")

        if self.shutdown and fails == 0:
            os.system("shutdown /s /t 1")
        else:
            input("Press enter to exit...")

    def read_lines(self, file):
        '''Read from file, split new lines and return a list of the lines.'''

        with open(file, "r+") as f:
            return f.read().splitlines()

    def load_options(self):
        '''Load options from the options.txt file.'''

        lines = self.read_lines("options.txt")

        # Load format
        self.format = re.match(r"format=(.+)", lines[0]).group(1)
        if self.format not in ["mp3", "mp4"]:
            raise Exception("Invalid format. Please use 'mp3' or 'mp4'.")

        # Load verbose
        verbose = re.match(r"verbose=(.+)", lines[1]).group(1)
        if verbose == "y":
            self.verbose = True
        elif verbose == "n":
            self.verbose = False
        else:
            raise Exception("Invalid verbose option. Please use 'y' or 'n'.")

        # Load shutdown
        shutdown = re.match(r"shutdown=(.+)", lines[2]).group(1)
        if shutdown == "y":
            self.shutdown = True
        elif shutdown == "n":
            self.shutdown = False
        else:
            raise Exception("Invalid shutdown option. Please use 'y' or 'n'.")
    
    def validate_input(self, lst):
        '''Check if the youtube urls in the list lst is valid.'''

        # Check if all inputs are YouTube urls
        invalid_urls = []
        for i in range(len(lst)):
            r = r"(https://www.)?(youtube.com/watch\?v=).{11}"
            match = re.sub(r, "", lst[i])
            if lst[i] == "" or match != "":
                invalid_urls.append("Line {0}: {1}".format(i + 1, lst[i]))
        
        # Print invalid urls and quit if there are any
        if len(invalid_urls) != 0:
            print("The following url(s) are invalid:")
            for i in range(len(invalid_urls)):
                print(invalid_urls[i])
            exit()
        
    def download_mp4(self, url):
        '''Download mp4 from url.'''

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
        cmd = f"ffmpeg -i \"{video_title}.mp4\" -i \"{audio_title}.mp4\" -c copy -map 0:v -map 1:a -shortest -hide_banner -loglevel panic \"output/{youtube_title}.mp4\""
        subprocess.call(cmd, shell=True)
        os.remove(f"{video_title}.mp4")
        os.remove(f"{audio_title}.mp4")
        print("Done", flush=True)

        print("Finished", flush=True)
    
    def download_mp3(self, url):
        '''Download mp3 from url.'''

        # Get streams
        print("Fetching video streams...", end="", flush=True)
        yt = pytube.YouTube(url)
        youtube_title = yt.streams.first().default_filename[0:-4]
        print("Done", flush=True)

        # Download audio
        print("Audio download...", end="", flush=True)
        a_s = yt.streams.filter(only_audio=True).first()
        a_s.download(filename=youtube_title)
        os.rename(f"{youtube_title}.mp4", f"output/{youtube_title}.mp3")
        print("Done", flush=True)

        print("Finished", flush=True)
    
    def download_list_of_urls(self, lst):
        length = len(lst)
        fails = 0
        for i in range(length):
            url = lst[i]
            print(f"Beginning download {i + 1} out of {length} ({url})")
            try:
                if self.format == "mp3":
                    self.download_mp3(url)
                elif self.format == "mp4":
                    self.download_mp4(url)
            except Exception as e:
                fails += 1
                print("Failed")
                print("Error:")
                if self.verbose:
                    if hasattr(e, "message"):
                        print(e.message)
                    else:
                        print(e)
            else:
                print("Success")
                with open("urls.txt", "w") as f:
                    if i < len(lst):
                        for line in lst[i + 1:]:
                            f.write(line)
                            f.write("\n")
                    else:
                        f.write("")
            finally:
                print()
        return fails


d = Downloader()

