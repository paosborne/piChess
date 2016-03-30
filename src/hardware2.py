######################################################################
#
#  Hardware routines for LEDs
#
######################################################################

import wiringpi2 as wiringpi
from time import sleep
import RPi.GPIO as GPIO


# Address for i2c expanders
i2c1_LEDS_addr = 0x20
i2c2_LEDS_addr = 0x21

# Address for the first pin
pin_base_i2c1 = 65     
pin_base_i2c2 = 81     

# Identify the PINS with friendly names
A = 65
B = 66
C = 67
D = 68
E = 69
F = 70
G = 71
H = 72
ONE=73
TWO=74
THR=75
FOU=76
FIV=77
SIX=78
SEV=79
EIG=80
WHI=81
BLA=82

#LCD PINS
LCD_RS = 83
LCD_EN  = 84
LCD_D4 = 85
LCD_D5 = 86
LCD_D6 = 87
LCD_D7 = 88


# Define some constants so we can read our own code...
ON = 1
OFF = 0
OUT = 1
IN = 0

# LCD Constants
LCD_WIDTH = 16    # Maximum characters per line
LCD_CHR = True
LCD_CMD = False
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line
 
# Timing constants
E_PULSE = 0.0005
E_DELAY = 0.0005
T_MS = 1.0000000/1000000
P_RS = 11 # 7


# Initialise the I2Cs
wiringpi.wiringPiSetup()
wiringpi.mcp23017Setup(pin_base_i2c1,i2c1_LEDS_addr)
wiringpi.mcp23017Setup(pin_base_i2c2,i2c2_LEDS_addr)


# Set default PIN MODES
wiringpi.pinMode(A,OUT)
wiringpi.pinMode(B,OUT)
wiringpi.pinMode(C,OUT)
wiringpi.pinMode(D,OUT)
wiringpi.pinMode(E,OUT)
wiringpi.pinMode(F,OUT)
wiringpi.pinMode(G,OUT)
wiringpi.pinMode(H,OUT)
wiringpi.pinMode(ONE,OUT)
wiringpi.pinMode(TWO,OUT)
wiringpi.pinMode(THR,OUT)
wiringpi.pinMode(FOU,OUT)
wiringpi.pinMode(FIV,OUT)
wiringpi.pinMode(SIX,OUT)
wiringpi.pinMode(SEV,OUT)
wiringpi.pinMode(EIG,OUT)
wiringpi.pinMode(WHI,OUT)
wiringpi.pinMode(BLA,OUT)
wiringpi.pinMode(LCD_RS,OUT)
wiringpi.pinMode(LCD_EN,OUT)
wiringpi.pinMode(LCD_D4,OUT)
wiringpi.pinMode(LCD_D5,OUT)
wiringpi.pinMode(LCD_D6,OUT)
wiringpi.pinMode(LCD_D7,OUT)


def LCDInitDisplay():
  # Set function to 4 bit operation
  i = 0
  while i < 3:     
    # Needs to be executed 3 times
    # Wait > 40 MS
    sleep(1)
    wiringpi.digitalWrite(LCD_RS, IN)
   #wiringpi.digitalWrite(LCD_RW, IN)
    wiringpi.digitalWrite(LCD_D7, IN)
    wiringpi.digitalWrite(LCD_D6, IN)
    wiringpi.digitalWrite(LCD_D5, OUT)
    wiringpi.digitalWrite(LCD_D4, OUT)
    LCDPulseEnable()
    i += 1

# Turn on display and cursor
def LCDDisplay(display, cursor, block):
  wiringpi.digitalWrite(LCD_RS, 0)
 #wiringpi.digitalWrite(LCD_RW, 0)
  wiringpi.digitalWrite(LCD_D7, 0)
  wiringpi.digitalWrite(LCD_D6, 0)
  wiringpi.digitalWrite(LCD_D5, 0)
  wiringpi.digitalWrite(LCD_D4, 0)
  LCDPulseEnable()

  wiringpi.digitalWrite(LCD_RS, 0)
 #wiringpi.digitalWrite(LCD_RW, 0)
  wiringpi.digitalWrite(LCD_D7, 1)
  wiringpi.digitalWrite(LCD_D6, display) # 1 = 0n
  wiringpi.digitalWrite(LCD_D5, cursor) # 1 = Cursor on, 0 = Cursor off
  wiringpi.digitalWrite(LCD_D4, block) # 1 = Block, 0 = Underline cursor
  LCDPulseEnable()

