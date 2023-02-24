import random
from enum import Enum
from colorama import Fore, Back
import pprint
import os


class state(Enum):
    hidden = 1
    revealed = 2
    flagged = 3


class Grid():
    def __init__(self, x, y, count):
        pregrid = []
        self.pregrid = pregrid
        self.x = x
        self.y = y
        self.count = count
        self.flagging = False
        self.first_play = False
        self.finished = False
        self.viewgrid = []
        self.first_ran = False
        self.lost = False
        self.won = False
        self.pos = [0, 0]
        for i in range(self.x * self.y):
            self.viewgrid.append(state.hidden)

        self.viewgrid = [self.viewgrid[i:i+self.x] for i in range(0,len(self.viewgrid),self.x)]
        for i in range(x * y):
            pregrid.append(False)

        for i in range(count):
            pregrid[i] = True

        random.shuffle(pregrid)

        self.bombgrid = [pregrid[i:i+x] for i in range(0,len(pregrid),x)]

        for num, i in enumerate(pregrid):
            if i == True:
                pregrid[num] = 9
            if i == False:
                pregrid[num] = 0
        self.numgrid = [pregrid[i:i+x] for i in range(0,len(pregrid),x)]



        #inside
        for row_num, row in enumerate(self.bombgrid):
            if row_num == 0 or row_num == len(self.bombgrid)-1:
                pass
            else:
                for col_num, col in enumerate(row):
                    if col_num == 0 or col_num == len(row)-1:
                        pass
                    elif col == True:
                        self.numgrid[row_num+1][col_num] += 1
                        self.numgrid[row_num-1][col_num] += 1
                        self.numgrid[row_num+1][col_num+1] += 1
                        self.numgrid[row_num+1][col_num-1] += 1
                        self.numgrid[row_num-1][col_num+1] += 1
                        self.numgrid[row_num-1][col_num-1] += 1
                        self.numgrid[row_num][col_num+1] += 1
                        self.numgrid[row_num][col_num-1] += 1

        #top row
        for col_num, col in enumerate(self.bombgrid[0]):
            if col_num == 0 or col_num == len(self.bombgrid[0])-1:
                pass
            elif col == True:
                self.numgrid[0][col_num+1] += 1
                self.numgrid[0][col_num-1] += 1
                self.numgrid[1][col_num+1] += 1
                self.numgrid[1][col_num-1] += 1
                self.numgrid[1][col_num] += 1

        #bottom row
        for col_num, col in enumerate(self.bombgrid[len(self.bombgrid)-1]):
            if col_num == 0 or col_num == len(self.bombgrid[len(self.bombgrid)-1])-1:
                pass
            elif col == True:
                self.numgrid[len(self.bombgrid)-1][col_num+1] += 1
                self.numgrid[len(self.bombgrid)-1][col_num-1] += 1
                self.numgrid[len(self.bombgrid)-2][col_num+1] += 1
                self.numgrid[len(self.bombgrid)-2][col_num] += 1
                self.numgrid[len(self.bombgrid)-2][col_num-1] += 1

        #left edge
        for row_num, row in enumerate(self.bombgrid):
            if row_num == 0 or row_num == len(self.bombgrid)-1:
                pass
            elif row[0] == True:
                self.numgrid[row_num-1][0] += 1
                self.numgrid[row_num-1][1] += 1
                self.numgrid[row_num][1] += 1
                self.numgrid[row_num+1][1] += 1
                self.numgrid[row_num+1][0] += 1

        #right edge
        for row_num, row in enumerate(self.bombgrid):
            if row_num == 0 or row_num == len(self.bombgrid)-1:
                pass
            elif row[len(row)-1] == True:
                self.numgrid[row_num-1][len(row)-1] += 1
                self.numgrid[row_num-1][len(row)-2] += 1
                self.numgrid[row_num][len(row)-2] += 1
                self.numgrid[row_num+1][len(row)-2] += 1
                self.numgrid[row_num+1][len(row)-1] += 1

        #top left
        if self.bombgrid[0][0] == True:
            self.numgrid[0][1] += 1
            self.numgrid[1][1] += 1
            self.numgrid[1][0] += 1

        #top right
        if self.bombgrid[0][len(self.bombgrid[0])-1] == True:
            self.numgrid[0][len(self.bombgrid[0])-2] += 1
            self.numgrid[1][len(self.bombgrid[0])-2] += 1
            self.numgrid[1][len(self.bombgrid[0])-1] += 1

        #bottom left
        if self.bombgrid[len(self.bombgrid)-1][0] == True:
            self.numgrid[len(self.bombgrid)-1][1] += 1
            self.numgrid[len(self.bombgrid)-2][1] += 1
            self.numgrid[len(self.bombgrid)-2][0] += 1

        #bottom right
        if self.bombgrid[len(self.bombgrid)-1][len(self.bombgrid[0])-1] == True:
            self.numgrid[len(self.bombgrid)-1][len(self.bombgrid[0])-2] += 1
            self.numgrid[len(self.bombgrid)-2][len(self.bombgrid[0])-2] += 1
            self.numgrid[len(self.bombgrid)-2][len(self.bombgrid[0])-1] += 1


    def create_board(self):
        os.system('cls')
        #for j_num, j in enumerate(self.viewgrid[0]):
            #print('   ' + chr(j_num + 65), end='  ')
        for i_num,i in enumerate(self.viewgrid):
            print('\n-', end='')
            for j in i:
                print('----',end='')
            print('\n', end='')
            #print(i_num + 1, end='')
            for j_num,j in enumerate(i):
                print('|', end='')
                if self.pos[0] == i_num and self.pos[1] == j_num:
                    print(Back.MAGENTA, end='')
                if j == state.hidden:
                    print('   ', end='')
                if j == state.revealed: 
                    print('', self.viewnums[i_num][j_num], '', end='')
                if j== state.flagged:
                    print(' F', '', end='')
                print(Back.RESET, end='')
            print('|', end='')
        print('\n-', end='')
        for i in self.viewgrid[0]:
            print('----', end='')
        print('\nArrow Keys to move. F to Flag. R to Reset. Space to Clear. M to go back to main menu.', end='\n')
        if self.lost:
            print('\nFat L. \nTo play again with the same settings, press r. To return to menu and change settings, press m.')
        if self.won:
            print('\nBIG W WOOOOO\nTo play again with the same settings, press r. To return to menu and change settings, press m.')
        print('\n', end='')

    def win_check(self):
        flag_count = 0
        for row in self.viewgrid:
            for col in row:
                if col == state.hidden:
                    return
                if col == state.flagged:
                    flag_count += 1
        if flag_count > self.count:
            return
        if flag_count == self.count:
            #print('you win')
            self.finished = True
            self.won = True

    def loss(self):
        for row_num, row in enumerate(self.bombgrid):
                for col_num, col in enumerate(row):
                    if col == True:
                        self.viewgrid[row_num][col_num] = state.revealed
        self.finished = True
        self.lost = True

    def reveal(self, y, x):
        self.viewgrid[y][x] = state.revealed
        if self.numgrid[y][x] > 0:
            return
        for y_offset in range(-1, 2):
            for x_offset in range(-1, 2):
                if x_offset == 0 and y_offset == 0:
                    continue
                if y+y_offset < 0 or y+y_offset >= len(self.numgrid) or x+x_offset < 0 or x+x_offset >= len(self.numgrid[0]):
                    continue
                if self.viewgrid[y+y_offset][x+x_offset] == state.hidden and not self.bombgrid[y+y_offset][x+x_offset]:
                    self.reveal(y+y_offset, x+x_offset)
        self.win_check()

    def toggle_mode(self):
        if self.flagging:
            self.flagging = False
        if not self.flagging:
            self.flagging = True
    
    def chord(self, y, x):
        if self.viewgrid[y][x] != state.revealed:
            return
        flag_num = 0
        for y_offset in range(-1, 2):
            for x_offset in range(-1, 2):
                if x_offset == 0 and y_offset == 0:
                    continue
                if y+y_offset < 0 or y+y_offset >= len(self.numgrid) or x+x_offset < 0 or x+x_offset >= len(self.numgrid[0]):
                    continue
                if self.viewgrid[y+y_offset][x+x_offset] == state.flagged:
                    flag_num += 1
        if flag_num >= self.numgrid[y][x]:
            for y_offset in range(-1, 2):
                for x_offset in range(-1, 2):
                    if x_offset == 0 and y_offset == 0:
                        continue
                    if y+y_offset < 0 or y+y_offset >= len(self.numgrid) or x+x_offset < 0 or x+x_offset >= len(self.numgrid[0]):
                        continue
                    if self.viewgrid[y+y_offset][x+x_offset] == state.flagged:
                        continue
                    if self.bombgrid[y+y_offset][x+x_offset] == True:
                        print('loser chorded bad haha')
                        self.loss()
                    self.reveal(y+y_offset, x+x_offset)
            self.win_check()
            self.create_board()

    def chord_all(self):
        for row in range(len(self.numgrid)):
            for col in range(len(self.numgrid[row])):
                self.chord(row, col)

    def check(self, y, x):
        if self.first_play:
            if self.bombgrid[y][x] == True:
                self.loss()
            elif self.numgrid[y][x] < 9:
                self.reveal(y, x)
        self.create_board()

    def flag(self, y, x):
        print(self.viewgrid[y][x])
        if self.viewgrid[y][x] == state.hidden:
            self.viewgrid[y][x] = state.flagged
        elif self.viewgrid[y][x] == state.flagged: 
            self.viewgrid[y][x] = None
            self.viewgrid[y][x] = state.hidden
            print(self.viewgrid[y][x])
        self.win_check()
        self.create_board()

    def first(self, y, x):
        self.first_play = True
        found = False
        if self.bombgrid[y][x]:
            for row_index, row in enumerate(self.bombgrid):
                for col_index, col in enumerate(row):
                    if not col:
                        col = True
                        self.numgrid[row_index][col_index] += 9
                        for y_offset in range(-1, 2):
                            if not found:
                                for x_offset in range(-1, 2):
                                    if x_offset == 0 and y_offset == 0:
                                        continue
                                    elif row_index+y_offset < 0 or row_index+y_offset >= len(self.numgrid) or col_index+x_offset < 0 or col_index+x_offset >= len(self.numgrid[0]):
                                        continue
                                    else:
                                        self.numgrid[row_index+y_offset][col_index+x_offset] += 1
                                        self.numgrid[y+y_offset][x+x_offset] -= 1
                                        self.bombgrid[row_index][col_index] = True
                                        found = True
                                        break
                        break
                    else:
                        continue
            self.bombgrid[y][x] = False
            self.numgrid[y][x] -= 9
            for y_offset in range(-1, 2):
                for x_offset in range(-1, 2):
                    if x_offset == 0 and y_offset == 0:
                        continue
                    if row_index+y_offset < 0 or row_index+y_offset >= len(self.numgrid) or col_index+x_offset < 0 or col_index+x_offset >= len(self.numgrid[0]):
                        continue
                    self.numgrid[y + y_offset][x+x_offset] -= 1
            self.first_ran = True
            pprint.pprint(self.numgrid)



        for y_offset in range(-1, 2):
            for x_offset in range(-1, 2):
                if x_offset == 0 and y_offset == 0:
                    continue
                if y + y_offset < 0 or x + x_offset < 0 or y + y_offset >= len(self.numgrid) or x + x_offset >= len(self.numgrid[0]):
                    continue
                found = False
                if self.bombgrid[y+y_offset][x+x_offset]:
                    for row_index, row in enumerate(self.bombgrid):
                        for col_index, col in enumerate(row):
                            if col:
                                continue
                            col = True
                            self.numgrid[row_index][col_index] += 9
                            for row_offset in range(-1,2):
                                for col_offset in range(-1,2):
                                    if row_offset == 0 and col_offset == 0:
                                        continue
                                    if row_index + row_offset < 0 or col_index + col_offset < 0 or row_index + row_offset >= len(self.numgrid) or col_index + col_offset >=len(row):
                                        continue
                                    self.numgrid[row_index + row_offset][col_index + col_offset] += 1
                            found = True
                            break
                        if found:
                            break

        for y_offset in range(-1, 2):
            for x_offset in range(-1, 2):
                if self.bombgrid[y+y_offset][x+x_offset]:
                    self.numgrid[y+y_offset][x+x_offset] -= 9
                    self.bombgrid[y+y_offset][x+x_offset] = False
                    for y_offset2 in range(-1, 2):
                        for x_offset2 in range(-1, 2):
                            if y_offset2 == 0 and x_offset2 == 0:
                                continue
                            if y+y_offset+y_offset2 < 0 or y+y_offset+y_offset2 >= len(self.numgrid) or x+x_offset+x_offset2 < 0 or x+x_offset+x_offset2 >= len(self.numgrid[0]):
                                continue
                            self.numgrid[y+y_offset+y_offset2][x+x_offset+x_offset2] -= 1
                            

            
        """for y_offset in range(-1, 2):
            for x_offset in range(-1, 2):
                if x_offset == 0 and y_offset == 0:
                    continue
                if y+y_offset < 0 or y+y_offset >= len(self.numgrid) or x+x_offset < 0 or x+x_offset >= len(self.numgrid[0]):
                    continue
                if self.bombgrid[y+y_offset][x+x_offset]:
                    for row_index, row in enumerate(self.bombgrid):
                        for col_index, col in enumerate(row):
                            found = False
                            if not col:
                                col = True
                                self.numgrid[row_index][col_index] += 9
                                for y_offset2 in range(-1, 2):
                                    if not found:
                                        for x_offset2 in range(-1, 2):
                                            if x_offset2 == 0 and y_offset2 == 0:
                                                continue
                                            elif y+y_offset+y_offset2 < 0 or y+y_offset+y_offset2 >= len(self.numgrid) or x+x_offset+x_offset2 < 0 or x+x_offset+x_offset2 >= len(self.numgrid[0]):
                                                continue
                                            else:
                                                self.numgrid[row_index+y_offset2][col_index+x_offset2] += 1
                                                #self.numgrid[y+y_offset+y_offset2][x+x_offset+x_offset2] -= 1
                                                self.bombgrid[row_index][col_index] = True
                                                found = True
                                                break
                                break
                
        for y_offset in range(-1, 2):
            for x_offset in range(-1, 2):
                if x_offset == 0 and y_offset == 0:
                    continue
                if y+y_offset < 0 or y+y_offset >= len(self.numgrid) or x+x_offset < 0 or x+x_offset >= len(self.numgrid[0]):
                    continue
                if self.bombgrid[y+y_offset][x_offset]:

                    for y_offset2 in range(-1, 2):
                        for x_offset2 in range(-1, 2):
                            if x_offset2 == 0 and y_offset2 == 0:
                                continue
                            if y+y_offset+y_offset2 < 0 or y+y_offset+y_offset2 >= len(self.numgrid) or x+x_offset+x_offset2 < 0 or x+x_offset+x_offset2 >= len(self.numgrid[0]):
                                continue
                            self.numgrid[y+y_offset+y_offset2][x+x_offset+x_offset2] -= 1


        for y_offset in range(-1, 2):
            for x_offset in range(-1, 2):       
                self.bombgrid[y+y_offset][x+x_offset] = False
                
            """
        
        self.make_view()

    def make_view(self):
        self.viewnums = []
        for i in self.numgrid:
            for j in i:
                if j == 0:
                    self.viewnums.append('-')
                elif j == 1:
                    self.viewnums.append(f'{Fore.LIGHTBLUE_EX}{str(j)}{Fore.RESET}')
                elif j == 2:
                    self.viewnums.append(f'{Fore.LIGHTGREEN_EX}{str(j)}{Fore.RESET}')
                elif j == 3:
                    self.viewnums.append(f'{Fore.LIGHTRED_EX}{str(j)}{Fore.RESET}')
                elif j == 4:
                    self.viewnums.append(f'{Fore.BLUE}{str(j)}{Fore.RESET}')
                elif j == 5:
                    self.viewnums.append(f'{Fore.RED}{str(j)}{Fore.RESET}')
                elif j == 6:
                    self.viewnums.append(f'{Fore.CYAN}{str(j)}{Fore.RESET}')
                elif j == 7:
                    self.viewnums.append(f'{Fore.BLACK}{str(j)}{Fore.RESET}')
                elif j == 8:
                    self.viewnums.append(f'{Fore.LIGHTBLACK_EX}{str(j)}{Fore.RESET}')
                elif j > 8:
                    self.viewnums.append('X')
                else:
                    self.viewnums.append('AAAHH IT BROKEY')

        self.viewnums = [self.viewnums[i:i+self.x] for i in range(0,len(self.viewnums),self.x)]
                      

    def what_do(self, y, x):
        if self.viewgrid[y][x] == state.flagged:
            if self.flagging:
                self.flag(y,x)
            else: return
        elif self.viewgrid[y][x] == state.revealed:
            self.chord(y,x)
        elif self.viewgrid[y][x] == state.hidden:
            if not self.first_play:
                self.first(y, x)
                self.make_view()
            if not self.flagging:
                self.check(y,x)
            elif self.flagging:
                self.flag(y,x)

    def move(self, dir):
        if not self.finished:
            if dir == 'u':
                self.pos[0] -= 1
                if self.pos[0] < 0:
                    self.pos[0] = len(self.viewgrid) - 1
            if dir == 'd':
                self.pos[0] += 1
                if self.pos[0] == len(self.viewgrid):
                    self.pos[0] = 0
            if dir == 'l':
                self.pos[1] -= 1
                if self.pos[1] < 0:
                    self.pos[1] = len(self.viewgrid[0]) - 1
            if dir == 'r':
                self.pos[1] += 1
                if self.pos[1] == len(self.viewgrid[0]):
                    self.pos[1] = 0
            self.create_board()



