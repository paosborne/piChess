# piChess
Raspberry Pi Chess Computer

Goal to make a 1980's style chess computer using a Raspberry Pi. I was planning on adding a load of buttons and LCD driven via MCP23017s - have changed my mind here and will instead use a TFT touch screen on the pi for messages from the computer and game management.

All moves though will be via the physical board using magnets and reed switches set up as a keyboard matrix.

This is a labour of love, no rush just gently tinkering as and when I get time which is usually half an hour here and there.

This project blatantly uses ChessBoard found at: http://pygame.org/   with GPL - so my backside is covered.

The bulk of my code is in interface.py this is the bit that talks between a real physical chess board, the chess engine (stockfish), Chessboard.py (used to validate the human moves and referee the game) and the human player.

This is the first bit of python I have written, its not pretty to be honest and I am learning as I go along.

If you want to take the code and do something with it, help yourself - it's at your own risk as the code is probably bug ridden - as I find them I either fix them or ignore them for the moment.

Finally - I know I am not the first person to do this, I won't be the last. 

Ta 

Paul
