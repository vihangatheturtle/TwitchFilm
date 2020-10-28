from moviepy.editor import VideoFileClip
import requests
import socket
import time
import os

#Required for controlling stream from chat
server = 'irc.chat.twitch.tv'
port = 6667
nickname = ""
token = ""
channel = ""

#Required for streaming
streamKey = ""

#Required for auto changing stream title
broadcaster_id = ""
Authorization = ""
ClientId = ""

try:
    oauth = open('twitchservice_OAuth.dat', 'r')
except:
    pass
try:
    User = open('twitchservice_Username.dat', 'r')
except:
    pass
try:
    stream_key = open('twitchservice_StreamKey.dat', 'r')
except:
    pass
try:
    streamKey = str(stream_key.readlines()[0])
except:
    pass
try:
    nickname = str(User.readlines()[0])
except:
    pass
try:
    token = str(oauth.readlines()[0])
except:
    pass
try:
    channel = '#' + str(User.readlines()[0])
except:
    pass

if (token == ""):
    with open('twitchservice_OAuth.dat', 'a') as twitch:
        OAuthQ = input('No OAuth key detected, create one? [Y,N] ')
        if (OAuthQ == 'Y'):
            os.system('start https://twitchapps.com/tmi/')
            OAuthKey = input('OAuth key: ')
            token = str(OAuthKey)
            twitch.write(str(OAuthKey))
        if (OAuthQ == 'y'):
            os.system('start https://twitchapps.com/tmi/')
            OAuthKey = input('OAuth key: ')
            token = str(OAuthKey)
            twitch.write(str(OAuthKey))
        if (OAuthQ == 'N'):
            OAuthKey = input('OAuth key: ')
            token = str(OAuthKey)
            twitch.write(str(OAuthKey))
        if (OAuthQ == 'n'):
            OAuthKey = input('OAuth key: ')
            token = str(OAuthKey)
            twitch.write(str(OAuthKey))
elif (token == None):
    with open('twitchservice_OAuth.dat', 'a') as twitch:
        OAuthQ = input('No OAuth key detected, create one? [Y,N] ')
        if (OAuthQ == 'Y'):
            os.system('start https://twitchapps.com/tmi/')
            OAuthKey = input('OAuth key: ')
            token = str(OAuthKey)
            twitch.write(str(OAuthKey))
        if (OAuthQ == 'y'):
            os.system('start https://twitchapps.com/tmi/')
            OAuthKey = input('OAuth key: ')
            token = str(OAuthKey)
            twitch.write(str(OAuthKey))
        if (OAuthQ == 'N'):
            OAuthKey = input('OAuth key: ')
            token = str(OAuthKey)
            twitch.write(str(OAuthKey))
        if (OAuthQ == 'n'):
            OAuthKey = input('OAuth key: ')
            token = str(OAuthKey)
            twitch.write(str(OAuthKey))

if (nickname == ""):
    with open('twitchservice_Username.dat', 'a') as twitch:
        UserQ = input('Twitch Username: ')
        nickname = str(UserQ)
        channel = '#' + str(UserQ)
        twitch.write(str(UserQ))
elif (nickname == None):
    with open('twitchservice_Username.dat', 'a') as twitch:
        UserQ = input('Twitch Username: ')
        nickname = str(UserQ)
        channel = '#' + str(UserQ)
        twitch.write(str(UserQ))

if (streamKey == ""):
    with open('twitchservice_StreamKey.dat', 'a') as twitch:
        OAuthQ = input('No stream key detected, open twitch? [Y,N] ')
        if (OAuthQ == 'Y'):
            os.system('start https://dashboard.twitch.tv/settings/stream')
            OAuthKey = input('Stream Key: ')
            token = str(OAuthKey)
            twitch.write(str(OAuthKey))
        if (OAuthQ == 'y'):
            os.system('start https://dashboard.twitch.tv/settings/stream')
            OAuthKey = input('Stream Key: ')
            token = str(OAuthKey)
            twitch.write(str(OAuthKey))
        if (OAuthQ == 'N'):
            OAuthKey = input('Stream Key: ')
            token = str(OAuthKey)
            twitch.write(str(OAuthKey))
        if (OAuthQ == 'n'):
            OAuthKey = input('Stream Key: ')
            token = str(OAuthKey)
            twitch.write(str(OAuthKey))
