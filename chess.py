import random
from termcolor import colored
from IPython.display import clear_output
import time
# K, k: Vua
# Q, q: Hậu
# R, r: Xe
# B, b: Tượng
# N, n: Mã
# P, p: Tốt
liR = [(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0)]
liL = [(-1,0),(-2,0),(-3,0),(-4,0),(-5,0),(-6,0),(-7,0)]
liD = [(0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7)]
liU = [(0,-1),(0,-2),(0,-3),(0,-4),(0,-5),(0,-6),(0,-7)]
liRD = [(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7)]
liLU = [(-1,-1),(-2,-2),(-3,-3),(-4,-4),(-5,-5),(-6,-6),(-7,-7)]
liRU = [(1,-1),(2,-2),(3,-3),(4,-4),(5,-5),(6,-6),(7,-7)]
liLD = [(-1,1),(-2,2),(-3,3),(-4,4),(-5,5),(-6,6),(-7,7)]
liN = [(1,2),(-1,2),(1,-2),(-1,-2),(2,1),(-2,1),(2,-1),(-2,-1)]
liK = [(0,1),(1,0),(0,-1),(-1,0),(1,1),(-1,1),(1,-1),(-1,-1)]

board = [['r','n','b','q','k','b','n','r'],
         ['p','p','p','p','p','p','p','p'],
         ['_','_','_','_','_','_','_','_'],
         ['_','_','_','_','_','_','_','_'],
         ['_','_','_','_','_','_','_','_'],
         ['_','_','_','_','_','_','_','_'],
         ['P','P','P','P','P','P','P','P'],
         ['R','N','B','Q','K','B','N','R']]

# kiểm tra có thể đi được hay không (Xe, Tượng, Hậu)
def Go(x,y,l,isContinue=False,canFight=True,needFight=False):
  li = []
  for dx,dy in l:
    x1 = x+dx
    y1 = y+dy
    if x1<0 or x1>=8 or y1<0 or y1>=8: 
      if not isContinue: 
        break 
      else: 
        continue
    if board[y1][x1] != '_':
      if canFight and board[y][x].islower() != board[y1][x1].islower():
        li.append((x1,y1))
      if not isContinue: break 
      else: continue
    if not needFight:
      li.append((x1,y1))
  return li


# các nước có thể đi của quân Xe
def Rr(x,y):
  return Go(x,y,liR) + Go(x,y,liL) + Go(x,y,liU) + Go(x,y,liD)

# các nước có thể đi của quân Tượng
def Bb(x,y):
  return Go(x,y,liRD) + Go(x,y,liLU) + Go(x,y,liRU) + Go(x,y,liLD)

# các nước có thể đi của quân Hậu
def Qq(x,y):
  return Rr(x,y) + Bb(x,y)

# các nước có thể đi của quân Mã
def Nn(x,y):
  return Go(x,y,liN,isContinue=True)

# các nước có thể đi của quân Vua
def Kk(x,y):
  return Go(x,y,liK,isContinue=True)

# các nước có thể đi của quân Tốt
def Pp(x,y):
  li = []
  dx = 1
  if not board[y][x].islower():
    dx = -1
  # nước có thể đi
  if y==1 or y==6:
    li = li + Go(x,y,[(0,dx),(0,2*dx)],canFight=False)
  else:
    li = li + Go(x,y,[(0,dx)], canFight=False)
  # nước có thể ăn (tốt ăn chéo)
  li = li + Go(x,y,[(-1,dx),(1,dx)],needFight=True)
  return li

# x, y là tọa độ quân cờ
# islower lượt của quân thường (True) hay quân hoa (False)
# return danh sách tọa độ các nước có thể di chuyển tới
def CanGo(x,y,islower):
  if board[y][x].islower() != islower:
    return []
  if (board[y][x] in "Rr"):
    return Rr(x,y)
  if (board[y][x] in "Nn"):
   return Nn(x,y)
  if (board[y][x] in "Bb"):
    return Bb(x,y)
  if (board[y][x] in "Qq"):
    return Qq(x,y)
  if (board[y][x] in "Kk"):
    return Kk(x,y)
  if (board[y][x] in "Pp"):
    return Pp(x,y)
  return []


def isFinish(board):
  U = False
  L = False
  for _ in board:
    U = U or ('K' in _)
    L = L or ('k' in _)
  return not (U and L)

