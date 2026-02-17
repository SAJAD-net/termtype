import curses
import sys




def main(stdscr):
    
    
    stdscr.clear()
    stdscr.refresh()
    
    height, width = stdscr.getmaxyx()

    # Initializing the colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_CYAN, curses.COLOR_BLACK)


    statusbarstr = f"Press 'Esc' to exit | WPM : {0.0} | Pos: {width}, {height}"

    # Rendering status bar
    stdscr.attron(curses.color_pair(4))
    stdscr.addstr(height-1, 0, statusbarstr)
    stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
    stdscr.attroff(curses.color_pair(4))


    title = "TermType - WPM"

    # Turning on attributes for title
    stdscr.attron(curses.color_pair(4))
    stdscr.attron(curses.A_BOLD)

    # Rendering title
    twidth = int((width // 2) - (len(title) // 2) - len(title) % 2)
    stdscr.addstr(1, twidth, title)

    stdscr.refresh()
    stdscr.getkey()


curses.wrapper(main)
