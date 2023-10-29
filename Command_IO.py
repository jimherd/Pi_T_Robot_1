# This Python file uses the following encoding: utf-8

import serial

from enum    import Enum, IntEnum

from Globals import *

class Command_IO:

# data common to all instances of class
    ser_1 = serial.Serial()     
    reply_string = ""
    argc = 0
    int_parameters   = [0]   * MAX_COMMAND_PARAMETERS
    float_parameters = [0.0] * MAX_COMMAND_PARAMETERS
    parameter_type  = [0]    * MAX_COMMAND_PARAMETERS

# class functions
    def open_port(self, port, baud_rate):
        self.ser_1.baudrate = baud_rate
        self.ser_1.timeout = READ_TIMEOUT
        self.ser_1.port = port
        self.ser_1.timeout = 5
        try:
            self.ser_1.open()
        except serial.SerialException:
            return ErrorCode.BAD_COMPORT_OPEN
        self.ser_1.reset_input_buffer()
        self.ser_1.timeout = 5
        return ErrorCode.OK

    def close_port(self):
        self.ser_1.close()
        return ErrorCode.OK
    
    def set_port(self, port_name):
        self.ser_1.port = port_name
    
    def port_is_open(self) -> bool:
        return self.ser_1.is_open

    def send_command(self, send_string):
        if(self.ser_1.is_open == False):
            return ErrorCode.BAD_COMPORT_WRITE
        self.ser_1.write(str.encode(send_string)) # convert to bytes
        return ErrorCode.OK

    def get_reply(self) -> ErrorCode:
        self.reply_string = self.ser_1.read_until(b'\n', 50)
        if (len(self.reply_string) == 0):
            return ErrorCode.BAD_COMPORT_READ
        else:
            print("Reply = ", self.reply_string)
            return ErrorCode.OK
        
# execute a single command
    def do_command(self, cmd_string):
        if DEBUG: print("do_command string = ", cmd_string)
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
    

