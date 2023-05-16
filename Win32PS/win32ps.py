import winreg
from colorama import init, Fore, Back, Style
init()

def get_win32_priority_separation():
    path = r"SYSTEM\CurrentControlSet\Control\PriorityControl"
    name = "Win32PrioritySeparation"

    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path) as key:
            priority_separation, _ = winreg.QueryValueEx(key, name)
            return priority_separation
    except WindowsError:
        return None

def calculate_quantum(decimal, consumer_checked):
    clipped_binary = bin(decimal)[2:].zfill(32)[26:]
    fore_ground = 6
    back_ground = 6

    first_two = clipped_binary[:2]
    second_two = clipped_binary[2:4]
    third_two = clipped_binary[4:]

    if first_two == '01' or (not consumer_checked and (first_two == '00' or first_two == '11')):
        if back_ground < 36:
            fore_ground = back_ground = 12
        else:
            fore_ground = back_ground = 36

    if second_two == '10' or (not consumer_checked and (second_two == '00' or second_two == '11')):
        fore_ground = back_ground = fore_ground * 3
    elif third_two == '01':
        fore_ground *= 2
    elif third_two == '10' or third_two == '11':
        fore_ground *= 3

    fg_type, bg_type = get_fg_and_bg_types(fore_ground, back_ground)

    fg_interval = f'"Interval" es: {fore_ground}'
    bg_length = f'"Length" es: {back_ground} ({bg_type})'

    if fg_type == "Short":
        if back_ground >= 18:
            bg_type = "Fixed"
            if back_ground == 18:
                bg_length = f'"Length" es: {back_ground} ({bg_type})'
        else:
            bg_type = "Variable"
            bg_length = f'"Length" es: {back_ground} ({bg_type})'
    elif fg_type == "Long":
        if back_ground >= 36:
            bg_type = "Fixed"
            if back_ground == 36:
                bg_length = f'"Length" es: {back_ground} ({bg_type})'
        elif back_ground in [12, 24]:
            bg_type = "Variable"
            bg_length = f'"Length" es: {back_ground} ({bg_type})'
        elif back_ground == 18:
            bg_type = "Fixed"
            bg_length = f'"Length" es: {back_ground} ({bg_type})'

    return f'FG {fg_interval} ({fg_type})\n\nBG {bg_length}'

def get_fg_and_bg_types(fore_ground, back_ground):
    if fore_ground >= 36:
        fg_type = "Long"
    elif fore_ground == 12 or fore_ground == 24:
        fg_type = "Long"
    else:
        fg_type = "Short"

    if back_ground >= 36:
        bg_type = "Fixed"
    elif back_ground == 18:
        bg_type = "Fixed"
    else:
        bg_type = "Variable"

    return fg_type, bg_type

if __name__ == '__main__':
    priority_separation_decimal = get_win32_priority_separation()
if priority_separation_decimal is None:
    print(Fore.RED + "No se pudo obtener el valor de 'Win32PrioritySeparation'" + Style.RESET_ALL)
else:
    priority_separation_hex = hex(priority_separation_decimal)[2:]
    quantum = calculate_quantum(priority_separation_decimal, True)
    print(Fore.LIGHTYELLOW_EX + f'\nWin32PrioritySeparation Hexadecimal:{Style.RESET_ALL} {priority_separation_hex}')
    print(Fore.LIGHTYELLOW_EX + f'\nWin32PrioritySeparation Decimal:{Style.RESET_ALL} {priority_separation_decimal}')
    print(Fore.LIGHTBLUE_EX + f'\n{quantum}' + Style.RESET_ALL)
    input(Fore.LIGHTGREEN_EX + '\nPresiona Enter para cerrar el programa...' + Style.RESET_ALL)