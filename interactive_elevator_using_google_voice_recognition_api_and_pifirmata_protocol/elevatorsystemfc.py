from pyfirmata import Arduino, util
from time import sleep
import speech_recognition as sr
import pyttsx3
import pyaudio



port = 'COM11'
board = Arduino(port)



r = sr.Recognizer()
mic = sr.Microphone()
engine = pyttsx3.init()




servo180 = board.get_pin('d:11:s') # pin for 180 degree servo motor signal
servo360 = board.get_pin('d:9:s')  # pin for 360 degree servo motor signal
floor1pin = board.get_pin('d:2:i') # pin for floor 1 pushbuttonc
floor2pin = board.get_pin('d:7:i') # pin for floor 2 pushbutton
floor3pin = board.get_pin('d:8:i') # pin for floor 3 pushbutton
floor4pin = board.get_pin('d:12:i') # pin for floor 4 pushbutton



cf = 1
ef = 0



it = util.Iterator(board)
it.start()



door_open = True
door_close = False
confirmation = False
confirmation1 = False
servo360.write(90)



def voice_recognition():


  global ef

  txt = ""

  while not (('one' in txt) or ('two' in txt) or ('three' in txt) or ('four' in txt) or ('1' in txt) or ('2' in txt) or ('3' in txt) or ('4' in txt)):

    with mic as source:
      print('Speak Anything')
      engine.say('Which floor do you want to go?')
      engine.runAndWait()

      audio = r.listen(source)

      try:
          txt = r.recognize_google(audio)
          txt = txt.lower()
          print(f'You said : {txt}')

      except:
          print('Sorry did not recognized')
          engine.say('Sorry did not recognized. Speak Again')
          engine.runAndWait()
  
  if (('one' in txt) or ('1' in txt)):
    ef = 1
  
  elif (('two' in txt) or ('2' in txt)):
    ef = 2
  
  elif (('three' in txt) or ('3' in txt)):
    ef = 3
  
  elif (('four' in txt) or ('4' in txt)):
    ef = 4
  


def smr360():  # servo motor rotate


  servo360.write(70)
  sleep(6.3)
  servo360.write(90)


def smrr360():  # servo motor reverse rotate


  servo360.write(110)
  sleep(6.25)
  servo360.write(90)



def smr180():  # servo motor rotate


  for x in range(0,91):
    servo180.write(x)
    sleep(0.05)



def smrr180():  # servo motor reverse rotate


  for x in range(90,-1,-1):
    servo180.write(x)
    sleep(0.05)
  


# ur sensor reading will give us the current floor positioning
# cf : current floor
# ef : entered floor



