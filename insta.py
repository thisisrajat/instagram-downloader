from sys import argv, exit
import urllib, json
import subprocess

ACCESS_TOKEN = r'2912979.87fdd31.0949d22f4a714349ae84643c5af165ef'
image_urls = []

def getID(username):
  
  url = 'https://api.instagram.com/v1/users/search?q={}&access_token={}'.format(username, ACCESS_TOKEN)
  
  print "Checking ..."
  
  data = json.loads( urllib.urlopen( url ).read() )
  
  if data['meta']['code'] == 200:
    print "Found => {}".format(data['data'][0]['full_name'])
  
  else :
    print "Username not found"

  return data['data'][0]['id']


def download(url, name, username):
  urllib.urlretrieve(url, '{}/{}.png'.format(username, name))

def main(username):
  
  id = getID(username)
 
  url = "https://api.instagram.com/v1/users/{}/media/recent/?access_token={}".format(id, ACCESS_TOKEN)
    
  print "Fetching images url"

  while(True):
    
    print "."

    data = json.loads( urllib.urlopen( url ).read() )
    
    if data['meta']['code'] == 200:

      MAX = len(data['data'])
      i = 0
      
      while(i < MAX):
        image_urls.append( data['data'][i]['images']['standard_resolution']['url'] )
        i += 1
      
      try:
       url = data['pagination']['next_url']
      except:
        break

    elif data['meta']['code'] == 400:
      print "User is private. Can't Downlaod"
      exit(0)
    
  subprocess.Popen('mkdir {}'.format(username))

  print "Downloading images now..."

  i = 0;

  for image in image_urls:
    i += 1
    download(image, i, username)
    print "."

  print "Done. Exiting Now"


if __name__ == '__main__':
  if len(argv) == 2:
    main(argv[1])
  else :
    print "Usage:\npython insta.py username"