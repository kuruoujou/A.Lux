#!/usr/bin/env python3
import os, time, sys, datetime, requests, json, sqlite3
import xml.etree.ElementTree as et

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
            c.execute("SELECT * FROM alux_info WHERE key='version';")
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
        return

    def closeConnection(self):
        """Closes the database connection."""
        self.conn.commit()
        self.conn.close()
        return

    def createDB(self):
        """Create the Database if it doesn't exist.

        Requires a schema.ddl file to exist."""
        with open(schema_location, 'rt') as f:
            schema = f.read()
        self.conn.executescript(schema)
        # Make sure to add 
        self.updateInfo('version', alux_version)
        self.closeConnection()
        return

    def updateInfo(self, key, value):
        """Update the alux_info table with a given key and value.
        If the key doesn't exist, create it."""
        self.openConnection()
        c = self.conn.cursor()
        c.execute(
                '''SELECT * FROM alux_info WHERE key = ?;''',
                (version,))
        output = c.fetchone()
        if output is None:
            self.conn.execute(
                    '''INSERT INTO alux_info (key, value)
                    VALUES (?,?);''',
                    (key, value))
        else:
            self.conn.execute(
                    '''UPDATE alux_info SET value=? WHERE key=?;''',
                    (value, key))
        self.closeConnection()
        return

    def getUser(self, uid=None, username=None, cookie_id=None):
        """Gets user information based on some value."""
        self.openConnection()
        c = self.conn.cursor()
        if uid:
            c.execute(
                    '''SELECT * FROM users WHERE id=?;''',
                    (uid,))
        elif username:
            c.execute(
                    '''SELECT * FROM users WHERE username=?;''',
                    (username,))
        elif cookie_id:
            c.execute(
                    '''SELECT * FROM users WHERE cookie_id=?;''',
                    (cookie_id,))
        output = c.fetchone()
        output = dict(output) if output is not None else None
        self.closeConnection()
        return output

    def modifyUser(self, uid, userInfo):
        """Changes a user's information based on their UID.
        Changes the entire user row, userInfo should be a modified dictionary
        based on the output of getUser."""
        self.openConnection()
        if 'cookie_id' not in userInfo:
            userInfo['cookie_id'] = None
        if 'expiration' not in userInfo:
            userInfo['expiration'] = None
        self.conn.execute(
                '''UPDATE users SET username=?, password=?,
                cookie_id=?, expiration=? WHERE uid=uid''',
                ( userInfo['username'], userInfo['password'],
                  userInfo['cookie_id'], userInfo['expiration']))
        self.closeConnection()
        return

    def getSongs(self, hidden=False, ident=None, playlist=None):
        """Get songs in the database. If an ID or playlist is provided,
        just get that song. If hidden is false, then only
        return non-hidden items."""
        self.openConnection()
        c = self.conn.cursor()
        if not hidden and ident:
            c.execute(
                '''SELECT * FROM songs WHERE hidden=0 AND id=?;''',
                (ident))
        elif not hidden and playlist:
            c.execute(
                '''SELECT * FROM songs WHERE hidden=0 AND playlist=?;''',
                (playlist))
        elif not hidden:
            c.execute(
                '''SELECT * FROM songs WHERE hidden=0;'''
                )
        else:
            c.execute(
                '''SELECT * FROM songs;'''
                )
        output = c.fetchall()
        output = [dict(x) for x in output]
        self.closeConnection()
        return output

    def getSong(self, ident=None, playlist=None):
        """Get a single song from the database."""
        return self.getSongs(hidden=True, ident=ident, playlist=playlist)

    def addSong(self, playlist, title, artist, genre, image_url=None, thing_from=None, hidden=False, background=False):
        """Add a song to the database."""
        self.openConection()
        self.conn.execute(
                '''INSERT INTO songs
                (playlist, title, artist, genre, from, image_url, hidden, background)
                VALUES (?,?,?,?,?,?,?,?);''', 
                (playlist, title, artist, genre, thing_from, image_url, hidden, background)
                )
        self.closeConnection()
        return

    def removeSong(self, ident):
        """Removes a song from the database."""
        self.openConnection()
        self.conn.execute(
                '''DELETE FROM songs WHERE id=?;''', (ident)
                )
        self.closeConnection()
        return

    def modifySong(self, ident, songInfo):
        """Modifies a song in the database. songInfo is a modified
        dictionary originally from getSongs."""
        self.openConnection()
        self.conn.execute(
                '''UPDATE songs SET playlist=?, title=?, artist=?, genre=?,
                from=?, image_url=?, hidden=?, background=? WHERE id=?''',
                (songInfo['playlist'], songInfo['title'], songInfo['artist'],
                    songInfo['genre'], songInfo['from'], songInfo['image_url'], 
                    songInfo['hidden'], songInfo['background'], songInfo['id'])
                )
        self.closeConnection()
        return

        
