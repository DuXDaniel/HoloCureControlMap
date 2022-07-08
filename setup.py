from cx_Freeze import setup, Executable

base = None    

executables = [Executable("controller_script.py", base="Win32GUI")]

packages = ["inputs","threading","time","sys","json","math","pyautogui","PyQt5.QtCore", "PyQt5.QtWidgets"]
options = {
    'build_exe': {    
        'packages':packages,
        "excludes": ["tkinter","asyncio","colorama","concurrent","curses","dateutil","distutils","email","fontTools","html","http","kiwisolver","matplotlib","numba","numpy","pandas","scipy","xml"]
    },    
}

setup(
    name = "HoloCureControlMap",
    options = options,
    version = "1.0",
    description = 'If it works, it works.',
    executables = executables
)