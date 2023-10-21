
from Globals    import *
from Command_IO import *
from Sound_out  import  *

import pyttsx3
import time

from playsound import playsound

# ===========================================================================
# Command sequences

seq_0 = [               # seq 0
    [ "L", "say", "Sequence 0"] ,
    [ "R", "ping 0 34\n" ] 
]
 
seq_1 = [              # seq 1
    [ "L", "say", "Sequence 1"] ,
    [ "R", "ping 0 41\n" ] ,
    [ "R", "servo 9 0 4 30\n" ] ,
    [ "R", "servo 9 7 8 0\n" ] ,
    [ "R", "servo 9 0 8 30\n" ] ,
    [ "L", "play", "C:/Media/Sound/Hello.mp3"] ,
    [ "L", "sleep", 5 ] ,
    [ "R", "servo 9 7 8 1\n" ] ,
]

seq_2 = [             # seq 2
    [ "L", "say", "Sequence 2"] ,
    [ "R", "ping 0 51\n" ] ,
    [ "L", "say", "Hello jim"]
]

seq_list = [seq_0, seq_1, seq_2]

# ===========================================================================

class sequence:
    def __init__(self):
        self.Command_IO = Command_IO()
        self.Sound_out = Sound_out()
 
        self.nos_sequences = len(seq_list)

    def play_sequence(self, seq_index) -> ErrorCode:
        if ((seq_index) < 0 or (seq_index > self.nos_sequences)):
            return ErrorCode.BAD_SEQUENCE_NUMBER
        self.nos_commands = len(seq_list[seq_index])
        status = ErrorCode.OK
        for i in range(self.nos_commands):
            print(seq_list[seq_index][i][0])
            print(seq_list[seq_index][i][1])
            if (seq_list[seq_index][i][0] == "R"):
                status = self.Command_IO.do_command(seq_list[seq_index][i][1])
                if (status != ErrorCode.OK):
                    return status
            else:
                match (seq_list[seq_index][i][1]):
                    case "say_wait":
                        self.Sound_out.speak_text(seq_list[seq_index][i][2], True)
                    case "say":
                        self.Sound_out.speak_text(seq_list[seq_index][i][2], True)
                    case "play":
                        self.Sound_out.play_sound_file(seq_list[seq_index][i][2], True)
                    case "sleep":
                        time.sleep(seq_list[seq_index][i][2])
                    case _:
                        return ErrorCode.BAD_LOCAL_COMMAND
        return ErrorCode.OK