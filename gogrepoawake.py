import gogrepo
import time
import sys
import os
 import ctypes
 
ES_CONTINUOUS        = 0x80000000
ES_AWAYMODE_REQUIRED = 0x00000040
ES_SYSTEM_REQUIRED   = 0x00000001
ES_DISPLAY_REQUIRED  = 0x00000002

if __name__ == "__main__":
    try:
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED)
        gogrepo.main(gogrepo.process_argv(sys.argv))
        gogrepo.info('exiting...')
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
    except KeyboardInterrupt:
        gogrepo.info('exiting...')
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
        sys.exit(1)
    except SystemExit:
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
        raise
    except:
        ctypes.windll.kernel32.SetThreadExecutionState(ES_CONTINUOUS)
        gogrepo.log_exception('fatal...')
        sys.exit(1)