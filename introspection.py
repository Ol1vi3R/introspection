import sys
import os
from tqdm import tqdm
import time
import re
import requests
import threading


RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
BOLD = "\033[1m"
RESET = "\033[0m"

headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

def run(url):
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

    with open('wordlist.txt', 'r') as file:
        wordlist = file.read().splitlines()

    for i in tqdm(wordlist, desc="Progression"):
        resultat=""
        try:
            url2 = url + i
            reponse = requests.get(url2, timeout=5, headers={'Accept': '*/*'}, allow_redirects=False)
            if reponse.status_code == 200:
                resultat = GREEN + f"200 OK : {url2}" + RESET
            elif reponse.status_code == 301:
                resultat = BLUE + f"301 REDIRECT : {url2}" + RESET
            elif reponse.status_code == 403:
                resultat = RED + f"403 RESTRICTED : {url2}" + RESET
        except requests.RequestException:
            pass
        
        if resultat != "":
            tqdm.write(resultat)

def r():
    if len(sys.argv) < 2:
        print("Usage: {} <TargetURL>".format(sys.argv[0]))
    else:
        if est_url_valide(sys.argv[1]):
            if url_existe(sys.argv[1]):
                run(sys.argv[1])
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

def est_url_valide(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:\S+(?::\S*)?@)?'
        r'(?:[\dA-Za-z-]+\.)+[A-Za-z]{2,6}'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None


if __name__ == "__main__":
    r()