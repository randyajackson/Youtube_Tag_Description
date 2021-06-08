import os
import eyed3

def duration_from_seconds(s):
    """Module to get the convert Seconds to a time like format."""
    s = s
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    timelapsed = "{:02d}:{:02d}:{:02d}".format(int(h),int(m),int(s))
    return timelapsed

dir = 'C:\Albums\Dissidenten - Life At The Pyramids\Tracks\\'
trackList = [''] * 99 
for song in os.listdir(dir):
    if song.endswith(".mp3"):
        af = eyed3.load(dir + song)
        print(song)
        print(duration_from_seconds(af.info.time_secs))
        print( af.tag.track_num[0] )
        track = {}
        track["number"] = af.tag.track_num[0]
        track["name"] = song
        track["length"] = duration_from_seconds(af.info.time_secs)
        track["seconds"] = af.info.time_secs
        trackList[track["number"]] = track

totalTime = 0

for x in trackList:
    if x != '':
        print(str(x["number"]) + '  ' + str(x["name"]) + '  ' + str(duration_from_seconds(totalTime)))
        totalTime += x["seconds"]