# -*- coding: utf-8 -*-
"""
Created on Sun Dec  8 10:44:34 2019

@author: Viljar Femoen
"""
import tkinter
import random

#TODO gjør så space ikke er restart

#Declares a couple hex colors for the board. All values must be different
body='#30a820'
head='#3bc227'
tail='#30a821'
apple='red'
tile='#9c6a32'

#Keeps track of wether the snake recently ate an apple, and the score
appleEaten=0
score=0
submitscore=False
playername=''

#Desc:      Creates the tkinter board
#Input:     board:  list of lists of colors
#Output:    root:   tkinter master
def drawBoard(board):
    
    #Create the tkinter master
    root=tkinter.Tk()
    root.title('Snake')
    
    #Create and place a square for each element in board
    for y in range(len(board)):
        for x in range(len(board)):
            tkinter.Canvas(root, width=15, height=15, bg=board[y][x], highlightthickness=0, relief='ridge').grid(row=y, column=x)
    
    #Create and place a textbox for highscores, and one for instructions
    hsTextBox=tkinter.Text(root, height=6, width=30)
    hsTextBox.place(x=15*len(board), y=0)
    
    #Create content for the highscorebox
    hsText='Highscore list:\n'
    hsList=getHighScores()
    hsScores=[int(i[1]) for i in hsList]
    for x in range(min(5, len(hsList))):
        maxIndex=hsScores.index(max(hsScores))
        #ugly code to make the text pretty
        hsText+='{}. {}'.format(x+1, hsList[maxIndex][0])+str(max(hsScores)).rjust(22-len(hsList[maxIndex][0])+len(max(hsList)))+'\n'
        hsScores[maxIndex]=-1
    hsTextBox.insert('0.0', hsText)
        
    return root


#Desc:      Create the highscore file
#Input:     None
#Output:    None
def createHighScoreFile():
    try: 
        open('Snake_Highscores.txt','r')
    except:
        f=open('Snake_Highscores.txt','w')
        f.write('Snake highscore list (sorted by date)\n')
        f.close()


#Desc:      Gets a list of highscores
#Input:     None
#Output:    List of lists of strings
def getHighScores():
    try:
        f=open('Snake_Highscores.txt','r')
        highscorelist=[s.split(': ') for s in f.read().split('\n')]
        f.close()
        return highscorelist[1:-1]
    except:
        createHighScoreFile()
        getHighScores()


#Desc:      Adds a player to the highscorelist
#Input:     playername:     str, the name entered by the player
#           score:          int, the length of the snake when it died
#Output:    None
def addHighScore(playername, score, cond=True):
    if cond:
        try:
            open('Snake_Highscores.txt','r')
        except:
            createHighScoreFile()
        f=open('Snake_Highscores.txt','a')
        f.write(str(playername)+': '+str(score)+'\n')
        f.close()

#Desc:      Creates a board of size "size", all with the "tile" value
#Input:     size:   int
#Output:    board:  board
#Comment:   Minimum size is 9
def makeBoard(size):
    
    if size>=9:
        return [[tile for x in range(size)] for y in range(size)]
    
    else:
        raise ValueError("Size too small")


#Desc:      Updates the current tkinter board with the input board
#Input:     board:  board
#           root:   tkinter master
#Output:    root:   tkinter master
def updateDrawBoard(board, root):
    
    #Creates a list of the board tiles
    tileList=root.grid_slaves()
    
    #Loops through each tile
    for y in range(len(board)):
        for x in range(len(board)):
            #Updates the tile if necessary
            if tileList[len(board)*y+x].cget('bg') != board[y][x]:
                tileList[len(board)*y+x].configure(bg=board[y][x])
                
    return root