elif (streamKey == None):
    with open('twitchservice_StreamKey.dat', 'a') as twitch:
        OAuthQ = input('No stream key detected, open twitch? [Y,N] ')
        if (OAuthQ == 'Y'):
            os.system('start https://dashboard.twitch.tv/settings/stream')
            OAuthKey = input('Stream Key: ')
            token = str(OAuthKey)
            twitch.write(str(OAuthKey))
        if (OAuthQ == 'y'):
            os.system('start https://dashboard.twitch.tv/settings/stream')
            OAuthKey = input('Stream Key: ')
            token = str(OAuthKey)
            twitch.write(str(OAuthKey))
        if (OAuthQ == 'N'):
            OAuthKey = input('Stream Key: ')
            token = str(OAuthKey)
            twitch.write(str(OAuthKey))
        if (OAuthQ == 'n'):
            OAuthKey = input('Stream Key: ')
            token = str(OAuthKey)
            twitch.write(str(OAuthKey))

def changeTitle(data):
    data = str(data)
    
    print("Changing stream title: " + data)
    
    headers = {
        'Authorization': Authorization,
        'Client-Id': ClientId,
        'Content-Type': 'application/json',
    }
    
    params = (
        ('broadcaster_id', broadcaster_id),
    )
    
    data = '{"game_id":"33214", "title":"' + data + '"}'

    response = requests.patch('https://api.twitch.tv/helix/channels', headers=headers, params=params, data=data)
    print(str(response.text))
    if "REQUESTS_THROTTLED" in response.text:
        print("Request denied, reason: REQUESTS_THROTTLED\n   Retrying...")
        while True:
            time.sleep(5)
            retry = requests.post('https://gql.twitch.tv/gql', headers=headers, data=data)
            if "REQUESTS_THROTTLED" in retry.text:
                print("   Request retried... FAILED")
                pass
            else:
                print("   Request retried... SENT")
                break
    else:
        print("Request sent successfully")

def streamTrailers(data):
    print("Closing any other possible streams")
    closeFfmpeg()
    time.sleep(10)
    print("Starting new stream instance: " + str(data))
    os.system('start /min ffmpeg -re -stream_loop -1 -i "' + str(data) + '" -vcodec libx264 -profile:v main -preset:v medium -r 30 -g 60 -keyint_min 60 -sc_threshold 0 -b:v 2500k -maxrate 2500k -bufsize 2500k -filter:v scale="trunc(oh*a/2)*2:720" -sws_flags lanczos+accurate_rnd -acodec aac -b:a 96k -ar 48000 -ac 2 -f flv rtmp://live.twitch.tv/app/live_191842162_wbSygqVSvBa4G2aQ2qivMswluXUZ7L')

def closeFfmpeg():
    os.system('taskkill /f /im ffmpeg.exe')
   
def streamVideoFromPlan(data, title):
    sendMSG("Switching stream, please wait")
    print("Closing any other possible streams")
    closeFfmpeg()
    closeFfmpeg()
    time.sleep(10)
    print("Starting new stream instance: " + str(data))
    os.system('start /min ffmpeg -re -stream_loop -1 -i "' + str(data) + '" -vcodec libx264 -profile:v main -preset:v medium -r 30 -g 60 -keyint_min 60 -sc_threshold 0 -b:v 2500k -maxrate 2500k -bufsize 2500k -filter:v scale="trunc(oh*a/2)*2:720" -sws_flags lanczos+accurate_rnd -acodec aac -b:a 96k -ar 48000 -ac 2 -f flv rtmp://live.twitch.tv/app/live_191842162_wbSygqVSvBa4G2aQ2qivMswluXUZ7L')
    sendMSG("Playback started of " + title)
    changeTitle("Playing: " + title)
    clip = VideoFileClip(str(data))
    video_duration = clip.duration - 3
    print(video_duration)
    print("Waiting " + str(video_duration) + " for film to finish")
    try:
        time.sleep(video_duration)
    except:
        pass
    closeFfmpeg()
    closeFfmpeg()
    
def sendMSG(message):
    message = "PRIVMSG #vihangatheturtle_ :" + message + "\r\n"
    sock.send(message.encode('utf-8'))
    
def doAction():
    print("1. Show trailers")
    print("2. Play film")
    action = input("action: ")
    if (action == "1"):
        streamTrailers("trailers/1.mp4")
        changeTitle("Watching films, picking...")
    if (action == "2"):
        os.system("dir films")
        filmn = input("film name(exact): ")
        streamVideo('films/' + filmn + '')
        changeTitle("Watching: " + filmn.split(';;;')[1].split('.')[0])
    doAction()

#changeTitle("Watching films, picking...")
#streamTrailers("trailers/1.mp4")

