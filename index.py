#!/usr/bin/env python3
from bottle import route, get, run, default_app, template, static_file, post, request, response, redirect, TEMPLATE_PATH
import os, time, sys, datetime, requests, json

pwd = os.getcwd()
#Add the template path if it's not there
if pwd + '/views/' not in TEMPLATE_PATH:
    TEMPLATE_PATH.insert(0,pwd + '/views/')

cookieSig="afds0ahegagljajdfqajfidsjaindosajifdsjfaofniog"

with open('config.json', 'r') as f:
    config = json.load(f)

#Useful magic for the rest of the program
def getPlaylists(removeBackground=True):
  # Don't want to fuck around with proper xml parsing, especially with such a simple
  # schema, so we're going to string-parse this beyotch
  r = requests.get("%s/fppxml.php?command=getPlayLists"%(config['fppUrl'],), auth=(config['fppUser'], config['fppPass']))
  output = r.text.strip().strip('<Playlists>').strip('</Playlists>')
  playlists = output.split('</Playlist><Playlist>')
  if removeBackground:
    playlists.remove('Background')
  outputLists = []
  for i in playlists:
    outputLists.append({'title':i,'displayTitle':i.replace('_',' ')})
  return outputLists

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

#Root and static stuff
@get('/static/<filename:path>')
def serve_static(filename):
    return static_file(filename, root=pwd+'/static/')

@get('/')
def index():
    playingStatus, playingSong, timeRemaining = checkPlayingStatus()
    playing = True if playingStatus != "0" else False
    playlistName = playingSong.replace('_', ' ')
    playable = isPlayable()
    if not playing:
       playlists = getPlaylists()
    else:
       playlists = []
    return template('default', playing=playing, radioStation=config['radioStation'], playlistName=playlistName, timeRemaining=timeRemaining, playlists=playlists, playable=playable, error=False)

@get('/play')
def playSong():
    requestedPlaylist = request.query.song
    playingStatus, playingSong, timeRemaining = checkPlayingStatus(ignoreBackground=False)
    playable = isPlayable()
    playlistName = playingSong.replace('_', ' ')
    playing = True if playingStatus != "0" else False
    if not playing:
       playlists = getPlaylists()
    else:
       playlists = []
    if playing and playingSong != "Background":
      return template('default', playing=playing, radioStation=config['radioStation'], playlistName=playlistName, timeRemaining=timeRemaining, playlists=playlists, playable=playable, error="Please wait until the current song is over before starting another song.")
    elif playing and playingSong == "Background":
      stopPlaylist()
    playPlaylist(requestedPlaylist)
    redirect("/")

@get('/stop')
def stopSong():
    playingStatus, playingSong, timeRemaining = checkPlayingStatus(ignoreBackground=False)
    if playingStatus != "0":
       stopPlaylist()
    redirect("/")

#Test directory.
@get('/test')
def outputTest():
    return "successful test."

if __name__=="__main__":
    run(host="0.0.0.0",port="8081")
else:
    application = default_app()
