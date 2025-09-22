import subprocess
from colorama import Fore

def hash_crack(target, proxies_list):
    if not target:
        return "[-] Hash necessário!"
    with open("/tmp/hash.txt", "w") as f:
        f.write(target)
    cmd = ["proxychains", "hashcat", "-m", "0", "/tmp/hash.txt", "/usr/share/wordlists/rockyou.txt"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"[-] Erro no Hashcat: {e.stderr}"