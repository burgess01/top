""" Program in order to create a 'top' command implemented in Python. """

# needed imports
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
        os = compile("mac.top()", "mac", "eval")
    elif operatingSys == "Windows":
        os = compile("windows.top()", "windows", "eval")
    elif operatingSys == "Linux":
        os = compile("linux.top()", "linux", "eval")

    try:
        if len(sys.argv) == 1:
            # if they want to run it iteratively
            while True:
                eval(os)
                time.sleep(0.90)
        else:
            iterations = int(sys.argv[1])
            # run for the amount of times entered
            for i in range(iterations):
                eval(os)
                time.sleep(1)

    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
