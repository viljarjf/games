# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 17:02:57 2019

@author: Viljar Femoen
"""
import tkinter
import numpy
import random

tile='#cbc2b3'
numColors=['#eee6db','#ece0c8','#efb27c','#f39768', '#f37d63', '#f46042', '#eacf76', '#edcb67', '#ecc85a', '#e7c257', '#e8be4e']


def makeBoard(size):
    return [[[tile, 0] for x in range(size)] for y in range(size)]

def initDrawBoard(board):
    root=tkinter.Tk()
    for y in range(len(board)):
        for x in range(len(board)):
            temp=tkinter.Canvas(root, width=170, height=170, bg=board[y][x][0])
            if board[y][x][1]==0:
                temp.create_text(170//2,170//2, text='', font=('Comic Sans MS', '50'), fill='black')
            else:
                temp.create_text(170//2,170//2, text=str(board[y][x][1]), font=('Comic Sans MS', '50'), fill='black')
            temp.grid(column=x, row=y)
    root.title('2048')
    return root
    
def makeNum(board, pos, num):
    x=pos[0]
    y=pos[1]
    if num==0:
        board[y][x]=[tile, num]
    else:
        ind=int(numpy.log2(num))-1
        board[y][x]=[numColors[ind], num]
    return board

def updateBoard(board, root):
    tileList=root.grid_slaves()
    tileList.reverse()
    for y in range(len(board)):
        for x in range(len(board)):
            ind=len(board)*y+x
            tileList[ind].config(bg=board[y][x][0])
            if board[y][x][1]==0:
                tileList[ind].itemconfig(1, text='')
            else:
                tileList[ind].itemconfig(1, text=board[y][x][1])
                
            
def move(board, direction):
    if direction == 'Up':
        for y in range(len(board)-1):
            for x in range(len(board)):
                if board[y][x]==board[y+1][x]:
                    makeNum(board, [x,y], board[y][x][1]*2)
                    makeNum(board, [x, y+1], 0)
                if board[y][x][1]==0:
                    makeNum(board, [x,y], board[y+1][x][1])
                    makeNum(board, [x, y+1], 0)
                if y<2:
                    if board[y][x]==board[y+2][x] and board[y+1][x][1]==0:
                        makeNum(board, [x,y], board[y][x][1]*2)
                        makeNum(board, [x, y+2], 0)
                    if board[y][x][1]==0 and board[y+1][x][1]==0:
                        makeNum(board, [x,y], board[y+2][x][1])
                        makeNum(board, [x, y+2], 0)
                if y==0:
                    if board[y][x]==board[y+3][x] and board[y+1][x][1]==0 and board[y+2][x][1]==0:
                        makeNum(board, [x,y], board[y][x][1]*2)
                        makeNum(board, [x, y+3], 0)
                    if board[y][x][1]==0 and board[y+1][x][1]==0 and board[y+2][x][1]==0:
                        makeNum(board, [x,y], board[y+3][x][1])
                        makeNum(board, [x, y+3], 0)
    if direction == 'Down':
        for y in range(len(board)-1, 0, -1):
            for x in range(len(board)):
                if board[y][x]==board[y-1][x]:
                    makeNum(board, [x,y], board[y][x][1]*2)
                    makeNum(board, [x, y-1], 0)
                if board[y][x][1]==0:
                    makeNum(board, [x,y], board[y-1][x][1])
                    makeNum(board, [x, y-1], 0)
                if y>1:
                    if board[y][x]==board[y-2][x] and board[y-1][x][1]==0:
                        makeNum(board, [x,y], board[y][x][1]*2)
                        makeNum(board, [x, y-2], 0)
                    if board[y][x][1]==0 and board[y-1][x][1]==0:
                        makeNum(board, [x,y], board[y-2][x][1])
                        makeNum(board, [x, y-2], 0)
                if y==3:
                    if board[y][x]==board[y-3][x] and board[y-1][x][1]==0 and board[y-2][x][1]==0:
                        makeNum(board, [x,y], board[y][x][1]*2)
                        makeNum(board, [x, y-3], 0)
                    if board[y][x][1]==0 and board[y-1][x][1]==0 and board[y-2][x][1]==0:
                        makeNum(board, [x,y], board[y-3][x][1])
                        makeNum(board, [x, y-3], 0)
    if direction == 'Left':
        for x in range(len(board)-1):
            for y in range(len(board)):
                if board[y][x]==board[y][x+1]:
                    makeNum(board, [x,y], board[y][x][1]*2)
                    makeNum(board, [x+1, y], 0)
                if board[y][x][1]==0:
                    makeNum(board, [x,y], board[y][x+1][1])
                    makeNum(board, [x+1, y], 0)
                if x<2:
                    if board[y][x]==board[y][x+2] and board[y][x+1][1]==0:
                        makeNum(board, [x,y], board[y][x][1]*2)
                        makeNum(board, [x+2, y], 0)
                    if board[y][x][1]==0 and board[y][x+1][1]==0:
                        makeNum(board, [x,y], board[y][x+2][1])
                        makeNum(board, [x+2, y], 0)
                if x==0:
                    if board[y][x]==board[y][x+3] and board[y][x+1][1]==0 and board[y][x+2][1]==0:
                        makeNum(board, [x,y], board[y][x][1]*2)
                        makeNum(board, [x+3, y], 0)
                    if board[y][x][1]==0 and board[y][x+1][1]==0 and board[y][x+2][1]==0:
                        makeNum(board, [x,y], board[y][x+3][1])
                        makeNum(board, [x+3, y], 0)
    if direction == 'Right':
        for x in range(len(board)-1, 0, -1):
            for y in range(len(board)):
                if board[y][x]==board[y][x-1]:
                    makeNum(board, [x,y], board[y][x][1]*2)
                    makeNum(board, [x-1, y], 0)
                if board[y][x][1]==0:
                    makeNum(board, [x,y], board[y][x-1][1])
                    makeNum(board, [x-1, y], 0)
                if x>1:
                    if board[y][x]==board[y][x-2] and board[y][x-1][1]==0:
                        makeNum(board, [x,y], board[y][x][1]*2)
                        makeNum(board, [x-2, y], 0)
                    if board[y][x][1]==0 and board[y][x-1][1]==0:
                        makeNum(board, [x,y], board[y][x-2][1])
                        makeNum(board, [x-2, y], 0)
                if x==3:
                    if board[y][x]==board[y][x-3] and board[y][x-1][1]==0 and board[y][x-2][1]==0:
                        makeNum(board, [x,y], board[y][x][1]*2)
                        makeNum(board, [x-3, y], 0)
                    if board[y][x][1]==0 and board[y][x-1][1]==0 and board[y][x-2][1]==0:
                        makeNum(board, [x,y], board[y][x-3][1])
                        makeNum(board, [x-3, y], 0)
    return board

def pruneMoveInput(moveinput):
    for i in ['Right', 'Left', 'Up', 'Down']:
        if i in str(moveinput):
            return(i)

def addTile(board):
    posList=[]
    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x][1]==0:
                posList.append([x,y])
    pos=random.choice(posList)
    num=random.choice([4]+[2]*9)
    makeNum(board, pos, num)
    return board

def completeMoveFunc(board, root, directionObject):
    direction=pruneMoveInput(directionObject)
    if lossCheck(board):
        score=sum([sum([x[1] for x in y]) for y in board])
        root.title(f'You lost. Score: {score}')
    elif isLegalMove(board, direction):
        move(board, direction)
        addTile(board)
        updateBoard(board, root)

def isLegalMove(board, direction):
    oldBoard=[[x for x in y] for y in board]
    if move(oldBoard, direction)==board:
        return False
    return True

def lossCheck(board):
    #Is this loss?
    dirs=['Left', 'Right', 'Up', 'Down']
    for direction in dirs:
        if isLegalMove(board, direction):
            return False
    return True
    
def main():
    board=makeBoard(4)
    root=initDrawBoard(board)
    addTile(board)
    addTile(board)
    updateBoard(board, root)
    root.bind('<Right>', lambda x: completeMoveFunc(board, root, x))
    root.bind('<Left>', lambda x: completeMoveFunc(board, root, x))
    root.bind('<Up>', lambda x: completeMoveFunc(board, root, x))
    root.bind('<Down>', lambda x: completeMoveFunc(board, root, x))
    root.focus_force()
    root.mainloop()

main()