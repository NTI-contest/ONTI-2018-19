from pwn import *

board = [[b'_', b'_', b'_'], [b'_', b'_', b'_'], [b'_', b'_', b'_']]

win_combos = [
    [(0,0), (0,1), (0,2)],
    [(1,0), (1,1), (1,2)],
    [(2,0), (2,1), (2,2)],
    [(0,0), (1,0), (2,0)],
    [(0,1), (1,1), (2,1)],
    [(0,2), (1,2), (2,2)],
    [(0,0), (1,1), (2,2)],
    [(2,0), (1,1), (0,2)]
]

win_counter = 0

conn = remote("tictactoe.2018.cyberchallenge.ru", 9002)
conn.recvlines(timeout=1)

def read_board():
    reply = conn.recvlines(timeout=0.5)

    i = reply.index(b'  0 1 2 ')

    board[0] = reply[i + 1][2:].split(b' ')
    board[1] = reply[i + 2][2:].split(b' ')
    board[2] = reply[i + 3][2:].split(b' ')

def count_char(char, cells):
    count = 0
    for cell in cells:
        if board[cell[0]][cell[1]] == char:
            count += 1
    return count

def find_free(cells):
    for cell in cells:
        if board[cell[0]][cell[1]] == b'_':
            return cell

    return (-1, -1)

def do_move(cell):
    conn.sendline(str(cell[0]) + " " + str(cell[1]))

def select_move():
    global win_counter
    xCount = sum([row.count(b'x') for row in board])
    if xCount == 0:
        do_move((1,1))
        return

    for wc in win_combos:
      if count_char(b'x', wc) == 2:
         choice = find_free(wc)
         if choice != (-1, -1):
            do_move(choice)
            print(conn.recvline(timeout=0.5))
            win_counter += 1
            print("Wins: " + str(win_counter))
            if win_counter == 100:
                print(conn.recvline(timeout=0.5))
            return
    
    for wc in win_combos:
      if count_char(b'o', wc) == 2:
         choice = find_free(wc)
         if choice != (-1, -1):
            do_move(choice)
            return
    
    choice = find_free([(0,0), (2,0), (0,2), (2,2)])
    if choice != (-1, -1):
        do_move(choice)
        return
    
    choice = find_free([(0,1), (1,0), (1,2), (2,1)])
    do_move(choice)
    print(conn.recvline(timeout=0.5))
    return

while True:
    select_move()
    read_board()