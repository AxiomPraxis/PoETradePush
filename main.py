from pathlib import Path
import os
import time
import http.client
import urllib
import re
import logging

# Fill out the APItoken and APIuser environment variables with your
# Token and User from Pushover.

APItoken = os.environ('APIToken')
APIuser = os.environ('APIuser')

# Fill out your path to the Client.txt file

pathy = Path("F:/SteamLibrary/steamapps/common/Path of Exile/logs/")
clientfilename = pathy / "Client.txt"

logging.basicConfig(filename='tradepush.log', level=logging.INFO)
logging.info(' Init variables')

logging.info(f' Pointing to SteamLibrary at: {clientfilename}')

pattern = r'From\s(<?.*?>)?\s?(.*?):\s(Hi,\s.*)'

logging.info(f' Following regex pattern: {pattern}')
# logging.info(f' APItoken: {APItoken}')
# logging.info(f' APIuser: {APIuser}')

# Logging of the APItoken and APIuser disabled by default,
# uncomment them to enable.


def follow(clientfilename):
    clientfilename.seek(0, 2)
    while True:
        line = clientfilename.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line
        match = re.search(pattern, line)
        if match:
            messageToPush = match.group()
            print(f"{match.group()}")
            logging.info(messageToPush)
            pushmessage(messageToPush)


def pushmessage(messageToPush):
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
                 urllib.parse.urlencode({
                                         "token": f"{APItoken}",
                                         "user": f"{APIuser}",
                                         "message": f"{messageToPush}",
                                         "sound": "cashregister",
                                        }),
                 {"Content-type": "application/x-www-form-urlencoded"})
    conn.getresponse()


if __name__ == '__main__':
    clientfile = open(clientfilename, "r")
    clientlines = follow(clientfile)
    for line in clientlines:
        print(line)