sock = socket.socket()
sock.connect((server, port))

sock.send(f"PASS {token}\n".encode('utf-8'))
sock.send(f"NICK {nickname}\n".encode('utf-8'))
sock.send(f"JOIN {channel}\n".encode('utf-8'))

def twitchControl():
    while True:
        try:
            sock.send("online check\n".encode('utf-8'))
            data = sock.recv(2048).decode()
            if not data:
                print("Socket offline")
                sock.close()
                sock.connect((server, port))
                
            resp = sock.recv(2048).decode()
            if "@vihangatheturtle_" in resp:
                if "pf!" in resp:
                    with open('film.index', 'r') as f:
                        for line in f:
                            if str(resp.splitlines()[0].split('pf!')[1]).startswith(line.split(' ')[0]):
                                print('playing film from location ' + line.split(';;;')[1])
                                sendMSG("Starting: " + str(line.split(';;;')[2]))
                                changeTitle("Starting: " + str(line.split(';;;')[2]))
                                streamVideo("films/" + line.split(';;;')[1], str(line.split(';;;')[2]))
                            else:
                                if str(resp.splitlines()[0].split('pf!')[1]) in line:
                                    print('Film ID not found, do you mean ' + line.split(' ')[0] + '?')
                                    sendMSG('Film ID not found, do you mean ' + line.split(' ')[0] + '?')
                                else:
                                    print('Film ID not found, no near matches found either')
                if "pf!trailers" in resp:
                    changeTitle("Watching films, picking...")
                    streamTrailers("trailers/1.mp4")
            if "@typhoonwq" in resp:
                if "pf!" in resp:
                    with open('film.index', 'r') as f:
                        for line in f:
                            if str(resp.splitlines()[0].split('pf!')[1]).startswith(line.split(' ')[0]):
                                print('playing film from location ' + line.split(';;;')[1])
                                sendMSG("Starting: " + str(line.split(';;;')[2]))
                                changeTitle("Starting: " + str(line.split(';;;')[2]))
                                streamVideo("films/" + line.split(';;;')[1], str(line.split(';;;')[2]))
                            else:
                                if str(resp.splitlines()[0].split('pf!')[1]) in line:
                                    print('Film ID not found, do you mean ' + line.split(' ')[0] + '?')
                                    sendMSG('Film ID not found, do you mean ' + line.split(' ')[0] + '?')
                                else:
                                    print('Film ID not found, no near matches found either')
                if "pf!trailers" in resp:
                    changeTitle("Watching films, picking...")
                    streamTrailers("trailers/1.mp4")
        except Exception as ex:
            print('Excepted with error: ' + ex)
            pass

filmindex = "film.index"
fiIdentity = "findex"
inOrder = "true"
ogQuality = "true"
noAds = "false"
noTrailersTillEnd = "false"
useIndex = "findex"
FilmID = []

