#Email: Java12man@gmail.com
#Dalton Kolb-Connolly
import pygame
import queue
from random import randint
import argparse
import re
def stringify(board):
    st = ""
    for n in board:
        for r in n:
            st += r
    return st
class GameState:
    def __init__(self,boardState,pieces,prev):
        self.prev = prev
        self.pieces = pieces
        self.boardState = boardState
    def movePieceLeft(self,piece):
        newBoard = [r[:] for r in self.boardState]
        height = len(newBoard)
        length = len(newBoard[0])
        newpieces = self.pieces.copy()
        piecepos = newpieces[piece]
        for x in range(piecepos[0],piecepos[0]+2):
            for y in range(piecepos[1],piecepos[1]+2):
                if newBoard[y][x] == piece:
                    if newBoard[y][x-1] == "F":
                        newBoard[y][x-1] = piece
                        newBoard[y][x] = "F"
                    else:
                        return False
        newpieces[piece]=(piecepos[0]-1,piecepos[1])
        return (newBoard,newpieces)
    def movePieceUp(self,piece):
        newBoard = [r[:] for r in self.boardState]
        height = len(newBoard)
        length = len(newBoard[0])
        newpieces = self.pieces.copy()
        piecepos = newpieces[piece]
        for y in range(piecepos[1],piecepos[1]+2):
            for x in range(piecepos[0],piecepos[0]+2):
                if newBoard[y][x] == piece:
                    if newBoard[y-1][x] == "F":
                        newBoard[y-1][x] = piece
                        newBoard[y][x] = "F"
                    else:
                        return False
        newpieces[piece]=(piecepos[0],piecepos[1]-1)
        return (newBoard,newpieces)
    def movePieceRight(self,piece):
        newBoard = [r[:] for r in self.boardState]
        height = len(newBoard)
        length = len(newBoard[0])
        newpieces = self.pieces.copy()
        piecepos = newpieces[piece]
        for x in range(piecepos[0]+1,piecepos[0]-1,-1):
            for y in range(piecepos[1],piecepos[1]+2):
                if newBoard[y][x] == piece:
                    if newBoard[y][x+1] == "F":
                        newBoard[y][x+1] = piece
                        newBoard[y][x] = "F"
                    else:
                        return False
        newpieces[piece]=(piecepos[0]+1,piecepos[1])
        return (newBoard,newpieces)
    def movePieceDown(self,piece):
        newBoard = [r[:] for r in self.boardState]
        height = len(newBoard)
        length = len(newBoard[0])
        newpieces = self.pieces.copy()
        piecepos = newpieces[piece]
        for x in range(piecepos[0],piecepos[0]+2):
            for y in range(piecepos[1]+1,piecepos[1]-1,-1):
                if newBoard[y][x] == piece:
                    if newBoard[y+1][x] == "F":
                        newBoard[y+1][x] = piece
                        newBoard[y][x] = "F"
                    else:
                        return False
        newpieces[piece]=(piecepos[0],piecepos[1]+1)
        return (newBoard,newpieces)
    def compare(self,other):
        r = 0
        for row in self.boardState:
            x = 0
            for p in row:
                if p != other.boardState[r][x]:
                    return False
                x+=1
            r+=1
        return True
    def minimizeMemory(self):
        self.pieces = None

boardText = """
v1 b1 b1 v2
v1 b1 b1 v2
F h1 h1 F
v3 s1 s2 v4
v3 s3 s4 v4
"""
example = """
v1 b1 b1 v2
v1 b1 b1 v2
F h1 h1 F
v3 F F v4
v3 F F v4
"""
SCALE = 128
def showAnimation(gamestates, pieces):
    firstFrame = gamestates.get()
    height = len(firstFrame)
    width = len(firstFrame[0])
    dim =(SCALE*width,SCALE*height)
    screen = pygame.display.set_mode(dim)

    pygame.display.flip()
    #Display Generating Frames Text progress bar if it actualy takes time but I doubt it will
    frames = []
    gamestates.put(firstFrame)
    colors = {"X":(10,10,20,100),"F":(1,1,1,100),"V":(1,30,30,100)}
    while not gamestates.empty():
        newSurf = pygame.Surface((SCALE*width,SCALE*height))
        board = gamestates.get()
        xpos = 0
        ypos = 0
        for row in board:
            xpos=0
            for cell in row:
                if cell in colors:
                    color = colors[cell]
                else:
                    color = ((360/(len(pieces)+1)*len(colors))%359+1,90,90,100)
                    colors[cell]=color
                pcolor = pygame.Color(0,0,0)
                #print(color)
                pcolor.hsva = color
                square = pygame.Rect(xpos*SCALE,ypos*SCALE,SCALE,SCALE)
                pygame.draw.rect(newSurf,pcolor,square)
                xpos+=1
            ypos+=1
        frames.append(newSurf)
    frameID = 0
    oldFrameID = -1
    print("Moves =",len(frames))
    while -1:
        pygame.time.wait(100)
        for EVENT in pygame.event.get():
            if EVENT.type == pygame.QUIT:
                exit()
            if EVENT.type == pygame.KEYDOWN:
                if EVENT.key == pygame.K_ESCAPE:
                    exit()
                if EVENT.key == pygame.K_LEFT:
                    frameID += -1
                if EVENT.key == pygame.K_RIGHT:
                    frameID += 1


        if frameID != oldFrameID:
            frameID = frameID%len(frames)
            screen.blit(frames[frameID],(0,0))
            oldFrameID = frameID
            pygame.display.flip()



