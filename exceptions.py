

'''
  define customize python exceptions
  Author: Runquan Ye, Alec Allain
'''

#customize exception class
class CLI_Audio_Exception(Exception):
    """Base class for cutomize Cli Audio exceptions"""
    pass

#an exception for the unavailable file path
class File_Exception(CLI_Audio_Exception):
    """The file path is not available!!!"""
    pass

#an exception for the unavailable window size
class WindowSize_Exception(CLI_Audio_Exception):
    """The screen is too small to fit the application!!!"""
    pass


