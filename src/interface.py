#!/usr/bin/python
# -*- coding: utf-8 -*-

# This program plays chess using Stockfish the open 
# source chess engine, using the ChessBoard library to manage the board.
# it assumes you have got the python libraries chessboard, subprocess and time

# to start try running the program and type me2e4 at the first prompt.
# This program is built using lots of examples from around the web, 
# so do what you want with it.

# This code was orginally taken from www.chess.fortherapy.co.uk - but somewhat
# updated for my purposes with a load of tidying so I could understand the code.

# It does what I need, your mileage may vary... Please do not ask for support
# as I am no Python programmer and am making it myself as I go along.

# The aim is to end up with a real chess board with LEDs, buttons and perhaps
# a LCD display that functions like SciSys Chess Computers like I owned
# back in the 80s...

# This is set to use the v6 version of stockfish installed as a binary called 
# 'stockfish6' this is due to there being no Debian binary for the RaspberryPi
# and I needed to compile it from source but wanted the old engine around which
# had subtly different responses and options.  Both versions now work.

#####################################################################

# This file is interface.py and acts as a inteface between the chess engine
# 'stockfish', the player side rules and referee set 'chessBoard.py' and the
# physical world where the board and the player are.

# functions that use the chess engine directly are prefaced with 'engine'
#   ie. enginePut, engineGet  (to send messages to and from Stockfish using
#   the UCI protocol)

# methods that are called from the referee chessBoard.py are prefaced with
# 'game'   i.e game.getBoard

######################################################################
# initiate chessboard rules library
######################################################################

from ChessBoard import ChessBoard
from hardware import *
import subprocess, time
from array import array
game = ChessBoard()

LCD_RS = 83
LCD_EN = 84
LCD_D4 = 85
LCD_D5 = 86
LCD_D6 = 87
LCD_D7 = 88

# Initialise the LCD display
lcd = wiringpi.lcdInit (2, 16, 4, LCD_RS, LCD_EN, LCD_D4, LCD_D5, LCD_D6, LCD_D7, 0,0,0,0)
wiringpi.lcdHome(lcd)
wiringpi.lcdClear(lcd)
wiringpi.lcdPosition(lcd, 0, 0)
wiringpi.lcdPuts(lcd, "oh yeah!")
wiringpi.lcdPosition(lcd, 0, 1)
wiringpi.lcdPuts(lcd, "it works!")


######################################################################
# initiate stockfish chess engine
######################################################################

engine = subprocess.Popen('/usr/local/bin/stockfish6', 
		universal_newlines=True, 
		stdin=subprocess.PIPE, 
		stdout=subprocess.PIPE,);

######################################################################
# Set Skill Level  (1-8)
######################################################################

def level(skill, depth):

#lichess.org  Level settings for stockfish:
#
#AI level 1: skill 3/20, depth 1, 50ms
#AI level 2: skill 6/20, depth 2, 100ms
#AI level 3: skill 9/20, depth 3, 150ms
#AI level 4: skill 11/20, depth 4, 200ms
#AI level 5: skill 14/20, depth 6, 250ms
#AI level 6: skill 17/20, depth 8, 300ms
#AI level 7: skill 20/20, depth 10, 350ms
#AI level 8: skill 20/20, depth 12, 400ms

  level = int(input("\nBOARD engine skill level 1-8:"))

  engineLevels = []
  engineLevels.append(['level', 'skill', 'depth','ms'])
  engineLevels.append(['1', '3', '1', '50'])
  engineLevels.append(['2', '6', '2', '100'])
  engineLevels.append(['3', '9', '3', '150'])
  engineLevels.append(['4', '11', '4', '200'])
  engineLevels.append(['5', '14', '6', '250'])
  engineLevels.append(['6', '17', '8', '300'])
  engineLevels.append(['7', '20', '10', '350'])
  engineLevels.append(['8', '20', '12', '400'])


  sleep(.2)
  response = ""

  lvl = engineLevels[level][0]
  skill = engineLevels[level][1]
  depth = engineLevels[level][2]
  mtime = engineLevels[level][3]

  print('Level: ' + lvl)
  print('Skill: ' + skill)
  print('Depth: ' + depth)
  print('Ms: ' + mtime)
  putEngine('setoption name Skill Level value ' + skill)
  waitEngine()
  return skill, depth








