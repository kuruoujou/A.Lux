#!/usr/bin/env python3
import os, time, sys, datetime, requests, json

alux_version = 0.2
schema_location = (os.path.join(os.path.dirname(__file__), "db", "schema.ddl"))
db_location = (os.path.join(os.path.dirname(__file__), "db", "alux.sqlite"))

class db():
    """Database Access Functions."""

    def __init__(self):
        """Create DB if it doesn't exist, if it does, load it."""
        self.openConnection()
        c = self.conn.cursor()
        try:
            c.execute("SELECT * FROM alux_info WHERE key='version'")
            self.conn.row_factory = sqlite3.Row
        except sqlite3.OperationalError:
            self.conn.row_factory = sqlite3.Row
            self.createDB()

    def __del__(self):
        """Close DB class - just make sure the connection is closed."""
        try:
            self.closeConnection()
        except sqlite3.ProgrammingError:
            pass

    def openConnection(self):
        """Open a database connnection."""
        self.conn = sqlite3.connect(db_location)
        self.conn.row_factory = sqlite3.Row

    def closeConnection(self):
        """Closes the database connection."""
        self.conn.commit()
        self.conn.close()

    def createDB(self):
        """Create the Database if it doesn't exist.

        Requires a schema.ddl file to exist."""
        with open(schema_location, 'rt') as f:
            schema = f.read()
        self.conn.executescript(schema)
        # Make sure to add 
        self.updateInfo('version', alux_version)
        self.closeConnection()

    def updateInfo(self, key, value):
        """Update the alux_info table with a given key and value.
        If the key doesn't exist, create it."""
        self.openConnection()
        self.conn.execute(
                '''select * from alux_info where key = ?''',
                (version,))
        output = c.fetchone()
        if output is None:
            self.conn.execute(
                    '''insert into alux_info (key, value)
                    values (?,?);''',
                    (key, value))
        else:
            self.conn.execute(
                    '''update alux_info set value=? where key=?''',
                    (value, key))
        self.closeConnection()

        
class alux():
    def __init__():
        with open('config.json', 'r') as f:
            self.config = json.load(f)
        

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
