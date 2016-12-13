#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
SaveGeekmails - Download Geekmails from BGG/RPGG/VGG

Copyright (c) 2016 BGG-Tools <https://github.com/bgg-tools>

released under the GNU General Public License v3.0

SaveGeekmails is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

SaveGeekmails is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with SaveGeekmails.  If not, see <http://www.gnu.org/licenses/>.
"""

### utf-8 shenanigans
# see http://stackoverflow.com/questions/11741574/how-to-print-utf-8-encoded-text-to-the-console-in-python-3

import sys,codecs,locale
sys.stdout = codecs.getwriter(locale.getpreferredencoding())(sys.stdout)

################################################ Logging ##

import logging
log = logging.getLogger("SaveGeekmails")
log.addHandler(logging.StreamHandler())

if __name__ == '__main__':
	log.setLevel(logging.INFO)
else:
	log.setLevel(logging.ERROR)	# don't blather too much if just being imported elsewhere

############################################### Download ##

import requests
try:
	requests.packages.urllib3.disable_warnings()	# ignore the annoying InsecurePlatformWarnings
except:
	pass

################################################## Parse ##

import re
r_geekmailID = re.compile(r"<div id='message_(\d+)'>")

# https://stackoverflow.com/a/7088472
try:
	from html import unescape			# for Python 3.4+
except ImportError:
	try:
		from html.parser import HTMLParser	# for Python 3.x (<3.4)
	except ImportError:
		from HTMLParser import HTMLParser	# for Python 2.x
	unescape = HTMLParser().unescape

#################################################### I/O ##

import io
import os.path

###########################################################

def get_geekmails(page, folder):
	log.info('Logging in')
	session = requests.session()
	session.post('https://boardgamegeek.com/login', data={"username":"Santa", "password":"password"})

	log.info('Grabbing geekmail index for page %d of folder %s' % (page, folder))
	gmURL = 'https://boardgamegeek.com/geekmail_controller.php?action=viewfolder&ajax=1&folder=%s&pageID=%d' # ajax=0 for debugging in browser
	index = session.get(gmURL % (folder, page))

	if index.status_code != 200:
		log.error("Could not connect to BGG successfully")
		raise IOError("Could not connect to BGG successfully")

	for num in re.findall(r_geekmailID, index.text):
		if os.path.isfile(num+'.txt'):
			continue

		log.info('Grabbing geekmail #'+num)
		r = session.get('https://boardgamegeek.com/geekmail_controller.php?action=forward&ajax=1&messageid='+num)
		text = r.json()['output']
		text = unescape(text[text.find('------------ Forwarded Message -----------')+42:text.find('</textarea>')])

		with io.open(num+'.txt', 'wt', encoding='UTF-8') as f:
			f.write(text.strip())

#################################### Handle command line ##

if __name__ == '__main__':
	# patch up the command line arguments for special cases
	# maybe I should just lose the positional args instead
	if len(sys.argv) > 2 and sys.argv[2].isdigit() and not sys.argv[1].isdigit():
		# assume that the command line arguments page and folder have been swapped
		sys.argv[1], sys.argv[2] = sys.argv[2], sys.argv[1]
	elif len(sys.argv) == 2 and not sys.argv[1].isdigit():
		# assume that this only argument is the folder to use, add page in front
		sys.argv.insert(1, '1')

	# get command line arguments
	import argparse
	parser = argparse.ArgumentParser(description='Download Geekmails from BoardGameGeek')
	parser.add_argument("page", help="Geekmail page # (default: 1)", type=int, nargs='?', default=1)
	parser.add_argument("folder", help="Geekmail folder (default: Inbox)", type=str, nargs='?', default='Inbox')

	get_geekmails(**vars(parser.parse_args()))

