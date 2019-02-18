

LANGUAGES:

1. Compiler
	/Python + C/
	Has its own Readme in folder.

2. Interpreter
	/Java/ 
	To compile - javac Evaluator.java. 
	To run - java Evaluator.
	A CLI evaluator for expressions for the above compiler.
	Has fewer features than the compiled version - is a proof of concept

3. Querylang
	/Java/
	A databse language.

	Compile with javac Dbsys.java
	Run with java Dbsys *database*
	
	*database* is a text file in the form of family.txt.
	It must contain data items and rules.
	Family.txt has an example database and a few rule examples.
	(SICP inspired with a few variations)

	Folder contains a text file with example queries and results.

GAMES:

1. Antichess.
	/Python + C/
	Download as folder and cd to it.
	Run gcc -Wall -O3 IDalpha_beta.c boards_and_pieces.c -o IDalpha_beta
	To play - python3 antichess.py
2. Snake
	Download script in snake folder
	Run python3 snake.py.
3. Tetris
	Downlaod scirpt in tetris folder.
	Run python3 tetris_int.py

4. Nine men's morris
	Download 'dama' folder
	Run python3 dama.py

5. Conway's game of life
	Runs with python3 conwayGame.py
	Click on the black boxes to toggle them.
	Continuously click enter to advance generations.	
	
6. CLI games
	Any game in the folder gets run with python3 *filename*.
	All of the scripts require the ansi_colors.py library.
	Some require the words.txt file.
	Contains:
		Haiku generating script
		Blackjack
		Maze illustration
		Picross
		Sudoku
                Sudoku solver (example input file in folder, give as cli arg)
		Typing speed tester
		Hunt the wumpus
MISC:

1. Single use scripts
	Run script with python3
	Contains:
		Analog clock (GUI)
		Calculator (CLI - RPN and op precedence)
		Thumbnail viewer (python3 thump.py *directory*)
		Ascii clock (CLI)
		Sierpinski triangle (GUI)
		Ulam spiral (GUI)
		

2. Digits
	A solution to the mnist digit recognition - http://yann.lecun.com/exdb/mnist/.
	Practicing matrices and logistic regression.
	Used pypy and python2 - about 13 % error rate. 

3. Poker
	Runs with python3 pokerUI.py
	First it asks for a hand
	Then it asks for what the board looks like
	Then it evaluates your probabilities of win,loss or tie versing one opponent


