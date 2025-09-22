import subprocess
from colorama import Fore

def whois_lookup(target, proxies_list):
    if not target:
        return "[-] Domínio necessário!"
    cmd = ["proxychains", "whois", target]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"[-] Erro no Whois: {e.stderr}"