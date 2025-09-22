import sys
import random
import requests
import os
import subprocess
from colorama import init, Fore, Style
from datetime import datetime
from config import modules, proxies_list
from modules import scanning, osint, utilities, vuln_viewer, anonize

init(autoreset=True)

ascii_art = """
 ██▓███   █    ██   ▄████   █████▒▄████▄   ██ ▄█▀  ▄████  ▒█████   ██▒   █▓   
▓██░  ██▒ ██  ▓██▒ ██▒ ▀█▒▓██   ▒▒██▀ ▀█   ██▄█▒  ██▒ ▀█▒▒██▒  ██▒▓██░   █▒   
▓██░ ██▓▒▓██  ▒██░▒██░▄▄▄░▒████ ░▒▓█    ▄ ▓███▄░ ▒██░▄▄▄░▒██░  ██▒ ▓██  █▒░   
▒██▄█▓▒ ▒▓▓█  ░██░░▓█  ██▓░▓█▒  ░▒▓▓▄ ▄██▒▓██ █▄ ░▓█  ██▓▒██   ██░  ▒██ █░░   
▒██▒ ░  ░▒▒█████▓ ░▒▓███▀▒░▒█░   ▒ ▓███▀ ░▒██▒ █▄░▒▓███▀▒░ ████▓▒░   ▒▀█░     
▒▓▒░ ░  ░░▒▓▒ ▒ ▒  ░▒   ▒  ▒ ░   ░ ░▒ ▒  ░▒ ▒▒ ▓▒ ░▒   ▒ ░ ▒░▒░▒░    ░ ▐░     
░▒ ░     ░░▒░ ░ ░   ░   ░  ░       ░  ▒   ░ ░▒ ▒░  ░   ░   ░ ▒ ▒░    ░ ░░     
░░        ░░░ ░ ░ ░ ░   ░  ░ ░   ░        ░ ░░ ░ ░ ░   ░ ░ ░ ░ ▒       ░░     
            ░           ░        ░ ░      ░  ░         ░     ░ ░        ░     
                                 ░                                     ░      
 ██░ ██  ▄▄▄       ▄████▄   ██ ▄█▀▄▄▄█████▓ ▒█████   ▒█████   ██▓      ██████ 
▓██░ ██▒▒████▄    ▒██▀ ▀█   ██▄█▒ ▓  ██▒ ▓▒▒██▒  ██▒▒██▒  ██▒▓██▒    ▒██    ▒ 
▒██▀▀██░▒██  ▀█▄  ▒▓█    ▄ ▓███▄░ ▒ ▓██░ ▒░▒██░  ██▒▒██░  ██▒▒██░    ░ ▓██▄   
░▓█ ░██ ░██▄▄▄▄██ ▒▓▓▄ ▄██▒▓██ █▄ ░ ▓██▓ ░ ▒██   ██░▒██   ██░▒██░      ▒   ██▒
░▓█▒░██▓ ▓█   ▓██▒▒ ▓███▀ ░▒██▒ █▄  ▒██▒ ░ ░ ████▓▒░░ ████▓▒░░██████▒▒██████▒▒
 ▒ ░░▒░▒ ▒▒   ▓▒█░░ ░▒ ▒  ░▒ ▒▒ ▓▒  ▒ ░░   ░ ▒░▒░▒░ ░ ▒░▒░▒░ ░ ▒░▓  ░▒ ▒▓▒ ▒ ░
 ▒ ░▒░ ░  ▒   ▒▒ ░  ░  ▒   ░ ░▒ ▒░    ░      ░ ▒ ▒░   ░ ▒ ▒░ ░ ░ ▒  ░░ ░▒  ░ ░
 ░  ░░ ░  ░   ▒   ░        ░ ░░ ░   ░      ░ ░ ░ ▒  ░ ░ ░ ▒    ░ ░   ░  ░  ░  
 ░  ░  ░      ░  ░░ ░      ░  ░                ░ ░      ░ ░      ░  ░      ░  
                  ░                                                           
"""

def get_current_ip():
    try:
        response = requests.get("https://ipinfo.io/ip", timeout=5)
        return response.text.strip()
    except:
        return "Erro ao obter IP."

def show_menu():
    print(Fore.GREEN + ascii_art)
    print(Fore.CYAN + "=== PugsFckGov-Tools (Ethical Hacking Suite) ===")
    for i, mod in enumerate(modules, 1):
        print(Fore.YELLOW + f"{i}. {mod['name']}: {mod['desc']}")
    print(Fore.CYAN + "\nDigite o número do módulo (1-{len(modules)}) ou 'q' para sair.")

def module_menu(module_index):
    mod = modules[module_index - 1]
    while True:
        print(Fore.CYAN + f"\n=== {mod['name']} ===")
        print(Fore.YELLOW + "1. Install")
        print(Fore.YELLOW + "2. Run")
        print(Fore.YELLOW + "3. Back")
        choice = input(Fore.GREEN + "Escolha (1-3): ").strip().lower()
        if choice == '1':
            print(Fore.MAGENTA + f"[*] Instalando {mod['tool']}...")
            subprocess.run(mod['install_cmd'], check=True)
            print(Fore.GREEN + f"[+] {mod['tool']} instalado! 🐶💥")
            if mod['name'] != "Anonize":
                anonize.setup_proxychains(proxies_list)
        elif choice == '2':
            if mod['input_type'] != "Nenhum (configura proxy)":
                target = input(Fore.GREEN + f"Digite o {mod['input_type']} (ex.: http://testphp.vulnweb.com): ").strip()
            else:
                target = None
            print(Fore.MAGENTA + f"[*] Executando {mod['tool']}...")
            current_ip = get_current_ip()
            func = getattr(globals()[mod['run_func'].split('.')[0]], mod['run_func'].split('.')[1])
            output = func(target, proxies_list)
            print(Fore.YELLOW + f"[*] IP atual: {current_ip}")
            print(Fore.GREEN + f"[+] Resultado: {output}")
            filename = f"pugsfckgov_{mod['name'].lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w') as f:
                f.write(ascii_art + f"\nPugsFckGov Scan - {mod['name']} - {datetime.now()}\n")
                f.write(f"Tool: {mod['tool']}\n")
                f.write(f"Target: {target or 'N/A'}\n")
                f.write(f"Output: {output}\n")
            print(Fore.BLUE + f"[*] Resultados salvos em {filename}")
        elif choice == '3':
            break
        else:
            print(Fore.RED + "[-] Opção inválida!")

def main():
    while True:
        show_menu()
        choice = input(Fore.GREEN + "Escolha um módulo (1-{len(modules)}) ou 'q': ").strip().lower()
        if choice == 'q':
            print(Fore.YELLOW + "[!] Saindo... Pugs voltam pro sofá! 🛋️🐶")
            break
        try:
            choice = int(choice)
            if 1 <= choice <= len(modules):
                module_menu(choice)
            else:
                print(Fore.RED + f"[-] Escolha entre 1 e {len(modules)}!")
        except ValueError:
            print(Fore.RED + "[-] Use um número ou 'q'!")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print(Fore.RED + "[-] Rode com sudo: sudo python3 main.py")
        sys.exit(1)
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[!] Interrompido. Pugs voltam pro sofá! 🛋️🐶")