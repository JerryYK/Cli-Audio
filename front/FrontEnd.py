import curses
import curses.textpad
import sys, os
from exceptions import File_Exception, WindowSize_Exception

'''
 Enhance the cli-audio's feature
 Author: Runquan Ye, Alec Allain
'''

class FrontEnd:



    def __init__(self, player):
	#use the try except case for handling the window size error
        try:
            self.player = player
	    
	    #create a veriable to hold the list
            self.songList = os.listdir('library')

            #remove the py file from the song list
            if os.path.isfile("library/__init__.py"):
                self.songList.remove('__init__.py')

            #self.player.play(sys.argv[1])
            curses.wrapper(self.menu)

	#get the window size exception then print out the warnning massage 
        except WindowSize_Exception:
            print("--------------------------------Warnning!!!--------------------------------",
                  "\n\tThe terminal size is too small to fit the Cli-Audio!"
                  "\n\tThe suggest size is: H >= 20; W >= 95")



    def menu(self, args):
        self.stdscr = curses.initscr()

	#get the window size
        h , w = self.stdscr.getmaxyx()

	#if the height and width are too small, raise the windowsize exception
        if(h < 20 or w < 95):
            raise WindowSize_Exception

        self.stdscr.border()
        self.stdscr.addstr(0,0, "cli-audio",curses.A_REVERSE)
        self.stdscr.addstr(5,10, "c - Change current song")
        self.stdscr.addstr(6,10, "p - Play/Pause")
        self.stdscr.addstr(7,10, "l - Library")
        self.stdscr.addstr(9,10, "ESC - Quit")
        self.updateSong()
        self.stdscr.refresh()
        while True:
            c = self.stdscr.getch()
            if c == 27:
                self.quit()
            elif c == ord('p'):
                #use the try except case to handle the play pause error
                try:
                    self.player.pause()

                #get the file exception then print out the warnning massage 
                except AttributeError:

		    #I create a new window to display the warnning message
                    warnningWindow = curses.newwin(5, 40, 5, 50)                    
                    warnningWindow.border()
                    warnningWindow.addstr(0,3, "Error")
                    warnningWindow.addstr(1,15, "Warnning!!")
                    warnningWindow.addstr(2,0, "There has no audio file is playing.")
                    warnningWindow.addstr(3,0, "The play / pause does not work.")
                    warnningWindow.addstr(4,0, "Press 'x' key to close warnning window!")
                    warnningWindow.refresh()

		    #set the key listener
                    d1 = self.stdscr.getch()

		    #press the "x" key to close the warnning window
                    if d1 == ord('x'):
                        del warnningWindow
                        self.stdscr.touchwin()
                        self.stdscr.refresh()

            elif c == ord('c'):
		#use the try except case the handle the file exception
                try:
                    self.changeSong()
                    self.updateSong()
                    self.stdscr.touchwin()
                    self.stdscr.refresh()

		#get the file exception then print out the warnning massage 
                except File_Exception:

		    #I create a new window to display the warnning message
                    warnningWindow = curses.newwin(5, 40, 5, 50)                    
                    warnningWindow.border()
                    warnningWindow.addstr(0,3, "Error")
                    warnningWindow.addstr(1,15, "Warnning!!")
                    warnningWindow.addstr(2,0, "The audio file does not exist in the file directory.")
                    warnningWindow.addstr(3,0, "Press 'x' key to close warnning window!")
                    warnningWindow.refresh()

		    #set the key listener
                    d = self.stdscr.getch()

		    #press the "x" key to close the warnning window
                    if d == ord('x'):
                        del warnningWindow
                        self.stdscr.touchwin()
                        self.stdscr.refresh()

            elif c == ord('l'):
               
		#create a list window to display the library list
                listWindow = curses.newwin(23, 55, 3, 42)                    
                listWindow.border()
                listWindow.addstr(0,3, "List")
                listWindow.addstr(1,18, "Song List")
                listWindow.addstr(2,1, "Here are the song in the 'library' forder: ")
                listWindow.addstr(3,1, "The maximum display length is: 15 songs")
                listWindow.addstr(4,1, "*Add: drop file into the 'library' forder and restar")
                listWindow.addstr(5,1, "*Remove: press the 'r' key.")
                listWindow.addstr(6,1, "*Exist: press the 'x' key.  Then the music plays")
                listWindow.addstr(7,1, "-----------------------------------------------------")
                
		#declare a variable to keep track on the song row place into the list window
                x = 0
                for song in self.songList:
                    if(x < 15):
                        #add the song file into the songlist window
                        listWindow.addstr(8+x ,1,song)
                        x = x + 1
                listWindow.refresh()
 
                while True:
                    #renew the key listener
                    d3 = listWindow.getch()
		    #press the "r" key to for removing the file
                    if d3 == ord('r'):
		        # create a window to ask the remove input
                        removeWindow = curses.newwin(5, 40, 5, 50)                    
                        removeWindow.border()
                        removeWindow.addstr(0,3, "Remove")
                        removeWindow.addstr(1,0, "Whoch Song name you want to remove?")
                        removeWindow.refresh()

                        curses.echo()
                        removeFile = removeWindow.getstr(2,1, 30)
                        curses.noecho()

		        #close the remove window
                        del removeWindow
                        listWindow.touchwin()
                        listWindow.refresh()

		        # remove the song from the list 
                        if removeFile.decode(encoding="utf-8") in self.songList:
                            self.songList.remove(removeFile.decode(encoding="utf-8"))

		        #remove the song file from the directory
                        if os.path.isfile("library/" + removeFile.decode(encoding="utf-8")):     
                            os.remove("library/" + removeFile.decode(encoding="utf-8"))
                    
                        for r in range(x+1):
                            if(x < 15):
                                #add the song file into the songlist window
                                listWindow.addstr(8+r, 1, "                        ")
                        x = 0
                        for song in self.songList:
                            if(x < 15):
                                #add the song file into the songlist window
                                listWindow.addstr(8+x ,1,song)
                                x = x + 1
                	#update the window
                        listWindow.refresh()

                    #get out of the while loop
                    if d3 == ord('x'):
                        d4 = listWindow.getch()
                        break

                #press the "x" key to close the warnning window
                if d4 == ord('x'):
                    del listWindow
                    for song in self.songList:
                       if self.player.paused is False:
                           self.player.stop()
                       self.player.play("library/" + song) 
                       self.updateSong()
                    
                    self.stdscr.touchwin()
                    self.stdscr.refresh()
    


    def updateSong(self):
        self.stdscr.addstr(15,10, "                                        ")
        self.stdscr.addstr(15,10, "Now playing: " + self.player.getCurrentSong())



    def changeSong(self):
        changeWindow = curses.newwin(5, 40, 5, 50)
        changeWindow.border()
        changeWindow.addstr(0,0, "What is the file path?", curses.A_REVERSE)
        self.stdscr.refresh()
        curses.echo()
        path = changeWindow.getstr(1,1, 30)
        curses.noecho()

        #check the input file is it on the exist, then do the following commands
        if (os.path.isfile(path.decode(encoding="utf-8"))):
            del changeWindow
            self.stdscr.touchwin()
            self.stdscr.refresh()
            if self.player.paused is False:
                self.player.stop()
            self.player.play(path.decode(encoding="utf-8"))

	#if the file path does not exist raise the file exception
        else:
            del changeWindow
            self.stdscr.touchwin()
            self.stdscr.refresh()
            raise File_Exception
        


    def quit(self):
        self.player.stop()
        exit()
