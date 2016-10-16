#!/usr/bin/env python3
from bottle import route, get, run, default_app, template, static_file, post,  put, delete, request, response, redirect, TEMPLATE_PATH
from alux import alux 
import os, time, sys, datetime, requests, json, uuid, hashlib

pwd = os.getcwd()
#Add the template path if it's not there
if pwd + '/views/' not in TEMPLATE_PATH:
    TEMPLATE_PATH.insert(0,pwd + '/views/')

cookieSig="2qn3h8gew9qgew9q8fe9wq8hfeiowqpjfiopeq"

with open('config.json', 'r') as f:
    config = json.load(f)

#Root and static stuff
@get('/static/<filename:path>')
def serve_static(filename):
    return static_file(filename, root=pwd+'/static/')

# Main Web Responses
@get('/')
def index():
    cookieid = request.get_cookie("alux_id", secret=cookieSig)
    if not cookieid:
        new_id = getid()
        response.set_cookie(
                "alux_id", new_id['alux_id'], 
                expires=new_id['expiration'], secret=cookieSig
                )
    playcheck = alux.checkPlayPossible()
    playlists = alux.getPlaylists()
    return template('default', radioStation = config['radioStation'], userinfo=userinfo, playing=playcheck, playlists=playlists, error=False)
    
# API Endpoints
@put('/play')
def play():
    this_request = request.json
    playcheck = alux.checkPlayPossible()
    if playcheck and not isinstance(playcheck, dict):
        if getPlaylist(ident=this_request['id']):
            alux.playPlaylist(ident=this_request['id'], repeat=this_request['repeat'])
            response.status = 205
            return
        response.status = 404
        return
    response.status = 409
    return

@delete('/stop')
def stop():
    alux.stopPlaylist()
    response.status = 205
    return

@get('/status')
def status():
    playing = alux.checkPlayingStatus()
    reponse.status = 200
    return playing

@get('/get')
def getplaylists():
    hidden = False
    cookie_id = request.query.alux_id
    if alux.checkUserAuthed(cookie_id):
        hidden = True
    playing = alux.getPlaylists(hidden=hidden)
    response.status = 200
    return playing

@get('/alux_id')
def getid():
    return {"alux_id": hashlib.sha512(str(uuid.uuid4()).encode('utf-8')).hexdigest(), "expiration": int(time.time())+2628000}

@post('/authenticate')
def authenticate():
    this_request = request.json
    myid = alux.checkAuth(this_request['username'], this_request['password'])
    if myid:
        alux.setCookieToUid(myid, this_request['alux_id'], this_request['expiration'])
        response.status = 205
        return
    response.status = 401
    return

@put('/add')
def add():
    cookie_id = request.query.alux_id
    if not alux.checkUserAuthed(cookie_id):
        response.status = 401
        return
    this_request = request.json
    alux.addPlaylist(this_request['playlist'], this_request['title'], this_request['artist'], this_request['genre'], this_request['image_url'], this_request['thing_from'], this_request['hidden'], this_request['background'])
    playlist = alux.getPlaylist(playlist=this_request['playlist'])
    response.status = 401
    return {'id': playlist['id']} 

@delete('/remove')
def remove():
    cookie_id = request.query.alux_id
    if not alux.checkUserAuthed(cookie_id):
        response.status = 401
        return
    this_request = request.json
    alux.removePlaylist(this_request['id'])
    response.status = 204
    return

@get('/listnew')
def listnew():
    cookie_id = request.query.alux_id
    if not alux.checkUserAuthed(cookie_id):
        response.status = 401
        return
    playlists = alux.getNewPlaylists()
    response.status = 200
    return {'playlists':playlists}

@put('/modify')
def modify():
    cookie_id = request.query.alux_id
    if not alux.checkUserAuthed(cookie_id):
        response.status = 401
        return
    this_request = request.json
    alux.modifyPlaylist(this_request['id'], this_request)
    response.status = 201
    return {'id': this_request['id']}

if __name__=="__main__":
    run(host="0.0.0.0",port="8081")
else:
    application = default_app()