#Desc:      Adds a snake to the board
#Input:     board:  board
#Output:    board:  board
#Comment:   The snake is placed with its head in the center, and faces right.
#           The snake is 4 units long
def makeSnake(board):
    
    size=len(board)
    
    #Creates the body
    for x in range(3):
        board[size//2][size//2+x]=body
    
    #Creates the head and tail
    board[size//2][size//2]=head
    board[(size//2)][size//2+3]=tail
    
    return board


#Desc:      Calculates the length of the snake
#Input:     board:  board
#Output:    length: int
def snakeLength(board):
    
    length=0
    
    for y in board:
        for x in y:
            #Adds 1 if the current tile is a snake part
            if x in [head, body, tail]:
                length+=1
                
    return length


#Desc:      Adds an apple to the board
#Input:     board:  board
#Output:    board:  board
#Comment:   Will add exactly one apple on a single empty tile
def makeApple(board):
    
    #Creates an empty list of possible apple positions
    poslist=[]
    
    #Loop through the board to find possible positions
    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x]==tile:
                poslist.append([x,y])
    
    #Picks a random tile from poslist, and makes it an apple
    pos=random.choice(poslist)
    board[pos[1]][pos[0]]=apple
    
    return board


#Desc:      Counts the amount off apples on the board
#Input:     board:  board
#Output:    count:  int
#Comment:   Should never be more than 1
def appleCount(board):
    
    count=0
    
    for y in board:
        for x in y:
            #Adds 1 if the current tile is an apple
            if x==apple:
                count+=1
                
    return count
   

#Desc:      Moves the snake in a given direction
#Input:     Direction:  str. The direction for the move. Capitalized and enclosed in <>
#           board:      board
#           movelist:   list of previous directions
#Output:    board:      board
#           movelist:   movelist
#Comment:   Contains the logic for apple eating, and subsequent apple creation
def move(direction, board, movelist):
    
    global appleEaten
    global score
    snakelength=snakeLength(board)
    
    #Adds the direction to the movelist
    movelist.append(direction)
    
    #Reduces the global variable appleEaten if necessary
    if appleEaten >0:
        appleEaten-=1
    
    #Find the position of the head and tail, and store them in pos and tailpos
    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x]==head:
                pos=[x,y]
    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x]==tail:
                tailpos=[x,y]
    
    #Move the head one tile in the correct direction
    if movelist[-1]=='<Right>':
        board[pos[1]][pos[0]-1]=head
        board[pos[1]][pos[0]]=body
    if movelist[-1]=='<Left>':
        board[pos[1]][pos[0]+1]=head
        board[pos[1]][pos[0]]=body
    if movelist[-1]=='<Up>':
        board[pos[1]+1][pos[0]]=head
        board[pos[1]][pos[0]]=body
    if movelist[-1]=='<Down>':
        board[pos[1]-1][pos[0]]=head
        board[pos[1]][pos[0]]=body
    
    #Intcrements appleEaten if there are no apples, and adds another one
    if appleCount(board) == 0:
        score+=100
        score += ((snakelength-4)//2)*10
        appleEaten+=2
        makeApple(board)
    
    #Moves the tail if no apple was recently eaten
    if appleEaten==0:
        #If the game has lasted for 3 moves, move the tail in the direction the head moved when it was there
        if len(movelist) >= snakelength:
            if movelist[-snakelength]=='<Right>':
                board[tailpos[1]][tailpos[0]]=tile
                board[tailpos[1]][tailpos[0]-1]=tail
            if movelist[-snakelength]=='<Left>':
                board[tailpos[1]][tailpos[0]]=tile
                board[tailpos[1]][tailpos[0]+1]=tail
            if movelist[-snakelength]=='<Up>':
                board[tailpos[1]][tailpos[0]]=tile
                board[tailpos[1]+1][tailpos[0]]=tail
            if movelist[-snakelength]=='<Down>':
                board[tailpos[1]][tailpos[0]]=tile
                board[tailpos[1]-1][tailpos[0]]=tail
        
        #If the game has just begun, move the tail to the right
        else:
            board[tailpos[1]][tailpos[0]]=tile
            board[tailpos[1]][tailpos[0]-1]=tail
            
    return board, movelist
      

#Desc:      The loop that makes the snake move
#Input:     board:      board
#           movequeue:  list of moves, input by the player
#           movelist:   movelist
#           root:       tkinter master
#Output:    None
#Comment:   Also contains the logic for losing the game
def loopMove(board, movequeue, movelist, root):
    if len(movequeue)==0:
        root.after(50, loopMove, board, movequeue, movelist, root)
    elif killCheck(board, movequeue[-1], root):
        move(movequeue[-1], board, movelist)
        updateDrawBoard(board, root)
        root.after(100, loopMove, board, movequeue, movelist, root)


#Desc:      Creates a child window with restart/quit options
#Input:     root:   tkinter master
#Output:    False
def drawDeathWindow(root):

    global submitscore
    global playername
    
    #Creates the child window
    deathwindow=tkinter.Toplevel(root)
    deathwindow.title('You lost')
    
    #Creates a textbox in the child window
    textbox=tkinter.Text(deathwindow, height=3, width=35)
    textbox.insert('0.0', 'You lost. Enter your name in the \nhighscore-list. Press the spacebar to retry or Escape to quit.')
    textbox.place(x=0, y=0, anchor=tkinter.NW)
    
    #Creates an entry widget for the playername, and a submit-button
    playernameInput=tkinter.Entry(deathwindow)
    playernameInput.delete(0,tkinter.END)
    playernameInput.insert(0, 'Enter your name')
    playernameInput.place(x=150, y=65, anchor=tkinter.CENTER)
    tkinter.Button(deathwindow, text='Submit', command=secret).place(x=280, y=65, anchor=tkinter.E)
    
    #Binds the esc and spacebar to quit and restart
    deathwindow.bind('<space>', lambda x: restart(root))
    deathwindow.bind('<Escape>', lambda x: root.destroy())

    #Clears the entry widget if you hover over it
    playernameInput.bind('<Motion>', lambda x: clearEntryWidget(playernameInput))
    
    #Binds the enter key to the submit button
    deathwindow.bind('<Return>', lambda x: secret())
    
    #Creates a restart button and a quit button
    tkinter.Button(deathwindow, text='Restart', command=lambda: restart(root)).place(x=20, y=65, anchor=tkinter.W)
    tkinter.Button(deathwindow, text='Quit', command= lambda: root.destroy()).place(x=20, y=85, anchor=tkinter.W)
    
    #Sets the child window size, and makes it take focus
    deathwindow.geometry('300x100')
    deathwindow.grab_set()
    deathwindow.focus_set()
    
    deathwindow.after(50, getPlayerName, playernameInput, deathwindow)

    return False

def getPlayerName(entry, child):
    global playername
    playername=entry.get()
    if submitscore:
        return
    child.after(50, getPlayerName, entry, child)
    
def secret():
    global submitscore
    submitscore=True

#Desc:      Clears the entry widget in the death window if the mouse is over it
#Input:     motion:     tkinter motion object
#           playername:      tkinter entry widget
#Output:    None
def clearEntryWidget(playername):
    if playername.get()=='Enter your name':
        playername.delete(0,tkinter.END)
    
    
#Desc:      Changes a tkinter keypress object to a direction
#Input:     moveinput:  tkinter keypress object
#Output:    direction
def pruneMoveInput(moveinput):
    
    for i in ['Right', 'Left', 'Up', 'Down']:
        if i in str(moveinput):
            return('<'+i+'>')


#Desc:      Checks wether the next move will kill the snake
#Input:     board:      board
#           direction:  direction
#           root:       tkinter master
#Output:    Boolean
#Comment:   If the output is False, drawDeathWindow will also run
def killCheck(board, direction, root):
    
    #Finds the position of the head
    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x]==head:
                headpos=[x,y]
                
    #Checks the correct direction for a wall or snake tile
    if direction=='<Right>':
        if (headpos[0]==0) or (board[headpos[1]][headpos[0]-1] in [body, tail]):
            return drawDeathWindow(root)
    if direction=='<Left>':
        if (headpos[0]==len(board)-1) or (board[headpos[1]][headpos[0]+1] in [body, tail]):
            return drawDeathWindow(root)
    if direction=='<Up>':
        if (headpos[1]==len(board)-1) or (board[headpos[1]+1][headpos[0]] in [body, tail]):
            return drawDeathWindow(root)
    if direction=='<Down>':
        if (headpos[1]==0) or (board[headpos[1]-1][headpos[0]] in [body, tail]):
            return drawDeathWindow(root)
        
    #Return True if the move will not kill the snake   
    return True
            

#Desc:      Restart the game
#Input:     root:   tkinter master
#Output:    None
def restart(root):
    
    #Destroy the tkinter master window and start over
    root.destroy()
    main()
    

#Desc:      Runs the game
#Input:     None
#Output:    None
def main():
    
    #Reset appleEaten and stuff
    global appleEaten
    global score
    global submitscore
    submitscore=False
    score=0
    appleEaten=0
    createHighScoreFile()
    
    #Creates the movequeue
    movequeue=[]
    
    #Initializes movelist and a 30x30 board
    movelist=[]
    board=makeBoard(30)
    
    #Add a snake and an apple to the board
    makeSnake(board)
    makeApple(board)
    
    #Create the tkinter window for the game, and make it take focus
    root=drawBoard(board)
    root.focus_force()
    
    #Ensures the board is updated
    updateDrawBoard(board, root)
    
    #Bind the arrow keys to move the snake, by adding the direction to movequeue
    root.bind('<Right>', lambda x: [movequeue.append(pruneMoveInput(x))])
    root.bind('<Left>', lambda x: [movequeue.append(pruneMoveInput(x))])
    root.bind('<Up>', lambda x: [movequeue.append(pruneMoveInput(x))])
    root.bind('<Down>', lambda x: [movequeue.append(pruneMoveInput(x))])
    
    #Adds the score to the score document when the window closes
    root.bind('<Destroy>', lambda x: [addHighScore(playername, score, submitscore) for i in [0] if x.widget is root])
    
    #Wait 1 secons, then move the snake every 0.1 seconds
    root.after(1000, loopMove, board, movequeue, movelist, root)

    root.geometry('{}x{}'.format(15*len(board)+250,15*len(board)))
    #Start the game
    root.mainloop()
    

main()