######################################################################
# Set Style - passive -> reckless
######################################################################

def style():
  style = raw_input("\nBOARD engine passive/aggressive: -100 to 100 :").lower()
  putEngine('setoption name Contempt value ' + style)
  waitEngine()

#####################################################################
# Wait for the engine to confim 'readyok' from 'isready'
#####################################################################

def waitEngine():
  text = '';
  engine.stdin.write("isready\n")
  while True:
    text = engine.stdout.readline().strip()
    print ("engine: " + text)
    if text == "readyok":
      break

#####################################################################
# Engine makes it's move - returns move and hint
#####################################################################

def moveEngine():
  sleep(.1)
  response = ""
  while True:
    sleep(.05)
    response = engine.stdout.readline().strip()
    print ("engine: " + response)
    # found the engine's move - so return the entire line - also 
    # contains the hint for the player
    if response[0:8] == "bestmove":
      return response
    elif response == '':
      print ("Null string from engine")
      exit(10)

######################################################################
# get a string from the physical board (player)
######################################################################

# This will get updated to reflect the physical board in due course,
# of course I need to build a board first...

def getBoard():
  # gets a text string from the board
  btxt = raw_input("\nBOARD Player move:").lower()
  #print "PLAYER: " +btxt;
  return btxt

######################################################################
# an invalid option chosen
######################################################################

# should never see this...
def optionError(stxt):
  print("LCD: OPTION ERROR" +stxt)

######################################################################
# Start a New Game
######################################################################

def newGame():
  # initialise our physical board LEDs
  leds_off()
  # message here?
  # lcd_newgame() or somesuch?
  # initialise engine
  waitEngine()
  putEngine('uci')
  waitEngine()
  #putEngine('setoption name Skill Level value ' + skill)
  #putEngine('setoption name Skill Level value 5')
  #waitEngine()
  # Amount of RAM to let stockfish use, this could be pulled
  # out of the system environment to maximise - but this will do for now
  putEngine('setoption name Hash value 32')
  waitEngine()
  # Set threads to no of CPU cores available - hard setting 2, could
  # pull this out of the system - job for another day
  putEngine('setoption name Threads value 4')
  waitEngine()
  putEngine('uci')
  waitEngine()
  putEngine('ucinewgame')
  game.resetBoard()
  game.printBoard()
  whoseTurn()

#####################################################################
# Get FEN position from rules engine
#####################################################################

def getBoardFEN():
  fen = game.getFEN()
  return fen

#####################################################################
# Tell the rules engine the FEN position
#####################################################################

def setBoardFEN(fen):
  game.setFEN(fen)

#####################################################################
# tell engine the FEN game state
#####################################################################

def setEngineFEN(fen):
  fen = fen
  fen_cmd = 'position fen ' + fen 
#  print(fen_cmd)
  putEngine(fen_cmd)
  waitEngine()

#####################################################################
# save FEN stat to disk
#####################################################################

def saveFEN(fen):
  fen = fen
  # Open a file
  fo = open("gamestate.txt", "wb")
  fo.write(fen);
  fo.close()

#####################################################################
# load FEN state from disk
#####################################################################

def loadFEN():
  fen = ''
  fo = open("gamestate.txt", "r+")
  fen = fo.read();
  print "Read String is : ", fen
  fo.close()

#####################################################################
# undo moves by stepping backwards...
#####################################################################

def undo():
  move_list=''
  move_list = game.getAllTextMoves()
  print('before undo:' )
  print(move_list)
  game.printBoard()
  game.undo()
  move_list = game.getAllTextMoves()
  print('after undo:')
  print(move_list)
  game.printBoard()

