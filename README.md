# A.Lux
The public web front-end for the [Falcon Pi Player](https://github.com/FalconChristmas/fpp)

A.Lux allows you to to have a smartphone-friendly easy-to-use interface for your
light display without exposing your falcon pi player itself to the world. It is
written as a python wsgi script, so you can run it with uwsgi, gunicorn, or any
other number of wsgi servers.

## Dependencies
These are also in the requirements.txt file, and can be installed with

    pip3 install -r requirements.txt

on most systems.

* bottle
* requests
* Pillow
* goldfinch

## Docker
A.Lux is available as a docker container to make deployment simpler. Using it is
simple:

    docker run -d -v /path/to/config.json:/alux/config.json -p 80:80 --name alux kuroshi/alux 

I recommend running a reverse proxy in front of it (such as 
[jwilder/nginx-proxy](https://github.com/jwilder/nginx-proxy) for example) for 
SSL/TLS. 

## Installation
There isn't a nice package for it now, outside of docker. You will need to
configure a wsgi server and a web server to server index.py in this repository.

There is no default user, but a username and password is basically required to
interact with the instance outside of the public view. This is the most challenging
part of installation, as you will have to generate a username and password by hand.

First, you will need to create an sha512 hash of your password with the salt
you choose. You can use python for this like so:

    import hashlib
    hashlib.sha512(str.encode("my_password_and_salt_with_no_spaces_between_them").hexdigest())

Keep that handy for now.

The first time the page is opened, it will generate an 'alux.sqlite' file in the 
db directory. Open this up with the command `sqlite3 alux.sqlite`. You may need
to install the sqlite packages (If you are using the docker container, you will
need to install the sqlite packages. Get into the container with 
`docker exec -ti alux /bin/bash` and run `apt-get install sqlite` to install the
sqlite packages). Once in the sqlite command line, run this command to add the
username and password:

    INSERT INTO users ('username', 'password') VALUES ('your_username', 'hash_generated_earlier');

## Configuration
Configuring A.Lux is mostly pretty easy. There's a `config.json.example` file in 
the root of the repository that has all of the base key/value pairs. Here's the 
example file:

    {
        "radioStation": "88.1 FM",
        "fppUrl": "http://fpp",
        "fppUser": "admin",
        "fppPass": "",
        "salt": "insert_random_string_here",
        "background": "background_playlist_name"
    }

* `radioStation` is the radio station people will tune into to hear your music.
   It is only used for display purposes.
* `fppUrl` is the URL of the Falcon Pi Player on your network. The default,
  `http://fpp`, is usually sufficent as FPP will configure itself as such on
  most networks, but in some cases you may need to replace 'fpp' with the Pi's
  IP address.
* `fppUser` is the username to get into your FPP instance. This is not optional
  for now, so you will need to configure FPP with a username and password.
* `fppPass` is the password for the above user. It's stored in plaintext, so 
  don't use an important one.
* `salt` is a random string that is used to salt passwords in the database.
* `background` is the FPP playlist name that will be considered the 'background'
  playlist, or the playlist to run when a song isn't going.

## Problems
If you have any problems, go ahead and make an issue on github. Also feel free
to make an issue for any enhancements or bug requests you would like looked at.
I literally just now created an account on falconchristmas.com, so if you want
to ping me there please feel free, though I doubt I will check it often.

