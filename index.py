from PIL import Image
from pycoingecko import CoinGeckoAPI
from pytesseract import *
from twilio.rest import Client
import platform
import os
import pyautogui as pt
import time
import yaml

from src.utils_ import *

############## load files ##############
configFile = open("config.yaml", 'r')
config     =  yaml.safe_load(configFile)

keyFile = open("keys.yaml", "r")
keys    =  yaml.safe_load(keyFile)


############## mapper config ##############
refresh_map_time  = config['refresh_map_time']
refresh_page_time = config['refresh_page_time']
offset = config['set_offset']
traying_time = config['traying_time']


############## global variables ##############
global isLogged
isLogged = False

global isMinnering
isMinnering = False

global timer
timer = 0

global pageTimer
pageTimer = 0

global toHunt
toHunt = False

############## get bcoins ##############
def get_bcoins():

  # Discomment in Windows 
  # if(platform.system() == 'Windows'):
    # pytesseract.tesseract_cmd = r'<tesseract_path_install>\tesseract.exe'
      
  image = getImage_('bcoin_bag.jpg')
  
  if(image != None):
    mouseClick_(image)
    
    if os.path.isfile('total_bcoins.jpg'):
      os.remove('total_bcoins.jpg')
    
    time.sleep(5)

    pt.screenshot('total_bcoins.jpg', region=(720, 520, 200, 60))
    
    img = Image.open('total_bcoins.jpg')
    balance = pytesseract.image_to_string(img)
    balance = balance.replace('\n', ' ').replace('\r', '').replace(',', '.')
    
    os.remove('total_bcoins.jpg')

    image = getImage_('x.jpg')
    mouseClick_(image)

    return float(balance)


############## cryto_price ##############
def bomb_balance():
  balance = get_bcoins()
  
  cg = CoinGeckoAPI()
  bcoin = cg.get_price(ids='bomber-coin', vs_currencies='usd,brl')

  bcoinUsd = bcoin['bomber-coin']['usd']
  bcoinBrl = bcoin['bomber-coin']['brl']

  balanceUsd = balance * bcoinUsd
  balanceBrl = balance * bcoinBrl

  return 'New Map Started \nBCOINS: {:0,.2f} \nBCOIN/USD: U${:0,.2f} \nBCOIN/BRL: R${:0,.2f} \nBalance/USD: U${:0,.2f} \nBalance/BRL: R${:0,.2f}'.format(balance, bcoinUsd, bcoinBrl, balanceUsd, balanceBrl)


############## send_sms ##############
def send_sms(destination, message):
  account_sid = keys['account_sid']
  auth_token = keys['auth_token']

  client = Client(account_sid, auth_token)

  message = client.messages.create(
    body = message,
    from_= keys['from_number'],
    to = destination
  )

############## refresh_page ##############
def refresh_page():
  global isLogged
  global timer
  global pageTimer

  print('Refresh Page')
  image = getImage_('server.jpg')
  
  print('Searching for Server Image')
  while(image == None):
    time.sleep(1)  
    image = getImage_('server.jpg')

  mouseClick_(image)
  isLogged = False
  timer = 0
  pageTimer = 0
  reloadPage_()


############## refresh_map ##############
def refresh_map():
  global timer
  global toHunt

  traying = 0
  
  print('Refresh Map')

  # Searching for Back Arrow Button
  print('Searching for Back Arrow Button')
  image = getImage_('back_arrow.jpg')
  
  while(image == None and traying < traying_time + 10):
    time.sleep(1)
    image = getImage_('back_arrow.jpg')
    traying+=1

    # If don't see it, refresh page
  if(traying >= traying_time):
    print('Back Arrow Button not found. Restarting page')
    refresh_page()
    return False

  if(image != None):
      mouseClick_(image)
      traying = 0

  if(toHunt == True):
      toHunt = False
      start_minner()
      timer = 0
  else:
      toHunt = True
      select_heroes()
      start_minner()
      timer = 0

