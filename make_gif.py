from parse import parse_microdvd, parse_srt
from datetime import datetime, timedelta
import subprocess as sp

PALETTE="palette.png"
GIF_FILTERS="fps=15,scale=640:-1:flags=lanczos"

class MakeWebm(object):
    """class to turn movie and subtitle file into webm loops"""
    def __init__(self, sub_path, movie_path):
        self.movie_path = movie_path
        self.sub_path = sub_path
        if ".sub" in sub_path:
            self.subtitles = parse_microdvd(sub_path)
        else:
            assert(".srt" in sub_path)
            self.subtitles = parse_srt(sub_path)

    def webm_from_str_match(self, query):
        """Find first subtitle containing query, and make a webm"""
        for subtitle in self.subtitles:
            if query in subtitle["line"]:
                start = subtitle["start"]
                print(str(start))
                duration = subtitle["end"] - subtitle["start"]
                print(str(duration.total_seconds()))
                params = ["ffmpeg", "-vcodec", 
                    "libvpx", "-an", 
                    "-ss", str(start),
                    "-t", str(duration.total_seconds()),
                    "-i", self.movie_path, 
                    # "-vf", "subtitles=" + self.sub_path,
                    "output.webm"]
                print(params)
                sp.run(params)
                return "output.webm"
        return "Line not found"


    def gif_from_str_match(self, query):
        """Find first subtitle containing query, and make a webm"""
        for subtitle in self.subtitles:
            if query in subtitle["line"]:
                start = subtitle["start"]
                print(str(start))
                duration = subtitle["end"] - subtitle["start"]
                print(str(duration.total_seconds()))
                # part 1: make frames
                # FIXME sp.run(["rm", ".\\frames\\*"])
                """sp.run(["ffmpeg", 
                    "-ss", str(start),
                    "-t", str(duration.total_seconds()),
                    "-vf", 
                    "-i", self.movie_path, 
                    "-vf",
                    GIF_FILTERS + "subtitles=" + self.sub_path,
                    "-y",
                    "frames/ffout%03d.png"])
                sp.run(["./imgmagick/convert", "-loop", "0",
                "./frames/ffout*.png", "output.gif"])
                return "output.webm"
            """
                params = ["ffmpeg", 
                        "-ss", str(start),
                        "-t", str(round(duration.total_seconds(), 3)),
                        "-i", self.movie_path,
                        "-an", "-vf", GIF_FILTERS + ",subtitles=" 
                        + self.sub_path,
                        "output.gif"]
                print(params)
                sp.run(params)
                return "output.gif"
        return "Line not found"


if __name__ == "__main__":
    m = MakeWebm("harold.sub", "harold.m4v")
    m.webm_from_str_match("buttocks")