
from Globals import *
from Command_IO import *

import pyttsx3

# ===========================================================================
# Command sequences

seq_0 = [ "R", "ping 34\n" ]             # seq 0
 
seq_1 = [ "R", "ping 41\n" ,             # seq 1
          "R", "servo 9 0 4 +30\n" ]  

seq_2 = [ "R", "ping 51\n" ,             # seq 2
          "L", "say", "Hello jim"]

seq_list = [seq_0, seq_1, seq_2]

# ===========================================================================

class sequence:
    def __init__(self):
        self.Command_IO = Command_IO()
        self.engine = pyttsx3.init()
        self.nos_sequences = len(seq_list)

    def play_sequence(self, seq_index) -> ErrorCode:
        if ((seq_index) < 0 or (seq_index > self.nos_sequences)):
            return ErrorCode.BAD_SEQUENCE_NUMBER
        self.nos_commands = len(seq_list[seq_index])
        status = ErrorCode.OK
        for i in range(self.nos_commands):
            if (seq_list[seq_index][0] == "R"):
                status = self.Command_IO.do_command(seq_list[seq_index][1])
                if (status != ErrorCode.OK):
                    return status
            else:
                match (seq_list[seq_index][1]):
                    case "say":
                        self.engine.say("I will speak this text")
                        self.engine.runAndWait()
                    case _:
                        return ErrorCode.BAD_LOCAL_COMMAND
        return ErrorCode.OK