# README

## Server Info

By default the server is running on [http://10.52.247.154:8000/](http://10.52.247.154:8000/) and can be accessed via the browser.

The server is running in development mode, however this is not advised. I think it will be fine, but if possible, launch it properly with a WSGI server (https://www.youtube.com/watch?v=YFBRVJPhDGY).

## SSH to remote server
To ssh into the remote server do `ssh rattool@10.52.247.154`. I have set up `cd ~/Documents/BAT_RAT` in `~/.profile` to automatically navigate to the folder 
of the BAT_RAT app.

## Copying code to remote server
To copy and paste all code from the current directory of the development machine to the remote server run the script `./scripts/deploy.sh`. 
**Note:** This intentionally does not copy the `venv` folder or the `requirements.txt` since these are different on Windows and Unix based systems.

## Reinstall Python Packages
Whilst SSH'd into the remote server, to reinstall all the python packages (`venv`) simply run `./scripts/reinstall_venv.sh` from within `~/Documents/BAT_RAT`.

## Running the server
Whilst SSH'd into the remote server, to run the HTTP server run `./run.sh` from within `~/Documents/BAT_RAT`. Once the server is running if you press `Ctrl + C` in the shell, the server will stop running, so do *NOT* do this. To keep the server running in the background you must close the shell by pressing the `X` in the rop right corner.

## Troubleshooting
### See Processes
To see a list of IP[v4,v6] processes use `lsof -i`. If the server is running you should see something like:

```
python  11162 rattool    3u  IPv4  68912      0t0  TCP *:5000 (LISTEN)
python  11163 rattool    3u  IPv4  68912      0t0  TCP *:5000 (LISTEN)
python  11163 rattool    4u  IPv4  68912      0t0  TCP *:5000 (LISTEN)
```

### Restarting The Server
To kill a process run `kill -9 [pid]`. Kill any processes present and the follow the steps above for running the server.

### Viewing Logs
To view server logs in realtime from the server run `tail -f logs/log.txt` from within the `~/Documents/BAT_RAT` directory. The logs are 
hardcoded at debug level.
