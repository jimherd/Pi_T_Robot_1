#
import sys
import serial
import serial.tools.list_ports
import random
import pyttsx3


DEFAULT_PORT    =  9
SPEED_THRESHOLD = 21
NOS_SERVOS      =  8

OFF = 0
ON  = 1

from Command_IO import  *
from Globals    import  *
from Sequences  import  *

class Pi_the_robot:
    def __init__(self, parent=None):
        self.Command_IO = Command_IO()
        ports = list(serial.tools.list_ports.comports())
        if (len(ports) == 0):
            print("No serial ports on system")
            sys.exit()
        status = ErrorCode.BAD_COMPORT_OPEN
        for p in ports:
            the_port = str(p).split(" ")[0]
            if DEBUG: print(the_port)
            self.Command_IO.close_port()
            status = self.Command_IO.open_port(the_port, BAUDRATE)
            if DEBUG: print("Open port status = ", status)
            if (status == ErrorCode.OK):
                status = self.ping()
                if DEBUG: print("Ping status = ", status)
                if(status == ErrorCode.OK):
                    port = str(p)
                else:
                    self.Command_IO.close_port()
                    continue
            else:
                self.Command_IO.close_port()
                continue
        self.mouth_state = OFF
        self.Mouth_on_off(ON, OFF)

# End of initialisation code
# ===========================================================================
# System functions

    def exit_program(self):
        sys.exit()

    def open_serial_port(self, port, baudrate):
        status = self.Command_IO.open_port(port, baudrate)
        return status
     
    def close_serial_port(self):
        self.Command_IO.close_port()

# ===========================================================================
# ping code
    def ping(self):
        self.cmd_string = "ping 0 " + str(random.randint(1,98)) + "\n"
        status = ErrorCode.OK
        status = self.Command_IO.do_command(self.cmd_string)
        if DEBUG: print("First value = ", self.Command_IO.get_reply_value(2))
        if DEBUG: print("do_command status = ", status)
        return status
    
# ===========================================================================
# servo code
    def Execute_servo_cmd(self, joint, position, speed, group):
    # select type of move command
        if ((group == False) and (speed < SPEED_THRESHOLD)):
            servo_cmd = ServoCommands.ABS_MOVE
        elif ((group == True) and (speed < SPEED_THRESHOLD)):
            servo_cmd = ServoCommands.ABS_MOVE_SYNC
        elif ((group == False) and (speed >= SPEED_THRESHOLD)):
            servo_cmd = ServoCommands.SPEED_MOVE
        else:
            servo_cmd = ServoCommands.SPEED_MOVE_SYNC
        # construct appropriate command string
        if (speed < SPEED_THRESHOLD):
            self.cmd_string =(f"servo {DEFAULT_PORT} {servo_cmd} {joint} {position}\n")
        else:
            self.cmd_string =(f"servo {DEFAULT_PORT} {servo_cmd} {joint} {position} {speed}\n")
        # log command for debug
        if DEBUG: print(self.cmd_string)
    # execute servo move command
        status =  self.Command_IO.do_command(self.cmd_string)
        if DEBUG: print("do_command status = ", status)
        if DEBUG: print("reply string = ", self.Command_IO.reply_string)
        return status

# ===========================================================================
# mouth servo code
    def Mouth_on_off(self, on_off, group_code):
        if (group_code == OFF ):
            servo_cmd = ServoCommands.ABS_MOVE
        else:
            servo_cmd = ServoCommands.ABS_MOVE_SYNC
        if (on_off == ON):
            servo_angle = +45
        else:
            servo_angle = 0
        self.cmd_string = (f"servo {DEFAULT_PORT} {servo_cmd} joints.MOUTH {servo_angle}\n")
    # execute mouth move command
        status =  self.Command_IO.do_command(self.cmd_string)
        if DEBUG: print(self.cmd_string)
        if DEBUG: print("do_command status = ", status)
        if DEBUG: print("reply string = ", self.Command_IO.reply_string)
        self.mouth_state = on_off
        return status

# ===========================================================================

# ===========================================================================
# Main call
#
def main():
    app = Pi_the_robot()
    print("Hello")

if __name__ == "__main__":
    sys.exit(main())