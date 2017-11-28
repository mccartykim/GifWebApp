#! /usr/bin/python3
import sys
from datetime import datetime, timedelta
import re

# store the format for SRT in time
SRT_TIME_FMT = "%H:%M:%S,%f"
DATETIME_ZERO = datetime.strptime("00:00:00,000", SRT_TIME_FMT)

# store the format for SRT in frames
MICRODVD_FMT = r"\{(\d*)\}"

# STUB FIXME TODO HOO BOY XXX
def parse_srt(fpath):
    subtitles = []

    with open(fpath, encoding="utf-8", errors="ignore") as f:
        subt = {"line": ""}
        for line in f:
            assert(subt["line"] == "" or subt["line"])
            ln = line.strip()
            if ln.isdigit():
                subt['num'] = int(ln)
            elif "-->" in ln:
                raw_start, raw_end = ln.split(" --> ")
                start = datetime.strptime(raw_start.strip(), SRT_TIME_FMT) - DATETIME_ZERO
                end = datetime.strptime(raw_end.strip(), SRT_TIME_FMT) - DATETIME_ZERO
                subt["start"] = start
                subt["end"] = end
            # if not blank
            elif ln:
                if subt.get("line") is None:
                    subt["line"] = ln
                subt["line"] += "\n" + ln 
            #if blank
            else:
                subtitles.append(subt)
                subt = {"line": ""}

    return subtitles


def parse_microdvd(fpath):
    subtitles = []
    with open(fpath,encoding="utf-8", errors="ignore") as f:
        for line in f:
            subt = {}
            ln = line.strip()
            m = re.search(r"\{(\d*)\}\{(\d*)\}(.*)", ln)
            try:
                raw_start = m[1]
                raw_end = m[2]
                line = re.sub("\|", "\n", m[3])
                start = timedelta(seconds=(int(raw_start) / 23.976)) 
                end = timedelta(seconds=(int(raw_end) / 23.976))
                subt["start"] = start
                subt["end"] = end
                subt["line"] = line
                subtitles.append(subt)
            # if regex match fails, print offending line
            # FIXME either put this in a log or debug mode
            except TypeError:
                print(ln)


    return subtitles

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if ".srt" in sys.argv[1]:
            [print(line) for line in parse_srt(sys.argv[1])]
        else: 
            [print(line) for line in parse_microdvd(sys.argv[1])]
    else:
        print("USAGE: python parse.py FILE")
