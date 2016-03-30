######################################################################
#
#  Hardware routines for LEDs
#
######################################################################

import wiringpi2 as wiringpi
from time import sleep


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

# Define some constants so we can read our own code...
ON = 1
OFF = 0
OUT = 1
IN = 0

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


#####################################################################
# Methods to turn individual LEDS on & off
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


#LedAllOff()