def solve(inputText):
    print("SOLVING")
    br = inputText.strip().split('\n')
    board = [["X" for i in range(6)]]
    for r in br:
        row = ["X"]
        row.extend(r.split(" "))
        row.append("X")
        board.append(row)
    board.append(["X","X","V","V","X","X"])
    #print(board)
    #pieces = ["v1","v2","v3","v4","b1","h1","s1","s2","s3","s4"] #"h1","s1","s2","s3","s4"
    pieces = set()
    pieceLocations = {}
    h = 1
    for r in br:
        x = 1
        for w in r.split(" "):
            if w != 'F':
                pieces.add(w)
                if w not in pieceLocations:
                    pieceLocations[w]=(x,h)
            x+=1
        h+=1
    #print(pieces)
    q = queue.Queue()


    startingState = GameState(board,pieceLocations,"NONE")
    q.put(startingState)
    visited = {}
    visited[stringify(startingState.boardState)] = "True"
    while not q.empty():
        current = q.get()
        currentBoard = current.boardState
        if currentBoard[5][2] == "b1" and currentBoard[5][3] == "b1":
            retrace = queue.LifoQueue()
            print("SOLUTION FOUND!")
            oh = open(infile,'r')
            p = current
            while p != "NONE":
                retrace.put(p.boardState)
                oh.write(repr(p.boardState)+"\n")
                p = p.prev
            showAnimation(retrace,pieces)
            oh.close()
            return 0

        for piece in pieces:
            options = []
            options.append(current.movePieceUp(piece))
            options.append(current.movePieceDown(piece))
            options.append(current.movePieceLeft(piece))
            options.append(current.movePieceRight(piece))
            for op in options:
                if op != False:
                    invisited = False
                    opState = GameState(op[0],op[1],current)
                    sv = stringify(op[0])
                    if sv not in visited:
                        q.put(opState)
                        visited[sv] = "True"
        current.minimizeMemory()
    print("IMPOSSIBLE")
def main():

    parser = argparse.ArgumentParser(description = "Welcome to Dalton Kolb-Connolly's implimentation of OLAP.py")
    parser.add_argument('--view',action = 'store',required=False)
    parser.add_argument('--solve',action = 'store',required=False)
    args = parser.parse_args()
    infile = args.solve
    mode = "solve"
    if infile == None:
        infile = args.view
        mode = "view"
        if infile == None:
            exit()
    if mode == "solve":
        fh = open(infile)
        t = fh.read()
        with open(infile+"_solution.txt",'w') as oh:
            solve(t)
    else:
        fh = open(infile)
        stack = queue.LifoQueue()
        text = fh.read()
        getInsideBrackets = re.compile('\[(.*)\]')
        pieces = set()
        for line in text.strip().split('\n'):
            arr = []
            outerBrackets = re.search(getInsideBrackets,line)
            if outerBrackets != None:
                board = outerBrackets[1]
                for row in board.split('['):
                    row = row.split(']')[0]
                    row = row.replace('\'','')
                    row = row.replace(' ','')
                    if len(row) > 1:
                        arr.append(row.split(','))
            stack.put(arr)
            for r in arr:
                for w in r:
                    if w != 'F':
                        pieces.add(w)
        showAnimation(stack,pieces)
if __name__ == "__main__":
    main()
