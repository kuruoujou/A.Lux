#!/usr/bin/env python3
from bottle import route, get, run, default_app, template, static_file, post,  put, delete, request, response, redirect, TEMPLATE_PATH
import alux, os, time, sys, datetime, requests, json, uuid, hashlib

pwd = os.getcwd()
#Add the template path if it's not there
if pwd + '/views/' not in TEMPLATE_PATH:
    TEMPLATE_PATH.insert(0,pwd + '/views/')

with open('config.json', 'r') as f:
    config = json.load(f)

alux = alux.alux()

#Root and static stuff
@get('/static/<filename:path>')
def serve_static(filename):
    return static_file(filename, root=pwd+'/static/')

# Main Web Responses
@get('/')
def index():
    alux_id = request.get_cookie("alux_id")
    alux_expiration = request.get_cookie("alux_expiration")
    userInfo = alux.checkUserAuthed(alux_id)
    if not alux_id or not alux_expiration or not userInfo:
        new_id = getid()
        response.set_cookie(
                "alux_id", new_id['alux_id'], expires=new_id['expiration'])
        response.set_cookie("alux_expiration", str(new_id['expiration']), expires=new_id['expiration'])
        userInfo = {'username': None, 'password': None, 'alux_id': new_id['alux_id'], 'expiration': new_id['expiration']}
    playcheck = alux.checkPlayPossible()
    return template('default', radioStation = config['radioStation'], userInfo=userInfo, playcheck=playcheck)

@get('/logout')
def web_logout():
    alux_id = request.get_cookie("alux_id")
    userInfo = alux.checkUserAuthed(alux_id)
    if not alux_id or not userInfo:
        redirect("/")
    alux.deauthorize(alux_id)
    redirect("/")
    
# API Endpoints
@put('/play')
def play():
    this_request = request.json
    playcheck = alux.checkPlayPossible()
    if playcheck:
        if alux.getPlaylist(ident=this_request['id']):
            alux.stopPlaylist()
            alux.playPlaylist(ident=this_request['id'], repeat=this_request['repeat'])
            response.status = 205
            return
        response.status = 404
        return
    else:
        playstatus = alux.checkPlayingStatus()
        alux_id = request.query.alux_id
        if playstatus['playing'] == False and alux.checkUserAuthed(alux_id):
            if alux.getPlaylist(ident=this_request['id']):
                alux.stopPlaylist()
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
    alux.playPlaylist(playlist=config['background'], repeat=True)
    response.status = 205
    return

@get('/status')
def status():
    playing = alux.checkPlayingStatus()
    response.status = 200
    return playing

@get('/get')
def getplaylists():
    hidden = False
    alux_id = request.query.alux_id
    if alux.checkUserAuthed(alux_id):
        hidden = True
    playing = alux.getPlaylists(hidden=hidden)
    response.status = 200
    return {'playlists': sorted(playing, key=lambda k: k['title'])}
    
@get('/get/<ident>')
@get('/get/<ident>/')
def getplaylist(ident=None):
    playing = alux.getPlaylist(ident=ident)
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
 
@post('/logout')
def logout():
    alux_id = request.query.alux_id
    if not alux.checkUserAuthed(alux_id):
        response.status = 401
        return
    this_request = request.json
    alux.deauthorize(this_request['alux_id'])
    response.status = 205
    return

@put('/add')
def add():
    alux_id = request.query.alux_id
    if not alux.checkUserAuthed(alux_id):
        response.status = 401
        return
    this_request = request.json
    alux.addPlaylist(this_request['playlist'], this_request['title'], this_request['artist'], this_request['genre'], this_request['image_url'], this_request['thing_from'], this_request['hidden'], this_request['background'])
    playlist = alux.getPlaylist(playlist=this_request['playlist'])
    response.status = 204
    return {'id': playlist['id']} 

@delete('/remove')
def remove():
    alux_id = request.query.alux_id
    if not alux.checkUserAuthed(alux_id):
        response.status = 401
        return
    this_request = request.json
    alux.removePlaylist(this_request['id'])
    response.status = 204
    return

@get('/listnew')
def listnew():
    alux_id = request.query.alux_id
    if not alux.checkUserAuthed(alux_id):
        response.status = 401
        return
    playlists = alux.getNewPlaylists()
    response.status = 200
    return {'playlists':sorted(playlists)}

@put('/modify')
def modify():
    alux_id = request.query.alux_id
    if not alux.checkUserAuthed(alux_id):
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