class alux():
    def __init__():
        with open('config.json', 'r') as f:
            self.config = json.load(f)
        self.db = db()

    def checkAuth(self, username, password):
        """Checks if a user gives the correct username and password.
        Passwords are a salted, hashed, sha256 string in the db.
        """
        userInfo = self.db.getUser(username=username)
        if userInfo:
            if userInfo['password'] == hashlib.sha256(
                    str.encode("{0}{1}".format(password, config['salt']))
                    ).hexdigest():
                return userInfo['id']
        return False

    def setCookieToUid(self, uid, cookie_id, expiration):
        """Sets a given cookie ID, which should always be set on
        the client, to a given user, so they don't have to log in again."""
        userInfo = self.db.getUser(uid=uid)
        userInfo['cookie_id'] = cookie_id
        userInfo['expiration'] = expiration
        self.db.modifyUser(uid=uid, userInfo)
        return

    def checkUserAuthed(self, cookie_id):
        """Checks if a user is authenticated based on the cookie id they have
        set."""
        return self.db.getUser(cookie_id=cookie_id)

    def getPlaylists(self, hidden=False):
        """Get all playlist in the database, if hidden is false, do not return
        hidden playlists."""
        return db.getSongs(hidden=hidden, ident=None)

    def getPlaylist(self, ident=None, playlist=None):
        """Get a single playlist in the database."""
        return db.getSong(ident=ident, playlist=playlist)

    def getNewPlaylists(self):
        """Gets all playlists from FPP that are not already in the database."""
        current = self.getPlaylists(hidden=True)
        r = requests.get(
                "{0}/fppxml.php?command=getPlayLists".format(self.config['fppUrl']),
                auth=(self.config['fppUser'], self.config['fppPass'])
                )
        root = et.fromstring(r.text)
        playlists = [child.text for child in root]
        return playlists

    def checkPlayingStatus(self, background=False):
        """Checks if something is playing. If background is false, do not return
        background playlists."""
        r = requests.get(
                "{0}/fppxml.php?command=getPlayLists".format(self.config['fppUrl']),
                auth=(self.config['fppUser'], self.config['fppPass'])
                )
        root = et.fromstring(r.text)
        status = root.find("./fppStatus").text
        if status != "0":
            playlist = root.find("./CurrentPlaylist").text
            time_remaining = int(root.find("./SecondsRemaining").text)
            time_since_start = int(root.find("./SecondsPlayed").text)
        else:
            return {"playing": False}
        song = db.getSong(playlist=playlist)
        if not background and song['background'] == 1:
            return {"playing": False}
        song['playing'] = True
        song['time_remaining'] = time_remaining
        song['time_since_start'] = time_since_start
        return song

    def checkPlayPossible(self):
        """Checks if we can play something. Currently assumes play is possible
        if any background playlist is playing, otherwise assumes no. This might
        need to change to be a configurable time period, later. If we're playing
        a song, return the song instead."""
        song = self.checkPlayingStatus(background=True)
        if not song['playing']:
            return False
        elif song['background'] != 1:
            return song
        return True

    def playPlaylist(self, ident=None, playlist=None, repeat=False):
        """Plays a given playlist given it's db ID or playlist name.
        If repeat is given, repeats the song."""
        if ident:
            playlist = db.getSong(ident=ident)['playlist']
        if repeat:
            requests.get(
                    "{0}/fppxml.php?command=startPlaylist&playlist={1}&repeat=checked".format(
                        self.config['fppUrl'], playlist),
                    auth=(self.config['fppUser'], self.config['fppPass'])
                    )
        else:
            requests.get(
                    "{0}/fppxml.php?command=startPlaylist&playlist={1}".format(
                        self.config['fppUrl'], playlist),
                    auth=(self.config['fppUser'], self.config['fppPass'])
                    )
        return

    def stopPlaylist(self):
        """Stops all playlists from playing."""
        requests.get(
                "{0}/fppxml.php?command=stopNow".format(
                    config['fppUrl']),
                auth=(config['fppUser'], config['fppPass'])
                )
        return

    def addPlaylist(self, playlist, title, artist, genre, image_url=None, thing_from=None, hidden=False, background=False):
        """Adds a playlist to the database."""
        db.addSong(playlist, title, artist, genre, image_url, thing_from, hidden, background)
        return

    def removePlaylist(self, ident):
        """Removes a playlist from the database."""
        db.removeSong(ident)
        return

    def modifyPlaylist(self, ident, songInfo):
        """Modifies a song in the database. songInfo is a modified dictionary
        originally from getPlaylist"""
        db.modifySong(ident, songInfo)
        return
