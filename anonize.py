import random
import os
from colorama import Fore

def setup_proxychains(proxies_list):
    proxy = random.choice(proxies_list)
    conf = f"""
dynamic_chain
proxy_dns
tcp_read_time_out 15000
tcp_connect_time_out 8000
[ProxyList]
{proxy['type']} {proxy['ip']} {proxy['port']}
"""
    try:
        with open("/etc/proxychains.conf", "w") as f:
            f.write(conf)
        return f"[+] Proxychains configurado com {proxy['ip']}:{proxy['port']} ({proxy['country']})"
    except PermissionError:
        return "[-] Rode com sudo para configurar Proxychains!"