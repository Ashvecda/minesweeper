from time import sleep
from threading import Thread
from win32gui import GetForegroundWindow
from grid import Grid
import pprint
import keyboard
import os

def menu():
    global x, y, count, grid, logger
    os.system('cls')
    difficulty = input("""Welcome to Minesweeper! Please type the difficulty you would like to play, or type "custom" to make your own:
    \nEasy: 9x9 Grid with 10 Mines\nMedium: 16x16 Grid with 40 Mines\nHard: 30x16 Grid with 99 Mines\n""")
    while True:
        os.system('cls')
        difficulty = difficulty.strip().lower()

        if difficulty == 'easy':
            x = 9
            y = 9
            count = 10
            break

        elif difficulty == 'medium':
            x = 16
            y = 16
            count = 40
            break

        elif difficulty == 'hard':
            x = 30
            y = 16
            count = 99
            break

        elif difficulty == 'custom':
            x = int(input('How wide do you want the grid?\n'))
            y = int(input('How tall would you like the grid?\n'))
            count = int(input('How many mines do you want in the grid?\n'))
            break

        else:
            difficulty = input("""Welcome to Minesweeper! Please type the difficulty you would like to play, or type "custom" to make your own:
        \nEasy: 9x9 Grid with 10 Mines\nMedium: 16x16 Grid with 40 Mines\nHard: 30x16 Grid with 99 Mines
        \nPlease enter a valid input.\n""")
            
    grid = Grid(x,y,count)
    
    grid.create_board()
    



class Keylogger():
    def __init__(self):
        self.current_window = GetForegroundWindow()
    def start_keys(self):
        keyboard.add_hotkey('right', self.move, args='r')
        keyboard.add_hotkey('left', self.move, args='l')
        keyboard.add_hotkey('up', self.move, args='u')
        keyboard.add_hotkey('down', self.move, args='d')
        keyboard.add_hotkey('space', self.space)
        keyboard.add_hotkey('f', self.flag)
        keyboard.add_hotkey('r', self.reset)
        keyboard.add_hotkey('m', menu)
        keyboard.add_hotkey('b', self.numgrid)
        #print('started')
        while True:
            if GetForegroundWindow() != self.current_window:
                self.stop_keys()
                break
            sleep(0.1)    

    def stop_keys(self):
        keyboard.unhook_all_hotkeys()
        #print('stopped')
        while True:
            if GetForegroundWindow() == self.current_window:
                self.start_keys()
                break
            sleep(0.1)
    
    def full_stop(self):
        keyboard.unhook_all_hotkeys()
    
    def move(self, dir):
        grid.move(dir)

    def reset(self):
        global grid
        grid = Grid(x,y,count)
        grid.create_board()

    def space(self):
        grid.what_do(grid.pos[0], grid.pos[1])  
        
    def flag(self): 
        grid.flag(grid.pos[0], grid.pos[1])

    def numgrid(self):
        pprint.pprint(grid.numgrid)
    

menu()
logger = Keylogger()
logger.start_keys()


   