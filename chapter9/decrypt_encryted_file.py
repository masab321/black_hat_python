from cryptor import decrypt

with open("git_trojan_encrypted", "rb") as f1:
    content = f1.read()

with open("git_trojan.py", "wb") as f2:
    f2.write(decrypt(content))
