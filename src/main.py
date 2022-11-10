""" Program in order to create a 'top' command implemented in Python. """

# needed imports
import schedule
import time
import sys
import platform

# needed cross platform files
import mac
import windows
import linux


def main():

    operatingSys = platform.system()

    if operatingSys == "Darwin":
        if len(sys.argv) == 1:
            try:
                # if they want to run it iteratively
                schedule.every(1).seconds.do(mac.top)
                while True:
                    schedule.run_pending()
                    time.sleep(1)
            except KeyboardInterrupt:
                sys.exit(0)
        else:
            try:
                iterations = int(sys.argv[1])
                # run for the amount of times entered
                for i in range(iterations):
                    mac.top()
                    time.sleep(1)
            except:
                print(
                    "Please enter an integer value for the amount of times you want the program to run."
                )
    elif operatingSys == "Windows":
        if len(sys.argv) == 1:
            try:
                # if they want to run it iteratively
                schedule.every(1).seconds.do(windows.top)
                while True:
                    schedule.run_pending()
                    time.sleep(1)
            except KeyboardInterrupt:
                sys.exit(0)
        else:
            try:
                iterations = int(sys.argv[1])
                # run for the amount of times entered
                for i in range(iterations):
                    windows.top()
                    time.sleep(1)
            except:
                print(
                    "Please enter an integer value for the amount of times you want the program to run."
                )
    elif operatingSys == "Linux":
        if len(sys.argv) == 1:
            try:
                # if they want to run it iteratively
                schedule.every(1).seconds.do(linux.top)
                while True:
                    schedule.run_pending()
                    time.sleep(1)
            except KeyboardInterrupt:
                sys.exit(0)
        else:
            try:
                iterations = int(sys.argv[1])
                # run for the amount of times entered
                for i in range(iterations):
                    linux.top()
                    time.sleep(1)
            except:
                print(
                    "Please enter an integer value for the amount of times you want the program to run."
                )


if __name__ == "__main__":
    main()
