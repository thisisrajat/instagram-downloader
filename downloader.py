from sys import argv, exit
import urllib, json
import subprocess



# Global Declaration

ACCESS_TOKEN = r'2912979.87fdd31.0949d22f4a714349ae84643c5af165ef'
image_urls = []
resolution = ""
file_format = ""
uid = ""
username = ""

# Return JSON dict
def getJson( url ):
  return json.loads( urllib.urlopen( url ).read() )


# Get ID by Username
def getID():
  
  global username, ACCESS_TOKEN

  url = 'https://api.instagram.com/v1/users/search?q={}&access_token={}'.format(username, ACCESS_TOKEN)
  
  print "Checking Username..."
  
  data = getJson(url)
  
  if data['meta']['code'] == 200:
    try:
      print "Found => %s" % (format(data['data'][0]['full_name']).encode('utf-8'))
    except:
      print "Username error."
      exit(0)

  else :
    print "Username not found"
    exit(0)

  return data['data'][0]['id']



# Download URL into username/{name} folder
def download(url, name, username):
  urllib.urlretrieve(url, '{}/{}.png'.format(username, name))


# Load settings
def settingsLoad(user):

  global resolution, file_format, uid, username
  settings = json.loads( open('settings.conf').read() )
  file_format = settings['file_format']
  resolution = str(settings['resolution'])
  username = user
  uid = getID()


# Fetch Urls
def fetchUrls(onlyOneRequest):

  global resolution, uid, ACCESS_TOKEN

  url = "https://api.instagram.com/v1/users/{}/media/recent/?access_token={}".format(uid, ACCESS_TOKEN)
    
  print "Fetching images url"

  while(True):
    
    print "."

    data = json.loads( urllib.urlopen( url ).read() )
    
    if data['meta']['code'] == 200:

      MAX = len(data['data'])
      i = 0
      
      while(i < MAX):
        image_urls.append( data['data'][i]['images']['{}'.format(resolution)]['url'] )
        i += 1
      

      if onlyOneRequest == True:
        break

      try:
       url = data['pagination']['next_url']
      except:
        break

    elif data['meta']['code'] == 400:
      print "User is private. Can't Download"
      exit(0)



# Download images
def batchDownload():
  subprocess.Popen('mkdir {}'.format(username), shell=True)

  print "Downloading images now..."

  i = 0;

  for image in image_urls:
    i += 1
    download(image, i, username)
    print "."

  print "Done. Exiting Now."


# Save all the urls to a file
def saveToFile():
  print "Saving to file..."
  pointer = open('{}-urls.txt'.format(username), 'w')
  for url in image_urls:
    pointer.write( str(url) )
    pointer.write( str('\n') )
  exit(0)


# Print Help
def printHelp():
  print 'usage: python downloader.py [username] [--save-only] [[all] [recent]]'
  print 'all : Download all of the images'
  print 'recent : Download only the recent images'
  print 'popular : Download only the popular images'
  print '--save-only : Only save the image urls, and not download any of them'
  print 'username : User\'s username on instagram. Also referrerd to as handlename.'
  exit(0)


# Download all the images
def all(saveOnly):

  fetchUrls(False)
  if saveOnly == True:
    saveToFile()
  else:
    batchDownload()


# Download only the recent ones
def recent(saveOnly):
  
  fetchUrls(True)
  if saveOnly == True:
    saveToFile()
  else:
    batchDownload()


# Choose which function to call according to arguments
def choose(username, mode, saveOnly):
  settingsLoad(username)

  if mode == 'all':
    all(saveOnly)
  elif mode == 'recent':
    recent(saveOnly)
  else:
    printHelp()


# Standard boilerplate to call appropriate functions
if __name__ == '__main__':
  
  length = len(argv)

  # [0] - filename
  # [1] - username
  # [2] - --save-only
  # [3] - recent, all

  if length == 1 or length > 4 or argv[1] == '--help': 
    printHelp()

  else:
    if length == 2:
      choose(argv[1], 'all', False)
    elif argv[2] == '--save-only':
      choose(argv[1], argv[3], True)
    else:
      choose(argv[1], argv[2], False)