#####################################################################
# Whose turn?
#####################################################################

def whoseTurn():
  turn = game.getTurn()
  if turn == ChessBoard.WHITE:
    print ("LED: 1 (WHITE) ON")
    LedWHIOn()
    print ("LED: 8 (BLACK) OFF")
    LedBLAOff()
    wiringpi.lcdPosition(lcd, 0, 1)
    wiringpi.lcdPuts(lcd, "White's move... ")
    #wiringpi.lcdPosition(lcd, 0, 1)
    #wiringpi.lcdPuts(lcd, "                ")

  elif turn == ChessBoard.BLACK:
    print ("LED: 8 (BLACK) ON")
    LedBLAOn()
    print ("LED: 1 (WHITE) OFF")
    LedWHIOff()
    wiringpi.lcdPosition(lcd, 0, 1)
    wiringpi.lcdPuts(lcd, "Black's move... ")
    #wiringpi.lcdPosition(lcd, 0, 1)
    #wiringpi.lcdPuts(lcd, "                ")

  else:
    print ("LCD: ERK! getTurn did not return what we expected")
    wiringpi.lcdPosition(lcd, 0, 0)
    wiringpi.lcdPuts(lcd, "Erk! Something  ")
    wiringpi.lcdPosition(lcd, 0, 1)
    wiringpi.lcdPuts(lcd, "went wrong      ")


#####################################################################
# Tell the rules engine the promoted piece
#####################################################################

def setBoardPromotion(promotion):
  promo = promotion
  print ("Promotion: " + promo)
  wiringpi.lcdPosition(lcd, 0, 0)
  wiringpi.lcdPuts(lcd, "Promotion:      ")
  wiringpi.lcdPosition(lcd, 0, 1)

  promoval = 0
  if promo == 'q':
    wiringpi.lcdPuts(lcd, "Queen           ")
    promoval = 1
  elif promo == 'r':
    wiringpi.lcdPuts(lcd, "Rook            ")
    promoval = 2
  elif promo == 'n':
    wiringpi.lcdPuts(lcd, "Knight          ")
    promoval = 3
  elif promo == 'b':
    wiringpi.lcdPuts(lcd, "Bishop          ")
    promoval = 4
  else:
    print ("Do not understand promotion value:" + promo)

  print("About to promote")
#  game.printBoard()  
#  raw_input("Press Enter to continue...")
  game.setPromotion(promoval)
  game.printBoard() 
#  raw_input("Press Enter to continue...")


#####################################################################
# Check?
#####################################################################

def isCheck():
  if (game.isCheck()):
    board_check()
  else:
    board_check_off()

#####################################################################
# Game Over?
#####################################################################

def isGameOver():
  if (game.isGameOver()):
    game.printBoard()
    result = game.getGameResult()
    if   result == 1:
      board_mate_white()
      exit(1)
    elif result == 2:
      board_mate_black()
      exit(2)
    elif result == 3:
      board_draw_stalemate()
      exit(3)
    elif result == 4:
      board_draw_fifty()
      exit(4)
    elif result == 5:
      board_draw_repetition()
      exit(5)

#####################################################################
# A game turn (NEW CODE)
#####################################################################

# this needs a re-written 'main' as it works in a more sensible way that
# reflects game flow and does not assume that the human player always
# plays white.

def playTurn(player, fen, move_list, hint, skill, depth):
  player = player
  fen = fen
  move_list = move_list
  hint = hint
  skill = skill
  depth = depth
  # white first
  whoseTurn()
  player, fen, move_list, hint, skill, depth =  playMove(player, fen, move_list, hint, skill, depth)
#  saveFEN(fen)
  # black second
  whoseTurn()
  player, fen, move_list, hint, skill, depth = playMove(player, fen, move_list, hint, skill, depth)
#  saveFEN(fen)

  return (player, fen, move_list, hint, skill, depth)

