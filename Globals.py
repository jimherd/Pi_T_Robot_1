# This Python file uses the following encoding: utf-8

# note :  ._name is the convention to indicate non-public attributes

import platform
from enum import Enum, IntEnum

class This_platform(IntEnum):
    UNKNOWN    = 0
    WINDOWS    = 1
    LINUX      = 2

# ===========================================================================
# Global system variables

DEBUG = True
port = ""
current_platform       = This_platform.UNKNOWN
current_platform_name  = "Unknown"

# ===========================================================================
# Global system constants

MAX_COMMAND_PARAMETERS    = 10
READ_TIMEOUT              = 4  # seconds
MAX_COMMAND_STRING_LENGTH = 100
MAX_REPLY_STRING_LENGTH   = 100
BAUDRATE                  = 115200

# ===========================================================================
# System ENUM constants

class Joints(IntEnum):
    LEFT_EYE_RIGHT_LEFT  = 0
    LEFT_EYE_UP_DOWN     = 1
    LEFT_EYE_LID         = 2
    LEFT_EYE_BROW        = 3
    RIGHT_EYE_RIGHT_LEFT = 4
    RIGHT_EYE_UP_DOWN    = 5
    RIGHT_EYE_LID        = 6
    RIGHT_EYE_BROW       = 7
    MOUTH                = 8

class ServoCommands(IntEnum):
    ABS_MOVE           = 0
    ABS_MOVE_SYNC      = 1
    SPEED_MOVE         = 2
    SPEED_MOVE_SYNC    = 3
    RUN_SYNC_MOVES     = 4
    STOP               = 5
    STOP_ALL           = 6

class StepperCommands(IntEnum):
    REL_MOVE           = 0
    ABS_MOVE           = 1
    REL_MOVE_SYNC      = 2
    ABS_MOVE_SYNC      = 3
    CALIBRATE          = 4

class ErrorCode(Enum):
    OK                              = 0
    LETTER_ERROR                    = -100    # rp2040 microcontroller errors
    DOT_ERROR                       = -101
    PLUSMINUS_ERROR                 = -102
    BAD_COMMAND                     = -103
    BAD_PORT_NUMBER                 = -104
    BAD_NOS_PARAMETERS              = -105
    BAD_BASE_PARAMETER              = -106
    PARAMETER_OUTWITH_LIMITS        = -107
    BAD_SERVO_COMMAND               = -108
    STEPPER_CALIBRATE_FAIL          = -109
    BAD_STEPPER_COMMAND             = -110
    BAD_STEP_VALUE                  = -111
    MOVE_ON_UNCALIBRATED_MOTOR      = -112
    EXISTING_FAULT_WITH_MOTOR       = -113
    SM_MOVE_TOO_SMALL               = -114
    LIMIT_SWITCH_ERROR              = -115
    UNKNOWN_STEPPER_MOTOR_STATE     = -116
    STEPPER_BUSY                    = -117
    SERVO_BUSY                      = -118

    BAD_COMPORT_OPEN                = -200     # PC errors
    UNKNOWN_COM_PORT                = -201
    BAD_COMPORT_READ                = -202
    BAD_COMPORT_WRITE               = -203
    NULL_EMPTY_STRING               = -204
    BAD_COMPORT_CLOSE               = -205
    BAD_PARSE                       = -206
    BAD_SEQUENCE_NUMBER             = -207
    BAD_LOCAL_COMMAND               = -208
    PING_FAIL                       = -209
    BAD_SOUND_FILE                  = -210

# modes for string parse routine
class Modes(IntEnum):
    MODE_U = 0
    MODE_I = 1
    MODE_R = 2
    MODE_S = 3

# ===========================================================================

class Platform_test():
    def __init__(self):
        self._current_platform = This_platform.UNKNOWN
        self._current_platform_name = ""

    def check_platform(self):
        self._current_platform_name = platform.system()
        if (self._current_platform_name == "Windows"):
            self._current_platform = This_platform.WINDOWS
        if (self._current_platform_name == "Linux"):
            self._current_platform = This_platform.LINUX

    def get_platform(self):
        return self._current_platform

    def get_platform_name(self):
        return self._current_platform_name