def mmufp():   # motor manipulation upon floor positioning after voice recognition


  global ef,cf

  if ef == 4:

    if cf == 4: # i.e. current floor and entered floor are same
      engine.say('You are on the same floor.')
      engine.runAndWait()

    elif cf == 3: # i.e. current floor is 3, entered floor is 4
      engine.say('Ascending to floor number four.')
      engine.runAndWait()
      smr360()
      engine.say('You have reached the floor number four.')
      engine.runAndWait()

    elif cf == 2: # i.e. current floor is 2, entered floor is 4
      engine.say('Ascending to floor number four.')
      engine.runAndWait()
      smr360()
      smr360()
      engine.say('You have reached the floor number four.')
      engine.runAndWait()

    elif cf == 1: # i.e. current floor is 3, entered floor is 4
      engine.say('Ascending to floor number four.')
      engine.runAndWait()
      smr360()
      smr360()
      smr360()
      engine.say('You have reached the floor number four.')
      engine.runAndWait()

    cf = 4


  elif ef == 3:

    if cf == 3: # i.e. current floor and entered floor are same
      engine.say('You are on the same floor.')
      engine.runAndWait()

    elif cf == 4: # i.e. current floor is 4, entered floor is 3
      engine.say('Descending to floor number three.')
      engine.runAndWait()
      smrr360()
      engine.say('You have reached the floor number three.')
      engine.runAndWait()

    elif cf == 2: # i.e. current floor is 2, entered floor is 3
      engine.say('Ascending to floor number three.')
      engine.runAndWait()
      smr360()
      engine.say('You have reached the floor number three.')
      engine.runAndWait()

    elif cf == 1: # i.e. current floor is 1, entered floor is 3
      engine.say('Ascending to floor number three.')
      engine.runAndWait()
      smr360()
      smr360()
      engine.say('You have reached the floor number three.')
      engine.runAndWait()

    cf = 3
    

  elif ef == 2:

    if cf == 2: # i.e. current floor and entered floor are same
      engine.say('You are on the same floor.')
      engine.runAndWait()

    elif cf == 3: # i.e. current floor is 3, entered floor is 2
      engine.say('Descending to floor number two.')
      engine.runAndWait()
      smrr360()
      engine.say('You have reached the floor number two.')
      engine.runAndWait()

    elif cf == 4: # i.e. current floor is 4, entered floor is 2
      engine.say('Descending to floor number two.')
      engine.runAndWait()
      smrr360()
      smrr360()
      engine.say('You have reached the floor number two.')
      engine.runAndWait()

    elif cf == 1: # i.e. current floor is 1, entered floor is 2
      engine.say('Ascending to floor number two.')
      engine.runAndWait()
      smr360()
      engine.say('You have reached the floor number two.')
      engine.runAndWait()

    cf = 2


  elif ef == 1:

    if cf == 1: # i.e. current floor and entered floor are same
      engine.say('You are on the same floor.')
      engine.runAndWait()

    elif cf == 2: # i.e. current floor is 2, entered floor is 1
      engine.say('Descending to floor number one.')
      engine.runAndWait()
      smrr360()
      engine.say('You have reached the floor number one.')
      engine.runAndWait()

    elif cf == 3: # i.e. current floor is 3, entered floor is 1
      engine.say('Descending to floor number one.')
      engine.runAndWait()
      smrr360()
      smrr360()
      engine.say('You have reached the floor number one.')
      engine.runAndWait()

    elif cf == 4: # i.e. current floor is 4, entered floor is 1
      engine.say('Descending to floor number one.')
      engine.runAndWait()
      smrr360()
      smrr360()
      smrr360()
      engine.say('You have reached the floor number one.')
      engine.runAndWait()

    cf = 1



def voice_confirmation():


  global confirmation

  txt1 = ""

  while not (('yes' in txt1) or ('no' in txt1)):

    with mic as source:
      print('Speak Anything')
      engine.say('Did you said floor which I just spoken about. yes or no?')
      engine.runAndWait()

      audio = r.listen(source)

      try:
          txt1 = r.recognize_google(audio)
          txt1 = txt1.lower()
          print(f'You said : {txt1}')

      except:
          print('Sorry did not recognized')
          engine.say('Sorry did not recognized. Speak Again')
          engine.runAndWait()
  
  if ('yes' in txt1):

    confirmation = True
  
  elif ('no' in txt1):

    confirmation = False



def voice_confirmation1():


  global confirmation1

  txt2 = ""

  while not (('voice command' in txt2) or ('push button' in txt2)):

    with mic as source:
      print('Speak Anything')
      engine.say('What do you want to use? Push Button or Voice Command.')
      engine.runAndWait()

      audio = r.listen(source)

      try:
          txt2 = r.recognize_google(audio)
          txt2 = txt2.lower()
          print(f'You said : {txt2}')

      except:
          print('Sorry did not recognized')
          engine.say('Sorry did not recognized. Speak Again')
          engine.runAndWait()
  
  if ('voice command' in txt2):

    confirmation1 = True
  
  elif ('push button' in txt2):

    confirmation1 = False