def LCDPulseEnable():
  # Indicate to LCD that command should be 'executed'
  wiringpi.digitalWrite(LCD_EN, 0)
  sleep(T_MS * 10)
  wiringpi.digitalWrite(LCD_EN, 1)
  sleep(T_MS * 10)
  wiringpi.digitalWrite(LCD_EN, 0)
  sleep(T_MS * 10)

def LCDSetEntryMode():
  # Entry mode set: move cursor to right after each DD/CGRAM write
  wiringpi.digitalWrite(LCD_RS, 0)
 #wiringpi.digitalWrite(LCD_RW, 0)
  wiringpi.digitalWrite(LCD_D7, 0)
  wiringpi.digitalWrite(LCD_D6, 0)
  wiringpi.digitalWrite(LCD_D5, 0)
  wiringpi.digitalWrite(LCD_D4, 0)
  LCDPulseEnable()

  wiringpi.digitalWrite(LCD_RS, 0)
 #wiringpi.digitalWrite(LCD_RW, 0)
  wiringpi.digitalWrite(LCD_D7, 0)
  wiringpi.digitalWrite(LCD_D6, 1)
  wiringpi.digitalWrite(LCD_D5, 1)
  wiringpi.digitalWrite(LCD_D4, 0)
  LCDPulseEnable()
  sleep(T_MS)

#def doLcdPrint(theText):
#  # Loop through each character in the string, convert it to binary, and print it to the LCD
#  theText.split(//).each { | theChar |
#    #puts theChar
#    #binChar = @parseBin.getBin(theChar)
#    binChar = theChar.bytes.first.to_s(2)
#    while (binChar.length < 8):
#      binChar = "0" + binChar
#
#    binCharArray = []
#    binChar.split().each {}
#    binChar.split(//).each{ |intChar| binCharArray << intChar.to_i  }
#
#    if (binChar):
#      if (@onPi == true):
#        LCDWrite(binCharArray)
#      binChar = nil
#  }

#####################################################################
# PUBLIC Methods to turn individual LEDS on & off
#####################################################################

def LedAOn():
  wiringpi.digitalWrite(A,ON)

def LedAOff():
  wiringpi.digitalWrite(A,OFF)

def LedBOn():
  wiringpi.digitalWrite(B,ON)

def LedBOff():
  wiringpi.digitalWrite(B,OFF)

def LedCOn():
  wiringpi.digitalWrite(C,ON)

def LedCOff():
  wiringpi.digitalWrite(C,OFF)

def LedDOn():
  wiringpi.digitalWrite(D,ON)

def LedDOff():
  wiringpi.digitalWrite(D,OFF)

def LedEOn():
  wiringpi.digitalWrite(E,ON)

def LedEOff():
  wiringpi.digitalWrite(E,OFF)

def LedFOn():
  wiringpi.digitalWrite(F,ON)

def LedFOff():
  wiringpi.digitalWrite(F,OFF)

def LedGOn():
  wiringpi.digitalWrite(G,ON)

def LedGOff():
  wiringpi.digitalWrite(G,OFF)

def LedHOn():
  wiringpi.digitalWrite(H,ON)

def LedHOff():
  wiringpi.digitalWrite(H,OFF)

def LedONEOn():
  wiringpi.digitalWrite(ONE,ON)

def LedONEOff():
  wiringpi.digitalWrite(ONE,OFF)

def LedTWOOn():
  wiringpi.digitalWrite(TWO,ON)

def LedTWOOff():
  wiringpi.digitalWrite(TWO,OFF)

def LedTHROn():
  wiringpi.digitalWrite(THR,ON)

