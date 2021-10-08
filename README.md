# Readme

## SSH to remote server
To ssh into the remote server do `ssh rattool@10.52.247.154`
with password: `London2012`. I have set up `cd ~/Documents/BAT_RAT` in `~/.profile` to automatically navigate to the folder 
of the RAT app.

## Installing Python Packages
### On the Development Machine

If you install a new python package on the development machine make sure you first are using
(venv) by running `source venv/Scripts/activate` and then running `pip install [packagename]`. If you need to create a
text file with a list of the required python packages then run `pip freeze > requirements.txt` (this text file tells 
you which packages need installing for the app to work).

### On the Remote Server
To install packages on the remote server you must use a proxy; `proxy.esl.cisco.com` should work. Run 
`pip install [packagename] --proxy proxy.esl.cisco.com` on the remote server to install a specific package or 
`pip install -r requirements.txt --proxy proxy.esl.cisco.com` to install all the required python packages.

## Copying code to remote server
To copy and paste all code to the remote server run the script `./deploy.sh`. **Note:** This intentionally does not copy the
`venv` folder since this is different on Windows and Unix based systems.

## Reinstall venv on the server
If you ever need to reinstall the virtual environment (venv) on the server run:
1. `rm -rf venv` (to remove `venv`)
2. `virtualenv venv` (reinitialise `venv`)
3. `source venv/bin/activate` (to use `venv`)
4. `pip install -r requirements.txt --proxy proxy.esl.cisco.com` (to install all the packages in `requirements.txt`)

## Running the server
To run the HTTP server run `./run.sh` from within `~/Documents/RAT`.

## Troubleshooting
### See Processes
To see a list of IP[v4,v6] processes use `lsof -i`. If the server is running you should see something like:

```
python  11162 rattool    3u  IPv4  68912      0t0  TCP *:5000 (LISTEN)
python  11163 rattool    3u  IPv4  68912      0t0  TCP *:5000 (LISTEN)
python  11163 rattool    4u  IPv4  68912      0t0  TCP *:5000 (LISTEN)
```

### Kill Process
To kill a process run `kill -9 [pid]`.

### Viewing Logs
To view server logs in realtime run `tail -f logs/log.txt` from within the `~/Documents/RAT` directory. The logs are 
hardcoded at debug level.