import subprocess
from colorama import Fore

def scan_port(target, proxies_list):
    if not target:
        return "[-] IP ou domínio necessário!"
    cmd = ["proxychains", "nmap", "-sT", target]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"[-] Erro no Nmap: {e.stderr}"

def scan_vuln_nikto(target, proxies_list):
    if not target:
        return "[-] URL necessária!"
    cmd = ["proxychains", "nikto", "-h", target]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"[-] Erro no Nikto: {e.stderr}"