def LedTHROff():
  wiringpi.digitalWrite(THR,OFF)

def LedFOUOn():
  wiringpi.digitalWrite(FOU,ON)

def LedFOUOff():
  wiringpi.digitalWrite(FOU,OFF)

def LedFIVOn():
  wiringpi.digitalWrite(FIV,ON)

def LedFIVOff():
  wiringpi.digitalWrite(FIV,OFF)

def LedSIXOn():
  wiringpi.digitalWrite(SIX,ON)

def LedSIXOff():
  wiringpi.digitalWrite(SIX,OFF)

def LedSEVOn():
  wiringpi.digitalWrite(SEV,ON)

def LedSEVOff():
  wiringpi.digitalWrite(SEV,OFF)

def LedEIGOn():
  wiringpi.digitalWrite(EIG,ON)

def LedEIGOff():
  wiringpi.digitalWrite(EIG,OFF)

def LedWHIOn():
  wiringpi.digitalWrite(WHI,ON)

def LedWHIOff():
  wiringpi.digitalWrite(WHI,OFF)

def LedBLAOn():
  wiringpi.digitalWrite(BLA,ON)

def LedBLAOff():
  wiringpi.digitalWrite(BLA,OFF)


######################################################################
# Turn ALL LEDS on/off
######################################################################

def LedAllOn():
  wiringpi.digitalWrite(A,ON)
  wiringpi.digitalWrite(B,ON)
  wiringpi.digitalWrite(C,ON)
  wiringpi.digitalWrite(D,ON)
  wiringpi.digitalWrite(E,ON)
  wiringpi.digitalWrite(F,ON)
  wiringpi.digitalWrite(G,ON)
  wiringpi.digitalWrite(H,ON)
  wiringpi.digitalWrite(ONE,ON)
  wiringpi.digitalWrite(TWO,ON)
  wiringpi.digitalWrite(THR,ON)
  wiringpi.digitalWrite(FOU,ON)
  wiringpi.digitalWrite(FIV,ON)
  wiringpi.digitalWrite(SIX,ON)
  wiringpi.digitalWrite(SEV,ON)
  wiringpi.digitalWrite(EIG,ON)
  wiringpi.digitalWrite(WHI,ON)
  wiringpi.digitalWrite(BLA,ON)

def LedAllOff():
  wiringpi.digitalWrite(A,OFF)
  wiringpi.digitalWrite(B,OFF)
  wiringpi.digitalWrite(C,OFF)
  wiringpi.digitalWrite(D,OFF)
  wiringpi.digitalWrite(E,OFF)
  wiringpi.digitalWrite(F,OFF)
  wiringpi.digitalWrite(G,OFF)
  wiringpi.digitalWrite(H,OFF)
  wiringpi.digitalWrite(ONE,OFF)
  wiringpi.digitalWrite(TWO,OFF)
  wiringpi.digitalWrite(THR,OFF)
  wiringpi.digitalWrite(FOU,OFF)
  wiringpi.digitalWrite(FIV,OFF)
  wiringpi.digitalWrite(SIX,OFF)
  wiringpi.digitalWrite(SEV,OFF)
  wiringpi.digitalWrite(EIG,OFF)
  wiringpi.digitalWrite(WHI,OFF)
  wiringpi.digitalWrite(BLA,OFF)

#LCD_RS = 83
#LCD_EN  = 84
#LCD_D4 = 85
#LCD_D5 = 86
#LCD_D6 = 87
#LCD_D7 = 88

lcd = wiringpi.lcdInit (2, 16, 4, LCD_RS, LCD_EN, LCD_D4, LCD_D5, LCD_D6, LCD_D7, 0,0,0,0)
wiringpi.lcdHome(lcd)
wiringpi.lcdClear(lcd)
wiringpi.lcdPosition(lcd, 0, 0)
wiringpi.lcdPuts(lcd, "oh yeah!")
wiringpi.lcdPosition(lcd, 0, 1)
wiringpi.lcdPuts(lcd, "it works!")
