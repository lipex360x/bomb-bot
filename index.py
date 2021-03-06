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
  now = dateFormatted_('%d/%m/%Y - %H:%M:%S')

  # Remove Comments bellow in Windows OS
  # if(platform.system() == 'Windows'):
    # pytesseract.tesseract_cmd = r'<tesseract_path_install>\tesseract.exe'
      
  image = getImage_('bcoin_bag.jpg')
  
  if(image != None):
    mouseClick_(image)
    
    if os.path.isfile('total_bcoins.png'):
      os.remove('total_bcoins.png')
    
    time.sleep(5)

    pt.screenshot('total_bcoins.png', region=(720, 550, 200, 60))
    
    img = Image.open('total_bcoins.png')
    balance = pytesseract.image_to_string(img)
    balance = balance.replace('\n', ' ').replace('\r', '').replace(',', '.')
    
    os.remove('total_bcoins.png')

    image = getImage_('x.jpg')
    mouseClick_(image)

    return float(balance)


############## bomb_balance ##############
def bomb_balance():
  now = dateFormatted_('%d/%m/%Y - %H:%M:%S')
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
  now = dateFormatted_('%d/%m/%Y - %H:%M:%S')
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
  now = dateFormatted_('%d/%m/%Y - %H:%M:%S')
  global isLogged
  global timer
  global pageTimer

  print(now, 'Refresh Page')
  image = getImage_('server2.jpg')
  
  print(now, 'Searching for Server Image')
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
  now = dateFormatted_('%d/%m/%Y - %H:%M:%S')
  global timer
  global toHunt
  global isLogged

  traying = 0
  
  print(now, 'Refresh Map')

  # Searching for Back Arrow Button
  print(now, 'Searching for Back Arrow Button')
  image = getImage_('back_arrow.jpg')
  
  while(image == None and traying < traying_time + 10):
    time.sleep(1)
    image = getImage_('back_arrow.jpg')
    traying+=1

    # If don't see it, refresh page
  if(traying >= traying_time):
    print(now, 'Back Arrow Button not found. Restarting page')
    isLogged = False
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
  now = dateFormatted_('%d/%m/%Y - %H:%M:%S')
  global timer
  global pageTimer
  global isLogged

  print(now, 'Workflow Started')

  while 1 and isLogged == True:
    time.sleep(1)

    if(time == 0):
      start_minner()

    if(timer > refresh_map_time):
      refresh_map()

    if(pageTimer > refresh_page_time):
      refresh_page()

    # image = getImage_('new_map.jpg')
    # if(image != None):
    #  mouseClick_(image)
    #  send_sms(keys['to_number'], bomb_balance())

    timer+=1
    pageTimer+=1

############## start_minner ##############
def start_minner():
  now = dateFormatted_('%d/%m/%Y - %H:%M:%S')
  global isLogged

  print(now, 'Start Minner')

  traying = 0

  # Searching for Treasure Hunt Button
  print(now, 'Searching for Treasure Hunt Button')
  image = getImage_('treasure_hunt_icon.jpg')
  while(image == None and traying < traying_time + 20):
    time.sleep(1)
    image = getImage_('treasure_hunt_icon.jpg')
    traying+=1

  # If don't see it, refresh page
  if(traying >= traying_time):
    print(now, 'Treasure Hunt Button not found. Restarting page')
    isLogged = False
    refresh_page()
    return False
  
  # Start Minner
  if(image != None):
    mouseClick_(image)
    print(now, 'Heroes in Map')
    traying = 0
    isLogged = True


############## select_heroes ##############
def select_heroes():
  global isLogged
  now = dateFormatted_('%d/%m/%Y - %H:%M:%S')
  print(now, 'Select Heroes')
  
  traying = 0

  print(now, 'Searching for Heroes Button')
  image = getImage_('hero_icon.jpg')
  while(image == None and traying < traying_time + 10):
    time.sleep(1)
    image = getImage_('hero_icon.jpg')
    traying+=1

  # If don't see it, refresh page
  if(traying >= traying_time):
    print(now, 'Heroes Button not found. Restarting page')
    isLogged = False
    refresh_page()
    return False

  if(image != None):
      mouseClick_(image)
      
      traying = 0
      print(now, 'Starting Heroes')
      image = None
      while(image == None and traying < traying_time + 10):
        image = getImage_('scroll_hero.jpg')
        traying+=1

      if(traying >= traying_time):
        print(now, 'Heroes Button not found. Restarting page')
        isLogged = False
        refresh_page()
        return False

      if(image != None):
        mouseClick_(image)
        x, y = pt.position()

        btn_clicks = []

        for i in range(5):            
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
      print(now, 'Close Heroes Characters')
      image = getImage_('x.jpg')
      while(image == None and traying < traying_time):
        time.sleep(1)
        image = getImage_('x.jpg')
        traying+=1
      
      # If don't see it, refresh page
      if(traying >= traying_time):
        print(now, 'Close Heroes Characters failure. Restarting page')
        isLogged = False
        refresh_page()
        return False

      if(image != None):
          mouseClick_(image)
          traying = 0

############## connect_wallet ##############
def connect_wallet():
  global isLogged
  now = dateFormatted_('%d/%m/%Y - %H:%M:%S')
  print(now, 'Connect Wallet')
  traying = 0
  
  # Searching for Connect Wallet Button
  image = getImage_('connect_wallet.jpg')
  print(now, 'Searching for Connect Wallet Button')
  while(image == None and traying < traying_time):
    time.sleep(1)
    image = getImage_('connect_wallet.jpg')
    traying+=1
  
  # If don't see it, refresh page
  if(traying >= traying_time):
    print(now, 'Connection Wallet failure. Restarting page')
    isLogged = False
    refresh_page()
    return False
  
  # Button connect Wallet found
  mouseClick_(image)
  traying = 0

  # Search for MetaMask Login button
  image = getImage_('btn_sign.jpg')
  print(now, 'Searching for MetaMask Login button')
  while (image == None and traying < traying_time):
    time.sleep(1)
    image = getImage_('btn_sign.jpg')
    traying+=1

  # If don't see it, refresh page
  if(traying >= traying_time):
    print(now, 'Connection Wallet failure. Restarting page')
    isLogged = False
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


############## start bot ##############
now = dateFormatted_('%d/%m/%Y - %H:%M:%S')
print(now, 'Start BombBot')
main()
