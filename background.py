#!/usr/bin/env python3
# Checks every 30 seconds to see if a thing is playing.
# If we are in our time and something is not playing, it starts it.
# If we are outside our time and something is playing, it stops it.
import os, time, sys, datetime, requests, json

with open('/lights/config.json', 'r') as f:
    config = json.load(f)

def checkPlayingStatus(ignoreBackground=True):
  r = requests.get("%s/fppxml.php?command=getFPPstatus"%(config['fppUrl'],), auth=(config['fppUser'], config['fppPass']))
  output = r.text.strip()
  playingStatus = output.split('<fppStatus>')[1].split('</fppStatus>')[0]
  if playingStatus != "0":
    playingSong = output.split('<CurrentPlaylist>')[1].split('</CurrentPlaylist>')[0]
    playingRemaining = output.split('<SecondsRemaining>')[1].split('</SecondsRemaining>')[0]
  else:
    playingSong = "None"
    playingRemaining = "0"
  if ignoreBackground and playingSong == "Background":
    playingStatus = "0"
  return playingStatus, playingSong, playingRemaining

def playPlaylist(playlist, repeat=False):
  if repeat:
    r = requests.get("%s/fppxml.php?command=startPlaylist&playList=%s&repeat=checked"%(config['fppUrl'],playlist), auth=(config['fppUser'], config['fppPass']))
  else:
    r = requests.get("%s/fppxml.php?command=startPlaylist&playList=%s"%(config['fppUrl'],playlist), auth=(config['fppUser'], config['fppPass']))

def stopPlaylist():
  r = requests.get("%s/fppxml.php?command=stopNow"%(config['fppUrl'],), auth=(config['fppUser'], config['fppPass']))

# Check if we are in the time frame for shows
def isPlayable():
  os.environ["TZ"]=config['timezone']
  time.tzset()
  currentHour = datetime.datetime.now().hour
  if config['startHour'] > config['endHour']:
    config['endHour'] = config['endHour'] + 24
  playable = True if config ['startHour'] <= currentHour and config['endHour'] > currentHour else False
  return playable

# Let supervisor handle daemon things, just run infinitely. Check every 30 seconds.
while(True):
  playingStatus, playingSong, playingRemaining = checkPlayingStatus(ignoreBackground=False)
  if isPlayable() and playingStatus == "0":
#  if False:
    playPlaylist("Background", repeat=True)
  elif not isPlayable() and playingStatus != "0":
    stopPlaylist()
  time.sleep(30)
