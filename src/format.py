from pathlib import Path
from colorama import Style, Fore, Back


def fmt_title(text: str) -> str:
    return Fore.CYAN + Style.BRIGHT + f"\n{text}" + Style.RESET_ALL


def fmt_filename(path: str | Path) -> str:
    return Fore.MAGENTA + f"f {path}" + Style.RESET_ALL


def fmt_dirname(path: str | Path) -> str:
    return Fore.BLUE + f"d {path}" + Style.RESET_ALL


def fmt_warn(msg: str) -> str:
    return Fore.YELLOW + msg + Style.RESET_ALL


def fmt_err(msg: str) -> str:
    return Fore.RED + msg + Style.RESET_ALL


def fmt_info(msg: str) -> str:
    return Fore.CYAN + msg + Style.RESET_ALL


def fmt_success(msg: str) -> str:
    return Fore.GREEN + msg + Style.RESET_ALL
