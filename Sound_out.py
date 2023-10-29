#
import os.path
import pyttsx3

from playsound import playsound

from Command_IO import  *
from Globals    import  *
from Sequences  import  *

class Sound_out:

    engine = pyttsx3.init()
    
    def play_sound_file(self, filename, block) -> ErrorCode:
        if (os.path.exists(filename) == False):
            print("sound file = ", filename)
            status = ErrorCode.BAD_SOUND_FILE
        else:
            playsound(filename, block)
            status = ErrorCode.OK
        print("Play_sound_file status = ", status)
        return status
    
    def speak_text(self, the_text, block):
        self.engine.say(the_text)
        self.engine.runAndWait()
