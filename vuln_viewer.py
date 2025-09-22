import subprocess
from colorama import Fore

def zap_scan(target, proxies_list):
    if not target:
        return "[-] URL necessária!"
    cmd = ["proxychains", "zaproxy", "-quickurl", target, "-quickout", f"/tmp/zap_report_{target.replace('://', '_')}.xml"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return f"[+] Scan concluído! Relatório em /tmp/zap_report_{target.replace('://', '_')}.xml"
    except subprocess.CalledProcessError as e:
        return f"[-] Erro no ZAP: {e.stderr}"