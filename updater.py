import os
import time


def main():
    while True:
    out = os.popen('git status -uno')
    if 'On branch master' in out:
        if 'Your branch is up to date with \'origin/master\'.' in out:
            pass
        else:
            os.popen('git pull')
            print('WARNING Updating Repository')
    else:
        pass


if __name__ == '__main__':
    main()