# save-geekmails
Download Geekmails from BGG/RPGG/VGG

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

Advanced bash usage to batch download multiple pages at once:

```bash
for i in {1..5}; do python SaveGeekmails.py Inbox $i; done
```