def usePlan():
    with open('plan.index', 'r') as f:
        i = 0
        print('Checking plan')
        for line in f:
            if (str(line) != ""):
                if (str(line) != None):
                    linedata = line.split(' ')[0]
                    if (linedata == "end"):
                            print('Found end of script')
                            break
                    if (linedata == "using"):
                            print('Found "using" identifier')
                            usingdata = line.split(' ')[1]
                            print('Setting "filmindex" variable')
                            filmindex = str(line.split(' ')[1])
                            usingoperator = line.split(' ')[2]
                            if (usingoperator == "as"):
                                print('Assinging "filmindex" variable to ' + str(line.split(' ')[3]).splitlines()[0])
                                usingFiIdentity = line.split(' ')[3]
                                fiIdentity = str(line.split(' ')[3].splitlines()[0])
                    if (linedata == "play"):
                        playtype = line.split(' ')[1]
                        if (playtype == "settings"):
                            print('Found "settings" block')
                            settingslist = line.split(' ')[2]
                            settingslist = settingslist.split(',')
                            if (settingslist[0] == "inorder"):
                                inOrder = "true"
                                print('inOrder: ' + inOrder)
                            if (settingslist[0] == "ogquality"):
                                ogQuality = "true"
                                print('ogQuality: ' + ogQuality)
                            if (settingslist[0] == "noads"):
                                noAds = "true"
                                print('noAds: ' + noAds)
                            if (settingslist[0] == "notrailers"):
                                noTrailersTillEnd = "true"
                                print('noTrailersTillEnd: ' + noTrailersTillEnd)
                            if (settingslist[1] == "inorder"):
                                inOrder = "true"
                                print('inOrder: ' + inOrder)
                            if (settingslist[1] == "ogquality"):
                                ogQuality = "true"
                                print('ogQuality: ' + ogQuality)
                            if (settingslist[1] == "noads"):
                                noAds = "true"
                                print('noAds: ' + noAds)
                            if (settingslist[1] == "notrailers"):
                                noTrailersTillEnd = "true"
                                print('noTrailersTillEnd: ' + noTrailersTillEnd)
                            if (settingslist[2] == "inorder"):
                                inOrder = "true"
                                print('inOrder: ' + inOrder)
                            if (settingslist[2] == "ogquality"):
                                ogQuality = "true"
                                print('ogQuality: ' + ogQuality)
                            if (settingslist[2] == "noads"):
                                noAds = "true"
                                print('noAds: ' + noAds)
                            if (settingslist[2] == "notrailers"):
                                noTrailersTillEnd = "true"
                                print('noTrailersTillEnd: ' + noTrailersTillEnd)
                            if (settingslist[3] == "inorder"):
                                inOrder = "true"
                                print('inOrder: ' + inOrder)
                            if (settingslist[3] == "ogquality"):
                                ogQuality = "true"
                                print('ogQuality: ' + ogQuality)
                            if (settingslist[3] == "noads"):
                                noAds = "true"
                                print('noAds: ' + noAds)
                            if (settingslist[3] == "notrailers"):
                                noTrailersTillEnd = "true"
                                print('noTrailersTillEnd: ' + noTrailersTillEnd)
                        if (playtype == "viewing"):
                            index = line.split(' ')[2]
                            index = index.split(':')
                            useIndex = index[0]
                            FilmID.append(index[1])
                            print('Found "viewing" block with index ' + useIndex + ' and film ID ' + FilmID[-1])
                else:
                    print('Line ' + str(i) + ' empty, ignoring...')
                i = i + 1
    print('RECAP:')
    print('  Film Index File: ' + filmindex)
    print('  Registered Film Index: ' + fiIdentity)
    print('  inorder setting: ' + inOrder)
    print('  ogquality setting: ' + ogQuality)
    print('  noads setting: ' + noAds)
    print('  notrailers setting: ' + noTrailersTillEnd)
    print('  Last Used Film Index: ' + useIndex)
    print('  Detected Film Array: ' + str(FilmID))
    print('  Film Array Length: ' + str(len(FilmID)))
    print('Checking registered film index file...')
    while True:
        try:
            index = open(str(filmindex), 'r')
            print('Registered film index OK')
            break
        except:
            print('Registered film index ERROR')
            time.sleep(5)
    print('Starting screening...')
    closeFfmpeg()
    time.sleep(1)
    closeFfmpeg()
    time.sleep(1)
    closeFfmpeg()
    print(filmindex)
    totalIDs = len(FilmID) - 1
    print(totalIDs)
    i = 0
    
    while i <= totalIDs:
        with open(filmindex, 'r') as index:
            for line in index:
                if line.split(' ')[0].startswith(FilmID[i]):
                    print('playing film from location ' + line.split(';;;')[1])
                    sendMSG("Switching stream, please wait")
                    print("Closing any other possible streams")
                    closeFfmpeg()
                    closeFfmpeg()
                    time.sleep(10)
                    print("Starting new stream instance: " + "films/" + str(line.split(';;;')[1]))
                    os.system('start /min ffmpeg -re -stream_loop -1 -i "' + "films/" + str(line.split(';;;')[1]) + '" -vcodec libx264 -profile:v main -preset:v medium -r 30 -g 60 -keyint_min 60 -sc_threshold 0 -b:v 2500k -maxrate 2500k -bufsize 2500k -filter:v scale="trunc(oh*a/2)*2:720" -sws_flags lanczos+accurate_rnd -acodec aac -b:a 96k -ar 48000 -ac 2 -f flv rtmp://live.twitch.tv/app/live_191842162_wbSygqVSvBa4G2aQ2qivMswluXUZ7L')
                    sendMSG("Playback started of " + line.split(';;;')[2])
                    changeTitle("Playing: " + line.split(';;;')[2])
                    clip = VideoFileClip("films/" + str(line.split(';;;')[1]))
                    video_duration = clip.duration - 3
                    print(video_duration)
                    print("Waiting " + str(video_duration) + " for film to finish")
                    try:
                        time.sleep(video_duration)
                    except:
                        pass
                    closeFfmpeg()
                    closeFfmpeg()
        i=i+1
    print('Plan finished, switching to twitch control...')
    twitchControl()
    
usePlan()