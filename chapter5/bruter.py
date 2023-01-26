import queue
import requests
import threading
import sys

AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:19.0) Gecho/20100101 Firefox/19.0"
EXTENSIONS = [".php", ".bak", ".orig", ".inc"]
TARGET = "http://testphp.vulnweb.com"
THREADS =50
WORDLIST = "./all.txt"

def get_words(resume=None):
    words = queue.Queue()
    
    def extend_words(word):
        if "." in word:
            words.put(f"/{word}")
        else:
            words.put(f"/{word}/")

            for extension in EXTENSIONS:
                words.put(f"/{word}{extension}")

    with open(WORDLIST) as f:
        raw_words = f.read()

    for word in raw_words.split():
        if resume is not None:
            if word == resume:
                resume = None

                print(f"Resuming wordlist from: {word}. Press return to continue.")
                sys.stdin.readline()

        else:
            print(word)
            extend_words(word)
 
    return words

def invisible_character_check(url):
    for c in url:
        if len(repr(c)) != 3:
            print(url)

            print("Press return to continue.")
            sys.stdin.readline()

            return


def dir_bruter(words):
    headers = {"User-Agent": AGENT}
    
    while not words.empty():
        url = f"{TARGET}{words.get()}"

        try:
            r = requests.get(url, headers=headers)

        except requests.exceptions.ConnectionError:
            sys.stderr.write("x")
            sys.stderr.flush()
            continue

        if r.status_code == 200:
            invisible_character_check(url)
            print(f"\nSuccess ({r.status_code}: {url})")

        elif r.status_code == 404:
            sys.stderr.write(".")
            sys.stderr.flush()

        else:
            invisible_character_check(url)
            print(f"{r.status_code} => {url}")

if __name__ == "__main__":
    words = get_words()

    print("Press return to continue.")
    sys.stdin.readline()

    for _ in range(THREADS):
        t = threading.Thread(target=dir_bruter, args=(words,))
        t.start()
