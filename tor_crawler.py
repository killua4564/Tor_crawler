
import os
import re
import sys
import socks
import socket
import subprocess

from json import load
from bs4 import BeautifulSoup
from urllib.request import urlopen

def checkTor():
  checkTor = str(subprocess.check_output(['ps', '-e']), 'utf-8')
  if re.compile(r'\b({0})\b'.format('tor'), flags=re.IGNORECASE).search(checkTor):
    print("## TOR is ready!")
  else:
    print("## TOR is NOT running!")
    sys.exit(2)

def checkIP():
  try:
    webIPcheck = 'https://api.ipify.org/?format=json'
    my_ip = load(urlopen(webIPcheck))['ip']
    print('## Your IP: ' + my_ip)
  except:
    print( "Error: IP can't obtain \n## Is " + webIPcheck + "up?")
    sys.exit(2)

def connectTor():
  def getaddrinfo(*args):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]
  checkIP() 
  checkTor()
  socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, '127.0.0.1', 9050)
  socket.socket = socks.socksocket
  socket.getaddrinfo = getaddrinfo

def crawl_page(link, link_dir):
  os.system('mkdir ' + link_dir)
  soup = BeautifulSoup(urlopen(link).read(), "html.parser")
  for tr in soup.select("tr")[3:-1]:
    next_link = "/" + tr.select("td")[1].select('a')[0]['href']
    if tr.select("td")[0].select("img")[0]['src'] == '/icons/folder.gif': # is a folder
      crawl_page(link + next_link, link_dir + next_link)
    else: # is a file
      open(link_dir + next_link, 'wb').write(urlopen(link + next_link).read())

if __name__ == '__main__':
  connectTor()
  crawl_page("http://iec56w4ibovnb4wc.onion/Library", "./crawler")
