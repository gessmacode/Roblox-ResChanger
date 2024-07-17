import os
import time
import win32api
import win32con
import wmi
import winsound
import sys
import ctypes
import locale
from ctypes import wintypes

class DEVMODE(ctypes.Structure):
    _fields_ = [
        ("dmDeviceName", wintypes.WCHAR * 32),
        ("dmSpecVersion", wintypes.WORD),
        ("dmDriverVersion", wintypes.WORD),
        ("dmSize", wintypes.WORD),
        ("dmDriverExtra", wintypes.WORD),
        ("dmFields", wintypes.DWORD),
        ("dmOrientation", wintypes.SHORT),
        ("dmPaperSize", wintypes.SHORT),
        ("dmPaperLength", wintypes.SHORT),
        ("dmPaperWidth", wintypes.SHORT),
        ("dmScale", wintypes.SHORT),
        ("dmCopies", wintypes.SHORT),
        ("dmDefaultSource", wintypes.SHORT),
        ("dmPrintQuality", wintypes.SHORT),
        ("dmColor", wintypes.SHORT),
        ("dmDuplex", wintypes.SHORT),
        ("dmYResolution", wintypes.SHORT),
        ("dmTTOption", wintypes.SHORT),
        ("dmCollate", wintypes.SHORT),
        ("dmFormName", wintypes.WCHAR * 32),
        ("dmLogPixels", wintypes.WORD),
        ("dmBitsPerPel", wintypes.DWORD),
        ("dmPelsWidth", wintypes.DWORD),
        ("dmPelsHeight", wintypes.DWORD),
        ("dmDisplayFlags", wintypes.DWORD),
        ("dmDisplayFrequency", wintypes.DWORD),
        ("dmICMMethod", wintypes.DWORD),
        ("dmICMIntent", wintypes.DWORD),
        ("dmMediaType", wintypes.DWORD),
        ("dmDitherType", wintypes.DWORD),
        ("dmReserved1", wintypes.DWORD),
        ("dmReserved2", wintypes.DWORD),
        ("dmPanningWidth", wintypes.DWORD),
        ("dmPanningHeight", wintypes.DWORD),
    ]

def get_system_language():
    windll = ctypes.windll.kernel32
    lang = locale.windows_locale[windll.GetUserDefaultUILanguage()]
    return "de" if lang.startswith("de") else "en"

def translate(message, language):
    translations = {
        "en": {
            "waiting": "[-] Waiting for Roblox",
            "res_injected": "[+] Resolution injected",
            "roblox_closed": "[-] Roblox closed, resolution reset to default",
            "script_interrupted": "[-] Script interrupted, resolution reset to default",
            "set_width": "Please enter the width of the resolution:",
            "set_height": "Please enter the height of the resolution:",
            "res_not_found": "[-] Resolution not found or not supported",
            "invalid_input": "[-] Invalid input. Please enter valid integers."
        },
        "de": {
            "waiting": "[-] Warten auf Roblox",
            "res_injected": "[+] Auflösung injiziert",
            "roblox_closed": "[-] Roblox geschlossen, Auflösung zurückgesetzt auf Standard",
            "script_interrupted": "[-] Skript unterbrochen, Auflösung zurückgesetzt auf Standard",
            "set_width": "Bitte geben Sie die Breite der Auflösung ein:",
            "set_height": "Bitte geben Sie die Höhe der Auflösung ein:",
            "res_not_found": "[-] Auflösung konnte nicht gefunden oder wird nicht unterstützt",
            "invalid_input": "[-] Ungültige Eingabe. Bitte geben Sie gültige Ganzzahlen ein."
        }
    }
    return translations[language][message]

def check_resolution(width, height):
    """Check if the given resolution is supported."""
    i = 0
    devmode = DEVMODE()
    devmode.dmSize = ctypes.sizeof(DEVMODE)
    while ctypes.windll.user32.EnumDisplaySettingsW(None, i, ctypes.byref(devmode)):
        if devmode.dmPelsWidth == width and devmode.dmPelsHeight == height:
            return True
        i += 1
    return False

def set_screen_resolution(width, height):
    dm = win32api.EnumDisplaySettings(None, 0)
    dm.PelsWidth = width
    dm.PelsHeight = height
    dm.Fields = win32con.DM_PELSWIDTH | win32con.DM_PELSHEIGHT
    win32api.ChangeDisplaySettings(dm, 0)

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    ctypes.windll.kernel32.SetConsoleTitleW("Roblox ResChanger")

    language = get_system_language()

    roblox_process_name = "RobloxPlayerBeta.exe"
    c = wmi.WMI()

    while True:
        try:
            roblox_width = int(input(f"{translate('set_width', language)} "))
            roblox_height = int(input(f"{translate('set_height', language)} "))
            if not check_resolution(roblox_width, roblox_height):
                print(f"\033[91m{translate('res_not_found', language)}\033[0m")
                time.sleep(1)
                clear_console()
                continue
            break  # Exit loop if successful
        except ValueError:
            print(f"\033[91m{translate('invalid_input', language)}\033[0m")

    clear_console()  # Clear console after resolution input

    winsound.Beep(500, 500)
    print(f"\033[93m{translate('waiting', language)}\033[0m")  # Show waiting message after clearing console

    default_width, default_height = 1920, 1080

    try:
        while True:
            roblox_process = [process for process in c.Win32_Process(name=roblox_process_name)]
            
            if roblox_process:
                set_screen_resolution(roblox_width, roblox_height)
                print(f"\033[93m{translate('res_injected', language)}\033[0m")
                winsound.Beep(500, 500)
                
                while roblox_process:
                    roblox_process = [process for process in c.Win32_Process(name=roblox_process_name)]
                    time.sleep(1)

                set_screen_resolution(default_width, default_height)
                print(f"\03393m{translate('roblox_closed', language)}\033[0m")
                winsound.Beep(500, 500)
                time.sleep(2)
                sys.exit()
            
            time.sleep(1)
    except KeyboardInterrupt:
        set_screen_resolution(default_width, default_height)
        print(f"\033[93m{translate('script_interrupted', language)}\033[0m")
        winsound.Beep(1000, 500)

if __name__ == "__main__":
    main()
    
    
# ████████╗██╗  ██╗ █████╗ ███╗   ██╗██╗  ██╗███████╗    ███████╗ ██████╗ ██████╗     ██╗   ██╗███████╗██╗███╗   ██╗ ██████╗ 
# ╚══██╔══╝██║  ██║██╔══██╗████╗  ██║██║ ██╔╝██╔════╝    ██╔════╝██╔═══██╗██╔══██╗    ██║   ██║██╔════╝██║████╗  ██║██╔════╝ 
#    ██║   ███████║███████║██╔██╗ ██║█████╔╝ ███████╗    █████╗  ██║   ██║██████╔╝    ██║   ██║███████╗██║██╔██╗ ██║██║  ███╗
#    ██║   ██╔══██║██╔══██║██║╚██╗██║██╔═██╗ ╚════██║    ██╔══╝  ██║   ██║██╔══██╗    ██║   ██║╚════██║██║██║╚██╗██║██║   ██║
#    ██║   ██║  ██║██║  ██║██║ ╚████║██║  ██╗███████║    ██║     ╚██████╔╝██║  ██║    ╚██████╔╝███████║██║██║ ╚████║╚██████╔╝
#    ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝    ╚═╝      ╚═════╝ ╚═╝  ╚═╝     ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ 
                                                                                                                            