#####################################################################
# Play move (NEW CODE)
#####################################################################

def playMove(player, fen, move_list, hint, skill, depth):
  player = player
  fen = fen
  move_list = move_list
  hint = hint
  skill = skill
  depth = depth
  valid_response = 'FALSE'
  # Computer plays itself?
  SELF='YES'
  print("moves: " + move_list)
  if player == "HUMAN":
    while valid_response == 'FALSE':
      # get human input and process accordingly (subroutine?) as
      # may be hint request, level change or even a move 

      if SELF == 'YES':
        code = 'c'
      else:
        bmessage = getBoard()
        code = bmessage[0]


      # This is input from the player when it is their turn and needs re-locating...
      # decide which function to call based on first letter of txt fed back in
      # from the board - 

      # player makes a move
      if code == 'm':
        brdmove = bmessage[1:5].lower()
        # now validate move
        # if invalid, get reason & send back to board
        if game.addTextMove(brdmove) == False :
          print "Invalid Move!"
          errcode = str(game.getReason());
          etxt = "error"+ str(game.getReason())+ brdmove
          board_error(errcode)
          game.printBoard()
        # valid move!
        else:
          game.printBoard()
          #board_move(brdmove)
          temp = move_list
          move_list = temp+" " +brdmove
          valid_response = 'TRUE'
          fen = getBoardFEN()
          print ("FEN: " + fen)
          hint = "None"
          player = "COMPUTER"

      elif code == 'g': newGame()
      elif code == 'l': 
        skill, depth = level(skill, depth)
      elif code == 's': style()
      elif code == 'h': showHint(hint)
      elif code == 'u': undo()
      # force computer to play move
      elif code == 'c':
        player = "COMPUTER"  
        valid_response = 'TRUE'
      # where are my pieces...
      #  elif code == 'p': locate_pawns()
      #  elif code == 'q': locate_queens()
      #  elif code == 'k': locate_kings()
      #  elif code == 'b': locate_bishops()
      #  elif code == 'n': locate_knights()
      #  elif code == 'r': locate_rooks()
      # Should not get here once we have hard wired the input options
      else : optionError('error at option')

  # COMPUTER!
  else:
    # send FEN position to engine and await OK
    setEngineFEN(fen)

    # get engines move
    putEngine("go depth " + depth)
    text = ""
    promotion = ""
    text = moveEngine()
#    print("TEXT: " + text)
    engine_move = text[9:13]
    # may be a pawn promotion to deal with so process the response from the
    # engine, also may be a promotion in the 'hint' as well.
    resplen = 0
    resplen =  len(text)
# #   print ("RESP LEN")
#    print resplen

    # Check length of responses
    # normal move no promotion and hint
    if resplen == 25:
#      print("NORMAL!")
      hint = text[21:25]
    # move with promotion in move or hint
    elif resplen == 26:
      #check whether promotion in computer move or hint
      #promotion in move
      if text[13] != ' ':
        promotion = text[13]
#        print("TEXT: " + text)
#        print("Promotion in move")
#        print("PROMOTION: " + promotion )
        hint = text[22:26]
        setBoardPromotion(promotion)
      #promotion in hint 
      else:
#        print("TEXT: " + text)
#        print("Promotion in hint")
        hint = text[21:26]
      #raw_input("Press Enter to continue...")

    # move and hint both with promotion!
    elif resplen == 27:
      promotion = text[13]
#      print("TEXT: " + text)
#      print("Promotion in move")
#      print("PROMOTION: " + promotion )
      hint = text[22:27]
      setBoardPromotion(promotion)
#      raw_input("Press Enter to continue...")  

    # no hint offered - straight to checkmate
    elif resplen == 13:
      hint = ""
#      print("TEXT: " + text)
#      print("No HINT OFFERED")
#      print("game over???")
#      raw_input("Press Enter to continue...")

    # no hint but promotion
    elif resplen == 14:
      promotion = text[13]
