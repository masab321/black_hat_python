import urllib2

url = 'https://www.google.com'

response = urllib2.urlopen(url)

print(response.read())

response.close()
