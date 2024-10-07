import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def printAt(y, x, str):
    print(f'\x1b[{y};{x}H{str}')

def gotoLn(y):
    print(f'\x1b[{y};0H')

cls()

str = "Hello, World!"
printAt(1, 40, str)
gotoLn(30)
