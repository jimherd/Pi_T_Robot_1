# This Python file uses the following encoding: utf-8

import serial

from enum import Enum, IntEnum
from Globals import *

class Command_IO:
    def __init__(self):
     #   super(Command_IO, self).__init__
    #    self.parent = parent
        self.ser = serial.Serial()

        self.reply_string = ""
        self.IO_status = ErrorCode.OK
        self.argc = 0

        self.int_parameters   = [0]   * MAX_COMMAND_PARAMETERS
        self.float_parameters = [0.0] * MAX_COMMAND_PARAMETERS
        self.parameter_type  = [0]    * MAX_COMMAND_PARAMETERS

    def open_port(self, port, baud_rate):
        self.ser.baudrate = baud_rate
        self.ser.timeout = READ_TIMEOUT
        self.ser.port = port
        self.ser.timeout = 5
        try:
            self.ser.open()
        except serial.SerialException:
            return ErrorCode.BAD_COMPORT_OPEN
        self.ser.reset_input_buffer()
        self.ser.timeout = 5
        return ErrorCode.OK

    def close_port(self):
        self.ser.close()
        return ErrorCode.OK

    def send_command(self, send_string):
        if(self.ser.is_open == False):
            return ErrorCode.BAD_COMPORT_WRITE
        self.ser.write(str.encode(send_string)) # convert to bytes
        return ErrorCode.OK

    def get_reply(self) -> ErrorCode:
        self.reply_string = self.ser.read_until(b'\n', 50)
        if (len(self.reply_string) == 0):
            return ErrorCode.BAD_COMPORT_READ
        else:
            print("Reply = ", self.reply_string)
            return ErrorCode.OK
        
# execute a single command
    def do_command(self, cmd_string):
        IO_status = self.send_command(cmd_string)
        if DEBUG: print("send_command status = ", IO_status)
        if(IO_status != ErrorCode.OK):
            return  IO_status
        IO_status = self.get_reply()
        if(IO_status != ErrorCode.OK):
            return IO_status
        IO_status = self.Parse_string(self.reply_string)
        if(IO_status != ErrorCode.OK):
            return IO_status
        else:
            return ErrorCode.OK
        
# break string into component parts and convert to ints/floats
    def Parse_string(self, string_data):
        for index in range(MAX_COMMAND_PARAMETERS):
            self.int_parameters[index] = 0
            self.float_parameters[index] = 0.0
            self.parameter_type[index] = Modes.MODE_U

        self.string_parameters = string_data.split()
        self.argc = len(self.string_parameters)

        for index in range(self.argc):
            if self.string_parameters[index].isdigit():
                self.int_parameters[index] = int(self.string_parameters[index])
                self.parameter_type[index] = Modes.MODE_I
            else:
                try:
                    self.float_parameters[index] = float(self.string_parameters[index])
                    self.parameter_type[index] = Modes.MODE_R
                except ValueError:
                    self.parameter_type[index] = Modes.MODE_S

        return ErrorCode.OK
    
    def get_reply_value(self, parameter_index):
        return self.int_parameters[parameter_index]
    

