import curses
import time
import logging
import signal 
import sys

class CursesHandler(logging.Handler):
    def __init__(self, screen):
        logging.Handler.__init__(self)
        self.screen = screen
    def emit(self, record):
            msg = self.format(record)
            screen = self.screen
            screen.addstr(msg + "\n")
            screen.refresh()


def restoreConsole():
    curses.nocbreak(); stdscr.keypad(0); curses.echo()
    curses.endwin()

# Signal handler for Control+C
# will restore console
def signal_handler(sig, frame):
    restoreConsole()
    print('You pressed Ctrl+C!')
    sys.exit(0)

# Overrinding Ctrl+C
signal.signal(signal.SIGINT, signal_handler)


try:
	stdscr = curses.initscr()

	curses.noecho()

	curses.cbreak()

	stdscr.keypad(1)
	
	screen = curses.initscr()
	screen.nodelay(1)
	maxy, maxx = screen.getmaxyx()
	height=maxy-2
	width=maxx-2

	screen.border('|', '|', '-', '-', '+', '+', '+', '+')
	win = curses.newwin(height, 80, 1, 1)
	#win.border('|', '|', '-', '-', '+', '+', '+', '+')
	curses.setsyx(-1, -1)
	screen.addstr("Testing my curses app")
	screen.refresh()
	win.refresh()
	win.scrollok(True)

	logger = logging.getLogger('myLog')
	mh = CursesHandler(win)
	logger.addHandler(mh)

	for i in range(1,70):
		logger.error("Test" + str(i))
		#win.addstr("test " + str(i) + "\n")
		win.refresh()
		time.sleep(0.1)		

	time.sleep(2)

except RuntimeError as e:
	print("ERROR")
	print(e)

finally:
	restoreConsole()