#      print("Promotion in move")
#      print("PROMOTION: " + promotion )
      setBoardPromotion(promotion)
#      print("game over???")
#      raw_input("Press Enter to continue...")

    else:
      print "Unexpected response from engine!"
      print("TEXT: " + text)
      raw_input("Press Enter to continue...")

  

    #print("HINT: " + hint)
    #board_move(move_list)
    #raw_input("Press Enter to continue...")

    # validate computer's move to be sure - should not really need this...
    if game.addTextMove(engine_move) != True :
      errcode = str(game.getReason())
      print ("error in computer move? " + errcode)
      errtxt = "error"+ str(game.getReason())
      board_error(errcode)
      print ("error in computer move?")
      print board_error
      print("LCD: error in engine more?")
      print("LCD: " + errtxt + "\n")
      game.printBoard()
      exit(10)
    else:
      # but we do need this
      temp = move_list
      move_list = temp+" " +engine_move
      # not sure this is needed...
      #stx = engine_move+hint

    game.printBoard()
#    print ("computer move: " +engine_move)
    board_move(engine_move)

    fen = getBoardFEN()
    print ("FEN: " + fen)
    player = "HUMAN"


  # Move made - now check the game status
  #print ("MOVES: " + move_list)
  isCheck()
  isGameOver()
  return player, fen, move_list, hint, skill, depth

#####################################################################
# Send command to engine
#####################################################################
def putEngine(command):
#  print("\nyou:\n\t"+command)
  engine.stdin.write(command+"\n")

#####################################################################
# send move to board
#####################################################################
def board_move(move):
  print("LCD: MOVE is:  " +move + "\n") 
  lcdmove = "Last move: " + move
  wiringpi.lcdPosition(lcd, 0, 0)
  wiringpi.lcdPuts(lcd, lcdmove)
  #wiringpi.lcdPosition(lcd, 0, 1)
  #wiringpi.lcdPuts(lcd, "                ")


#####################################################################
# Bzzzt!
#####################################################################
def sendBzzt():
  print("BZZZT")

#####################################################################
# send error to board
#####################################################################

def board_error(errcode):
  errcode = errcode
#  print("BOARD: Error: " + errcode )
  if   errcode == "1":
    error_move()
  elif errcode == "2":
    error_colour()
  elif errcode == "3":
    error_from()
  elif errcode == "4":
    error_location()
  elif errcode == "5":
    error_promotion()
  # this should get trapped elsewhere on and not seen here...
  elif errcode == "6":
    print ("LCD: GAME IS OVER")

######################################################################
# Error handlers
######################################################################

def error_move():
  print ("LCD: INVALID MOVE")
  sendBzzt()

def error_colour():
  print ("LCD: INVALID COLOR")
  sendBzzt()

def error_from():
  print ("LCD: INVALID FROM LOCATION")
  sendBzzt()

def error_location():
  print ("LCD: INVALID TO LOCATION")
  sendBzzt()

def error_promotion():
  print ("LCD: MUST_SET_PROMOTION")
  sendBzzt()

######################################################################
# send 'check' to board
######################################################################

def board_check():
  print("LCD: Check!\n")
  print("LED: A,B ON")
  wiringpi.lcdPosition(lcd, 0, 1)
  wiringpi.lcdPuts(lcd, "Check!          ")
  #wiringpi.lcdPosition(lcd, 0, 1)
  #wiringpi.lcdPuts(lcd, "                ")
  LedAOn()
  LedBOn()
  sendBzzt()

######################################################################
# turn 'check' LEDs off
######################################################################

def board_check_off():
  print("LED: A,B OFF")
  #wiringpi.lcdPosition(lcd, 0, 0)
  #wiringpi.lcdPuts(lcd, "                ")
  wiringpi.lcdPosition(lcd, 0, 1)
  wiringpi.lcdPuts(lcd, "                ")
  LedAOff()
  LedBOff()

