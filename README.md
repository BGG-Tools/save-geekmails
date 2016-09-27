# save-geekmails
Download Geekmails from BGG/RPGG/VGG

This script will download your geekmails and save them as text files in the same directory.
If a message has already been downloaded before (and the text file already exists), it will be skipped during this process.

The text files use their message ID as file name, so you can easily search within those text files and then load the rendered version on BGG. For example, to view 12345.txt on BGG, open it at http://boardgamegeek.com/geekmail/message/12345

Configuration
=============

Edit the line where the session.post() call is being made to match your login and password. You could use a cookie, too.

Usage
=====

```
$ python SaveGeekmails.py -h
usage: SaveGeekmails.py [-h] [page] [folder]

Download Geekmails from BoardGameGeek

positional arguments:
  page        Geekmail page # (default: 1)
  folder      Geekmail folder (default: Inbox)

optional arguments:
  -h, --help  show this help message and exit
```

To download all your latest geekmails from your Inbox, just use
```
python SaveGeekmails.py
```
To download from your Outbox folder instead, use
```
python SaveGeekmails.py Outbox
```
Downloading geekmails from a different page:
```
python SaveGeekmails.py 5
```

It is possible to mix and swap those parameters, so instead of
```
python SaveGeekmails.py 3 Outbox
```
one can also use (through very ugly hacks in the code to process the command line)
```
python SaveGeekmails.py Outbox 3
```

Advanced bash usage to batch download multiple pages at once:

```bash
for i in {1..5}; do python SaveGeekmails.py $i Inbox; done
```

Support
=======

For discussion or support requests with this code, go to https://boardgamegeek.com/thread/1644910/downloading-geekmails-disk