# return tất cả các nước có thể di chuyển (y,x) -> (y1,x1)
def CanGoList(board,islower):
  li = []
  for y in range(8):
    for x in range(8):
      l = CanGo(x,y,islower)
      for x1,y1 in l:
        li = li + [(y,x,y1,x1)]
  return li

def CPURandomTurn(board,islower):
  #######################################################
  #  Có thể bỏ time.sleep(1) để xem kết quả nhanh hơn   #
  ####################################################### 
  time.sleep(1)
  li = CanGoList(board,islower)
  return random.choice(li)

def CPUMiniMaxTurn(board,islower,depth = 3):
  #######################################################
  #  Nên dùng Minimax với độ sâu từ 2 đến 4             #
  #######################################################
  li = CanGoList(board,islower)
  Max = -1000
  for y,x,y1,x1 in CanGoList(board,islower):
    child = [_[:] for _ in board]
    child[y1][x1] = child[y][x]
    child[y][x] = '_'
    vl = Minimax(child,depth-1,islower,not islower)
    if Max < vl or (Max == vl and random.choice([0,1])==0):
      Max = vl
      r = (y,x,y1,x1)
  return r

# Board: Bàn cờ hiện tại
# islower: lượt của quân viết thường (True) hay quân viết hoa (False)
# return: giá trị của bàn cờ đối với quân viết thường
def value(board,islower): # có thể định nghĩa lại hàm value để minimax luôn win hoặc thua
  vl = 0
  for var in board:
    if 'K' in var:
      x, y = var.index('K'), board.index(var)
      break
    else:
      x, y = -1, -1
  for var in board:
    for i in range(8):
      if (var[i] == 'P'):
        vl += 10
        if (x, y) in CanGo(i, board.index(var), islower):
          vl -= 11
      if (var[i] == 'p'):
        vl -= 10
      if (var[i] == 'R'):
        vl += 30
        if (x, y) in CanGo(i, board.index(var), islower):
          vl -= 11
      if (var[i] == 'r'):
        vl -= 30
      if (var[i] == 'N' or var[i] == 'B'):
        vl += 20
        if (x, y) in CanGo(i, board.index(var), islower):
          vl -= 11
      if (var[i] == 'n' or var[i] == 'b'):
        vl -= 20
      if (var[i] == 'Q'):
        vl += 50
        if (x, y) in CanGo(i, board.index(var), islower):
          vl -= 11
      if (var[i] == 'q'):
        vl -= 50
  
  return vl

# node là node hiện tại
# depth là độ sâu
# Pmax là player cần tìm Max
# Pnow là player hiện tại
def Minimax(node,depth,Pmax,Pnow):
  if isFinish(node) or depth ==0:
    return value(node,Pmax)
  if Pmax == Pnow:
    Max = -1000
    for y,x,y1,x1 in CanGoList(node,Pnow):
      child = [_[:] for _ in node]
      child[y1][x1] = child[y][x]
      child[y][x] = '_'
      Max = max(Max,Minimax(child,depth-1,Pmax,not Pnow))
    return Max
  else:
    Min = 1000
    for y,x,y1,x1 in CanGoList(node,Pnow):
      child = [_[:] for _ in node]
      child[y1][x1] = child[y][x]
      child[y][x] = '_'
      Min = min(Min,Minimax(child,depth-1,Pmax,not Pnow))
    return Min


def printBoard(board):
  print("+",*range(8),"+")

  for i in range(8):
    print(i,end=" ")
    for j in range(8):
      if board[i][j] == '_':
        print(board[i][j],end=" ")
      elif board[i][j].islower():
        print(colored(board[i][j],'red'),end=" ")
      else:
        print(colored(board[i][j],'blue'),end=" ")
    print(i,) 

  print("+",*range(8),"+")
  print()

Random = True
MiniMax = False
Now = Random

while not isFinish(board):
  clear_output()
  printBoard(board)
  print("----",Now,"turn","----")
  if Now == MiniMax:
    y,x,y1,x1 = CPUMiniMaxTurn(board,MiniMax)
    board[y1][x1] = board[y][x]
    board[y][x] = '_'
    Now = Random
    print(y,x,y1,x1)
  else:
    y,x,y1,x1 = CPURandomTurn(board,Random)
    board[y1][x1] = board[y][x]
    board[y][x] = '_'
    print(y,x,y1,x1)
    Now = MiniMax

printBoard(board)
if Now:
  print("Minimax Won")
else:
  print("Random Won")