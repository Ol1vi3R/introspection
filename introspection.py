import sys
import os
from tqdm import tqdm
import time
import re
import requests
import threading
from threading import Lock
import random
import socket
from urllib.parse import urlparse
import urllib.request
import urllib.error
from scapy.all import *
from concurrent.futures import ThreadPoolExecutor
import ssl
from queue import Queue


RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
BOLD = "\033[1m"
BLACK_TEXT = "\033[30m"
YELLOW_BACKGROUND = "\033[43m"
GREEN_BACKGROUND = "\033[42m"
RESET = "\033[0m"


start_port = 1
end_port = 65535

score_200 = 0
score_301 = 0
score_403 = 0

key_words = ['admin','login','private','administration','secure','wp','wp-admin','wp-login','prive','robot','.htaccess','.htpassword','passwd','.ht']

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.1234.56 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.1234.56 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; Pixel 3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.1234.56 Mobile Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:100.0) Gecko/20100101 Firefox/100.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188',
    'Mozilla/5.0 (X11; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.92 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_0_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.1 Safari/605.1.15',
    'Mozilla/5.0 (Android 13; Mobile; rv:68.0) Gecko/68.0 Firefox/116.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.1234.56 Safari/537.36 Edg/100.0.123.456',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.1234.56 Safari/537.36 OPR/100.0.1234.56',
    'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.1234.56 Safari/537.36 OPR/100.0.1234.56',
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; fr; rv:1.8.1) VoilaBot BETA 1.2 (support.voilabot@orange-ftgroup.com)',
    'Opera/9.80 (Windows NT 6.2; Win64; x64) Presto/2.12.388 Version/12.15',
    'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_1 like Mac OS X; en-us) AppleWebKit/532.9 (KHTML, like Gecko) Version/4.0.5 Mobile/8B117 Safari/6531.22.7 (compatible; Googlebot-Mobile/2.1; +http://www.google.com/bot.html)',
    'Xenu Link Sleuth/1.3.8',
    'Mozilla/5.0 (compatible; Exabot/3.0; +http://www.exabot.com/go/robot)',
    'Mozilla/5.0 (X11; U; Linux x86; fr-fr) Gecko/20100423 Ubuntu/10.04 (lucid) Firefox/3.6.3 AppleWebKit/532.4 Safari/532.4',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0'

]

print_lock = Lock()
def scan_url(wordlist_slice, base_url, progress_bar):
    global score_200
    global score_301
    global score_403
    for word in wordlist_slice:
        try:
            url = base_url + word
            if any(key_word in word for key_word in key_words):
                word = YELLOW_BACKGROUND + BLACK_TEXT + word
            headers = {'Accept': '*/*', 'User-Agent': random.choice(user_agents)}
            response = requests.head(url, headers=headers)
            with print_lock:
                if response.status_code == 200:
                    tqdm.write(GREEN + f"200 OK : {base_url}{word}" + RESET)
                    score_200 += 1
                elif response.status_code == 301:
                    tqdm.write(BLUE + f"301 REDIRECT : {base_url}{word}" + RESET)
                    score_301 += 1
                elif response.status_code == 403:
                    tqdm.write(RED + f"403 RESTRICTED : {base_url}{word}" + RESET)
                    score_403 += 1
        except requests.RequestException:
            pass
        finally:
            progress_bar.update(1)

def scanner(url):
    with open('wordlist.txt', 'r') as file:
        wordlist = file.read().splitlines()

    num_threads = 50
    wordlist_slices = [wordlist[i::num_threads] for i in range(num_threads)]

    with tqdm(total=len(wordlist), desc="Progression") as progress_bar:
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            for wordlist_slice in wordlist_slices:
                executor.submit(scan_url, wordlist_slice, url, progress_bar)

    
    

def url_resolve(url):
    domain = urlparse(url).netloc
    return domain

def url_resolve_path(url):
    path = urlparse(url).path
    return path

def get_ip_address(domain):
    ip_address = socket.gethostbyname(domain)
    return ip_address


def r():
    if len(sys.argv) < 2:
        print("Usage: {} <TargetURL>".format(sys.argv[0]))
    else:
        if isValideUrl(sys.argv[1]):
            if url_existe(sys.argv[1]):
                show(sys.argv[1])
                pass
            else:
                print(RED+"-------- URL does not exist --------"+RESET)
        else:
            print("Usage: {} <TargetURL>".format(sys.argv[0]))
            print(RED+"-------- Invalid URL --------"+RESET)

def url_existe(url):
    b=False
    try:
        reponse = requests.get(url, timeout=5, headers={'Accept': '*/*'}, allow_redirects=False)
        print(reponse.status_code)
        if reponse.status_code == 200 or 406:
            b = True
    except:
        pass
    return b

def isValideUrl(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:\S+(?::\S*)?@)?'
        r'(?:[\dA-Za-z-]+\.)+[A-Za-z]{2,6}'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

def show(url):
    os.system('cls' if os.name == 'nt' else 'clear')
    if url.endswith('/'):
        pass
    else:
        url = url+"/"
    print(BOLD+RED + """
  _____       _                                 _   _             
 |_   _|     | |                               | | (_)            
   | |  _ __ | |_ _ __ ___  ___ _ __   ___  ___| |_ _  ___  _ __  
   | | | '_ \| __| '__/ _ \/ __| '_ \ / _ \/ __| __| |/ _ \| '_ \ 
  _| |_| | | | |_| | | (_) \__ | |_) |  __| (__| |_| | (_) | | | |
 |_____|_| |_|\__|_|  \___/|___| .__/ \___|\___|\__|_|\___/|_| |_|
                               | |                                
                               |_|                                
""" + RESET)
    print(YELLOW + BOLD +"----------")
    print("|"+ RESET +" by OdG "+YELLOW+BOLD+"|")
    print("----------"+RESET)
    print("")
    print(BOLD+"Target URL --------> " +RED+url+RESET)
    print("")
    domain = url_resolve(url)
    path = url_resolve_path(url)
    ip = get_ip_address(domain)
    print("Domain : " + domain)
    print("Path : " + path)
    print("IP : " + ip)
    print("Scanner started...")
    scanner(url)
    print("\n\n"+GREEN_BACKGROUND+BLACK_TEXT+"Scan completed"+RESET+"\n")
    print(BOLD+f"""Scores :    200 OK : {score_200} founded
            301 REDIRECT : {score_301} founded
            403 RESTRICTED : {score_403} founded""")


if __name__ == "__main__":
    r()