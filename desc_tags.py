import os
import eyed3
import sys
import requests
import urllib

def duration_from_seconds(s):
    """Module to get the convert Seconds to a time like format."""
    s = s
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)
    timelapsed = "{:02d}:{:02d}:{:02d}".format(int(h),int(m),int(s))
    return timelapsed

dir = sys.argv[1] + str('\\')
discogs = requests.get('https://api.discogs.com/releases/' + str(sys.argv[2])).json()

maxTrackNumber = 0

trackList = [''] * 99 
for song in os.listdir(dir):
    if song.endswith(".mp3"):
        af = eyed3.load(dir + song)
        track = {}
        track["number"] = af.tag.track_num[0]
        if af.tag.track_num[0] > maxTrackNumber:
            maxTrackNumber = af.tag.track_num[0]    
        track["name"] = song[:-4]
        track["name"] = track["name"][track["name"].find('-') + 1:]
        track["length"] = duration_from_seconds(af.info.time_secs)
        track["seconds"] = af.info.time_secs
        trackList[track["number"]] = track

trackList = trackList[1:maxTrackNumber]
totalTime = 0
print('Tracklist:')
for x in trackList:
        print(str(x["number"]) + '  ' + str(x["name"]) + '  ' + str(duration_from_seconds(totalTime)))
        totalTime += x["seconds"]

print('\n')
print("Label: " + discogs["labels"][0]["name"])
if discogs["year"] != 0:
    print("Year: " + str(discogs["year"]))

if discogs["companies"]:
    print('\n')
    print("Companies:")
    for x in discogs["companies"]:
        print(x["entity_type_name"] + ' - ' +x["name"])

if discogs["extraartists"]:
    print('\n')
    print("Credits:")
    for x in discogs["extraartists"]:
        print(x["role"] + ' - ' +x["name"])

print('\n')
print('Website: https://intrinse.net/ \n'+
'Instagram: https://www.instagram.com/intrinse_/ \n'+
'Soundcloud: https://soundcloud.com/intrinse \n'+
'Email: intrinse.mail@gmail.com \n\n'+

'Video generated with RenderTune: \n'+
'https://www.rendertune.com')

genres = []

for x in discogs["genres"]:
    x += ' full album'
    genres.append(urllib.parse.quote(x))
for x in discogs["styles"]:
    x += ' full album'
    genres.append(urllib.parse.quote(x))

keyWordCounts = {}
highestCount = 0

for n in genres:
    ytSearch = requests.get('https://www.googleapis.com/youtube/v3/search?order=date&part=snippet&q=' + n + '&maxResults=10&order=viewCount').json()

    for x in ytSearch["items"]:
        videoDetails = requests.get('https://www.googleapis.com/youtube/v3/videos?part=snippet&part=contentDetails&id=' + x["id"]["videoId"] + '').json()   
        for y in videoDetails["items"][0]["snippet"]["tags"]:
            if y in keyWordCounts:
                keyWordCounts[y] = keyWordCounts.get(y) + 1
                if keyWordCounts[y] >  highestCount:
                    highestCount = keyWordCounts[y]
            else:      
                keyWordCounts[y] = 1 

keyWordCounts = sorted(keyWordCounts.items(), key=lambda x: x[1])
printString = str(highestCount) + ": "

for i in reversed(keyWordCounts):
    if i[1] == highestCount: 
        printString += str(i[0]) + ', '
    else:
        print(printString + '\n')
        highestCount -= 1
        printString = str(highestCount) + ": " + str(i[0]) + ', '

print(printString)
        