############## workflow ##############
def workflow():
  global timer
  global pageTimer
  global isLogged

  print('Workflow Started')

  while 1 and isLogged == True:
    time.sleep(1)

    if(time == 0):
      start_minner()

    if(timer > refresh_map_time):
      refresh_map()

    if(pageTimer > refresh_page_time):
      refresh_page()

    image = getImage_('new_map.jpg')
    if(image != None):
      mouseClick_(image)
      send_sms('+5531990715078', bomb_balance())

    timer+=1
    pageTimer+=1

############## start_minner ##############
def start_minner():
  global isLogged

  print('Start Minner')

  traying = 0

  # Searching for Treasure Hunt Button
  print('Searching for Treasure Hunt Button')
  image = getImage_('treasure_hunt_icon.jpg')
  while(image == None and traying < traying_time + 20):
    time.sleep(1)
    image = getImage_('treasure_hunt_icon.jpg')
    traying+=1

  # If don't see it, refresh page
  if(traying >= traying_time):
    print('Treasure Hunt Button not found. Restarting page')
    refresh_page()
    return False
  
  # Start Minner
  if(image != None):
    mouseClick_(image)
    traying = 0
    isLogged = True


############## select_heroes ##############
def select_heroes():
  print('Select Heroes')
  
  traying = 0

  print('Searching for Heroes Button')
  image = getImage_('hero_icon.jpg')
  while(image == None and traying < traying_time + 10):
    time.sleep(1)
    image = getImage_('hero_icon.jpg')
    traying+=1

  # If don't see it, refresh page
  if(traying >= traying_time):
    print('Heroes Button not found. Restarting page')
    refresh_page()
    return False

  if(image != None):
      mouseClick_(image)
      
      print('Starting Heroes')
      image = None
      while(image == None and traying < traying_time + 10):
        image = getImage_('scroll_hero.jpg')

      if(traying >= traying_time):
        print('Heroes Button not found. Restarting page')
        refresh_page()
        return False

      if(image != None):
        mouseClick_(image)
        x, y = pt.position()

        btn_clicks = []

        for i in range(4):            
          greenBars = pt.locateAllOnScreen('images/green_bar.jpg', confidence = 0.95)
          
          for bar in greenBars:
            xb, yb, wb, hb = bar

            if([xb, yb] not in btn_clicks):
              btn_clicks.append([xb, yb])
              pt.moveTo(xb + offset, yb, 0.1)
              pt.click()

          pt.moveTo(x, y, 1)
          pt.dragRel(0, -120, 1)
          time.sleep(4)
      
      btn_clicks = []

      # Click X button
      print('Close Heroes Characters')
      image = getImage_('x.jpg')
      while(image == None and traying < traying_time):
        time.sleep(1)
        image = getImage_('x.jpg')
        traying+=1
      
      # If don't see it, refresh page
      if(traying >= traying_time):
        print('Close Heroes Characters failure. Restarting page')
        refresh_page()
        return False

      if(image != None):
          mouseClick_(image)

############## connect_wallet ##############
def connect_wallet():
  print('Connect Wallet')
  traying = 0
  
  # Searching for Connect Wallet Button
  image = getImage_('connect_wallet.jpg')
  print('Searching for Connect Wallet Button')
  while(image == None and traying < traying_time):
    time.sleep(1)
    image = getImage_('connect_wallet.jpg')
    traying+=1
  
  # If don't see it, refresh page
  if(traying >= traying_time):
    print('Connect Wallet failure. Restarting page')
    refresh_page()
    return False
  
  # Button connect Wallet found
  mouseClick_(image)
  traying = 0

  # Search for MetaMask Login button
  image = getImage_('btn_sign.jpg')
  print('Searching for MetaMask Login button')
  while (image == None and traying < traying_time):
    time.sleep(1)
    image = getImage_('btn_sign.jpg')
    traying+=1

  # If don't see it, refresh page
  if(traying >= traying_time):
    print('Connect Wallet failure. Restarting page')
    refresh_page()
    return False

  # Button MetaMask Login found
  mouseClick_(image)
  traying = 0

  # start minner
  start_minner()


############## main ##############
def main():
  
  global isLogged

  while True:
    time.sleep(1)

    if (isLogged == False):
      connect_wallet()
    
    if (isLogged == True):
      workflow()

    # select_heroes()

############## start bot ##############
print('Start BombBot')
main()
