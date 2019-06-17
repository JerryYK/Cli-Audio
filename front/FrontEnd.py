import curses
import curses.textpad
import sys
import os

'''
 Enhance the cli-audio's feature
 Author: Runquan Ye Alec Allain
'''

from exception.CLI_Audio_Exception import *

class FrontEnd:

    def __init__(self, player):
        self.player = player
      	#self.player.play(sys.argv[1])
        curses.wrapper(self.menu)
        self.playList = []
        """ This checks for a window size error"""
        try:
            self.player = player
            self.player.play(sys.argv[1])
            curses.wrapper(self.menu)
        except CLI_Audio_Screen_Size_Exception:
            print("Window size is at a really small size")
            print()
            pass


    def menu(self, args):
        #getiing the height and width from the window itself
        h, w = self.scr.getmaxyx()
        
        #check the h and w are they big enough
        if(h < 30 or w < 30):
            #throw the customer exception
            raise exceptions.Size_exception

        self.stdscr = curses.initscr()
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
                self.player.pause()
            elif c == ord('c'):
                self.changeSong()
                self.updateSong()
                self.stdscr.touchwin()
                self.stdscr.refresh()
            elif c == ord('l'):
                self.createSongList()

    def createSongList(self):
        listWindow = curses.newwin(5, 40, 5, 50)
        listWindow.border()
        listWindow.addstr(0, 0, "Create your favorite song list:")

        listWindow.addstr(1, 10, "a - Add")
        listWindow.addstr(2, 10, "r - Remove")
        listWindow.addstr(3, 10, "q - Quit")
        listWindow.addstr(4, 0, "-----------------------------------------------------------")
        listWindow.addstr(5, 0, "Your currennt playlist:")
        if self.playList is not None:
            for i in self.playList:                
                 listWindow.addstr(self.playList.index(i) + 7, 10, i)
        
        while True:
            c = self.stdscr.getch()
            if c == ord('a'):
                popWindow = curses.curses.newwin(8,40, 5, 50)
                popWindow.border()
                popWindow.addstr(0, 0, "What is the file path you want to add into the list?")    
            #if c == ord('r'):

            if c == ord('q'):
               curses.noecho()
               del changeWindow
               break;

        for i in self.playerList:      
            self.changeSong()
            self.updateSong()
            self.stdscr.touchwin()
            self.stdscr.refresh()

         
        self.stdscr.refresh()
        curses.echo()
        path = changeWindow.getstr(1,1, 30)
        curses.noecho()
        del changeWindow
        self.stdscr.touchwin()
        self.stdscr.refresh()
        self.player.stop()
        self.player.play(path.decode(encoding="utf-8"))


    def updateSong(self):
        self.stdscr.addstr(15,10, "                                        ")
        self.stdscr.addstr(15,10, "Now playing: " + self.player.getCurrentSong())

    def changeSong(self):
        """Method checks for executable path for music file"""
        try:
            changeWindow = curses.newwin(5, 40, 5, 50)
            changeWindow.border()
            changeWindow.addstr(0,0, "What is the file path?", curses.A_REVERSE)
        except CLI_Audio_File_Exception:
            print("There was no file path that linked up correctly")
            pass
        
        self.stdscr.refresh()
        curses.echo()
        path = changeWindow.getstr(1,1, 30)
        curses.noecho()
        del changeWindow
        self.stdscr.touchwin()
        self.stdscr.refresh()
        self.player.stop()
        self.player.play(path.decode(encoding="utf-8"))
        

    def quit(self):
        self.player.stop()
        exit()