def voice_recognition1():


  global ef

  txt3 = ""

  while not (('one' in txt3) or ('two' in txt3) or ('three' in txt3) or ('four' in txt3) or ('1' in txt3) or ('2' in txt3) or ('3' in txt3) or ('4' in txt3)):

    with mic as source:
      print('Speak Anything')
      engine.say('You are at which floor?')
      engine.runAndWait()

      audio = r.listen(source)

      try:
          txt3 = r.recognize_google(audio)
          txt3= txt3.lower()
          print(f'You said : {txt3}')

      except:
          print('Sorry did not recognized')
          engine.say('Sorry did not recognized. Speak Again')
          engine.runAndWait()
  
  if (('one' in txt3) or ('1' in txt3)):
    ef = 1
    engine.say('Wait... elevator is coming')
    engine.runAndWait()

  
  elif (('two' in txt3) or ('2' in txt3)):
    ef = 2
    engine.say('Wait... elevator is coming')
    engine.runAndWait()
  
  elif (('three' in txt3) or ('3' in txt3)):
    ef = 3
    engine.say('Wait... elevator is coming')
    engine.runAndWait()
  
  elif (('four' in txt3) or ('4' in txt3)):
    ef = 4
    engine.say('Wait... elevator is coming')
    engine.runAndWait()
  


def push_button():


  global ef

  print("Kindly Enter your Desired Floor Button.")
  engine.say('Kindly Enter your Desired Floor Button.')
  engine.runAndWait()

  while True:
    
    try:

        if floor1pin.read() == 1:
            engine.say('You entered the floor number one.')
            engine.runAndWait()
            voice_confirmation()
            if confirmation == True:
              ef = 1
              break
            else:
              engine.say('Kindly Enter your Desired Floor Button.')
              engine.runAndWait()
              continue

        elif floor2pin.read() == 1:
            engine.say('You entered the floor number two.')
            engine.runAndWait()
            voice_confirmation()
            if confirmation == True:
              ef = 2
              break
            else:
              engine.say('Kindly Enter your Desired Floor Button.')
              engine.runAndWait()
              continue
        
        elif floor3pin.read() == 1:
            engine.say('You entered the floor number three.')
            engine.runAndWait()
            voice_confirmation()
            if confirmation == True:
              ef = 3
              break
            else:
              engine.say('Kindly Enter your Desired Floor Button.')
              engine.runAndWait()
              continue
        
        elif floor4pin.read() == 1:
            engine.say('You entered the floor number four.')
            engine.runAndWait()
            voice_confirmation()
            if confirmation == True:
              ef = 4
              break
            else:
              engine.say('Kindly Enter your Desired Floor Button.')
              engine.runAndWait()
              continue

        elif ((floor1pin.read() == 0) and (floor2pin.read() == 0) and (floor3pin.read() == 0) and (floor4pin.read() == 0)):
            print("Still Waiting")
            engine.say('Still Waiting')
            engine.runAndWait()

    except : 

        print("Didn't Executed")



  print("Button is Pushed")


  


  

def open_door():


  global door_open,door_close
  print('Door Opens')
  engine.say('Openning the Door.')
  engine.runAndWait()
  smr180()
  door_open = True
  door_close = False




def close_door():


  global door_open,door_close
  print('Door closes')
  engine.say('Closing the Door.')
  engine.runAndWait()
  smrr180()
  door_close = True
  door_open = False



engine.say('Welcome! Elevator is On.')
engine.runAndWait()



while True:


  if door_open == True:

    engine.say('You are outside the elevator.')
    engine.runAndWait()
    voice_confirmation1()
    if confirmation1 == True:
      voice_recognition1()
    elif confirmation1 == False:
      push_button()

    if cf != ef :
        sleep(1)
        close_door()
        mmufp()
        open_door()
        sleep(3)
        close_door()

    elif cf == ef :
        sleep(1)
        mmufp()
        close_door()
        
        
  elif door_close == True:
    engine.say('You are inside the elevator.')
    engine.runAndWait()
    voice_recognition()
    mmufp()
    sleep(3)
    open_door()