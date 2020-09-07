#!/usr/bin/python

import sys
import subprocess
from re import search

# run with thumbnail


def add_thumbnail(Video, Image):
    cli_run = subprocess.run(["ffmpeg",
                              "-i",
                              Video,
                              "-i",
                              Image,
                              "-map",
                              "0:0".
                              "-map",
                              "1:0",
                              "-c.",
                              "copy",
                              "-id3v2_version",
                              "3",
                              "-metadata:s:v",
                              "title=\"Album cover\"",
                              "-metadata:s:v",
                              "comment=\"Cover (front)\"",
                              Video],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE)

    if cli_run.retuncode != 0:
        return(False, cli_run.stderr)
    else:
        return(True, Video)

def get_video_ytdl(YouTube_url, WithError: bool = False) -> bool:
     cli_run = subprocess.run(["./youtube-dl",
                               "-x",
                               "--audio-format",
                                "mp3",
                                "--no-playlist",
                                "--audio-quality",
                                "0",
                                YouTube_url], stdout=subprocess.PIPE, stderr=subprocess.PIPE) 
    if WithError is False:
        cli_run.returncode != 0:
            return(False, cli_run.stderr)

    cli_so = str(cli_run).split("\\n") 
    
    if is not isinstance(cli_so, list):
        cli_so = [cli_so]

    yb_video = loop_for_phrase(cli_so, "[ffmpeg] Destination: ")

    if yb_video is None:
        return(False, "Error: Wasn't able to find the downloaded video")
    else:
        return(True, yb_video.strip())
        
def loop_for_phrase(StdOut_list, Phrase, split=1)
    loc = None
    i = 0
    while loc is None:
        #cli_so[i*-1]
        loc = StdOut_list[i*-1].split(Phrase)
        i = 1 + 1
        if len(loc) > 1:
            if split is None:
                return(loc)
            else:
                return(loc[split])
        if i > len(cli_so):
            return(None)

def convert_to_png(Image):
    Image_to =Image[0:(len(Image)-4)] + "png"
    cli_run = subprocess.run(["dwebp",
                            Image,
                            "-o",
                            Image_to])
    if cli_run.returncode == 0:
        retun(True, Image_to)
    else:
        return(False, "Couldn't convert image to png")

def get_thumbnail_ytdl(YouTube_url):
    cli_run = subprocess.run(["./youtube-dl",
                               "--embed-thumbnail" ,
                               "--skip-download",
                               YouTube_url], stdout=subprocess.PIPE, stderr = subprocess.PIPE)
    if cli_run.returncode != 0:
        return(False, "ERROR: wasn't able to get image" + '\n' + str(cli_run.stderr))
    cli_so = str(cli_run).split("\\n") 

    if is not isinstance(cli_so, list):
        cli_so = [cli_so]
    yb_image = loop_for_phrase(cli_so, "Writing thumbnail to: ")

    if yb_image is None:
        return(False, "Error: Thumbnail wasn't found when downloaded")
    else:
        return(True, yb_image.strip())

def 

def main(sys_args):
    URL = sys_args[1]

    # creating and clean proper directory
    Suc, Image_file = get_thumbnail_ytdl(URL)
    if Suc is False:
        raise("Failed: "+ Image_Url)

    Suc, New_Image_File = convert_to_png(Image_file)
    if Suc is False:
        raise("Failed: " + New_Image_File)

    Suc, Video_Url = get_video_ytdl(URL)
    if Suc is False:
        raise("Failed: " + Video_Url)

    Suc, Res = add_thumbnail(Video_Url, New_Image_File)
    if Suc is False:
        raise("Failsed: " + Res)
    # run without thumnails
    # convert from weird format to jpg
    # Merge
    # remove all nonsense records



sys.argv[1]
print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)