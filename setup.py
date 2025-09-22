import subprocess
import sys
from colorama import init, Fore

init(autoreset=True)

def run_command(cmd, desc):
    print(Fore.YELLOW + f"[*] {desc}: {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(Fore.GREEN + f"[+] Sucesso: {desc}")
        return True
    except subprocess.CalledProcessError as e:
        print(Fore.RED + f"[-] Erro: {e.stderr}")
        return False

def install():
    print(Fore.CYAN + "\n=== PugsFckGov-Tools Setup ===")
    print(Fore.YELLOW + "[*] Instalando dependências éticas para pentest...")
    
    commands = [
        (["apt", "update"], "Atualizando repositórios"),
        (["apt", "install", "-y", "proxychains", "nmap", "nikto", "hashcat"], "Ferramentas de scanning e utilities"),
        (["apt", "install", "-y", "zaproxy"], "OWASP ZAP (Vulnerability Viewer)"),
        (["apt", "install", "-y", "tor"], "Tor para anonimato"),
        (["pip3", "install", "-r", "requirements.txt"], "Bibliotecas Python"),
    ]
    
    for cmd, desc in commands:
        run_command(cmd, desc)
    
    print(Fore.YELLOW + "[*] Iniciando Tor (opcional)...")
    run_command(["systemctl", "start", "tor"], "Iniciando Tor")
    
    print(Fore.GREEN + "[+] Setup concluído! Rode 'sudo python3 main.py' 🐶💥")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print(Fore.RED + "[-] Rode com sudo: sudo python3 setup.py")
        sys.exit(1)
    try:
        install()
    except KeyboardInterrupt:
        print(Fore.YELLOW + "\n[!] Interrompido. Pugs voltam pro sofá! 🛋️🐶")