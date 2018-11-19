import sys
import os

'''
This class handles the exceptions of the 
cli-audio file running into errors

@author Alec Allain
@author Jerry Ye
'''
class CLI_Audio_Exception(Exception):
    """ This is a custom made exception that extends off Python's Exception class """
    pass

class CLI_Audio_Screen_Size_Exception(CLI_Audio_Exception):
    """ This maintains any errors caused by a screen size error """
    pass

class CLI_Audio_File_Exception(CLI_Audio_Exception):
    """ This maintains any errors caused by a audio file error """
    pass