######################################################################
# send 'mate' to board
######################################################################

def board_mate_white():
  board_check_off()
  print("LCD: Checkmate! White wins\n")
  print("LED: G,H ON")
  wiringpi.lcdPosition(lcd, 0, 0)
  wiringpi.lcdPuts(lcd, "Checkmate!      ")
  wiringpi.lcdPosition(lcd, 0, 1)
  wiringpi.lcdPuts(lcd, "White wins      ")
  LedGOn()
  LedHOn()

def board_mate_black():
  board_check_off()
  print("LCD: Checkmate! Black wins\n")
  print("LED: G,H ON")
  wiringpi.lcdPosition(lcd, 0, 0)
  wiringpi.lcdPuts(lcd, "Checkmate!      ")
  wiringpi.lcdPosition(lcd, 0, 1)
  wiringpi.lcdPuts(lcd, "Black wins      ")
  LedGOn()
  LedHOn()

  
######################################################################
# send 'draw' to board
######################################################################

def board_draw_stalemate():
  print("LCD: Draw! Stalemate\n")
  print("LED D,E ON")
  wiringpi.lcdPosition(lcd, 0, 0)
  wiringpi.lcdPuts(lcd, "Draw!           ")
  wiringpi.lcdPosition(lcd, 0, 1)
  wiringpi.lcdPuts(lcd, "Stalemate       ")

  LedDOn()
  LedEOn()


def board_draw_fifty():
  print("LCD: Draw! Fifty move rule\n")
  print("LED D,E ON")
  wiringpi.lcdPosition(lcd, 0, 0)
  wiringpi.lcdPuts(lcd, "Draw!           ")
  wiringpi.lcdPosition(lcd, 0, 1)
  wiringpi.lcdPuts(lcd, "Fifty move rule ")

  LedDOn()
  LedEOn()

def board_draw_repetition():
  print("LCD: Draw! Three repetition rule\n")
  print("LED D,E ON")
  wiringpi.lcdPosition(lcd, 0, 0)
  wiringpi.lcdPuts(lcd, "Draw! Three     ")
  wiringpi.lcdPosition(lcd, 0, 1)
  wiringpi.lcdPuts(lcd, "repetitions     ")
  LedDOn()
  LedEOn()

  
######################################################################
# LEDs off
######################################################################

def leds_off():
  print("LEDs OFF")
  LedAllOff()
  
######################################################################
# Show Hint
######################################################################

def showHint(hint):
  print("LCD: Hint: " + hint)
  lcdhint = ''
  #wiringpi.lcdPosition(lcd, 0, 0)
  #wiringpi.lcdPuts(lcd, "Hint            ")
  wiringpi.lcdPosition(lcd, 0, 1)
  lcdhint = "hint: " + hint + "     "
  wiringpi.lcdPuts(lcd, lcdhint)


######################################################################
# MAIN LOOP
######################################################################

wiringpi.lcdPosition(lcd, 0, 0)
wiringpi.lcdPuts(lcd, "piChess powered")
wiringpi.lcdPosition(lcd, 0, 1)
wiringpi.lcdPuts(lcd, "by Stockfish")

# assume new game
print ("LCD: Welcome to piChess")
# Skill level 1-8 - default to 1 - far to good for me to play against!
# see levels() for details...
skill = "8"
depth = "5"
# minimum thinking time - we don't use this
movetime = "2000"
# list of moves
move_list = ""

# initialise UCI engine and setup board for a new game
newGame()
#fen = 'qbnrrnbk/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
setBoardFEN(fen)
setEngineFEN(fen)
hint = "None"

# human makes first move (white) by default - can always force the computer
# to move when asked for input
player = 'HUMAN'

# Game runs continually for the time being, should find a way to turn off/on
# and use a saved position
while True:
  player, fen, move_list, hint, skill, depth = playTurn(player, fen, move_list, hint, skill, depth)

######################################################################
# That's all folks!
######################################################################
