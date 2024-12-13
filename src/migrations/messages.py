from colorama import Fore, Style, init


init(autoreset=True)


def print_error(message):
    print(f"{Fore.RED}[ERROR] {message}{Style.RESET_ALL}")


def print_success(message):
    print(f"{Fore.GREEN}[SUCCESS] {message}{Style.RESET_ALL}")


def print_info(message):
    print(f"{Fore.CYAN}[INFO] {message}{Style.RESET_ALL}")


def print_warning(message):
    print(f"{Fore.YELLOW}[WARNING] {message}{Style.RESET_ALL}")
