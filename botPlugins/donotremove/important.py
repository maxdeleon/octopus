import os

if __name__ == '__main__':
    
    if os.path.isfile('./images/Cat.png'):
        print('type=FILE')
        print('./images/Cat.png')
    else:
        print('type=TEXT')
        print('Someone has deleted cat.png :(')