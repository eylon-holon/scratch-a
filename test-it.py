import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def gotoLn(y):
    print(f'\x1b[{y};0H')


def printAt(y, x, str):
    print(f'\x1b[{y};{x}H{str}')

cls()

str = "Hello, World!"
printAt(1, 30, str)
gotoLn(10)
