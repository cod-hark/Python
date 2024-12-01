#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
import subprocess
import platform
import ipaddress

def validate_ip(ip_address):
    """Valida si la dirección IP tiene un formato correcto."""
    try:
        ipaddress.ip_address(ip_address)
        return True
    except ValueError:
        return False

def get_os_type():
    """Detecta el sistema operativo local."""
    return platform.system().lower()

def get_ttl(ip_address):
    """Obtiene el valor TTL de una dirección IP mediante `ping`."""
    try:
        # Determinar el comando de ping según el sistema operativo
        os_type = get_os_type()
        if os_type == "windows":
            cmd = ["ping", "-n", "1", ip_address]
        else:  # Linux/MacOS
            cmd = ["ping", "-c", "1", ip_address]
        
        # Ejecutar el comando de ping
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        output = proc.stdout

        # Extraer TTL usando una expresión regular
        ttl_match = re.search(r"ttl[=|:](\d+)", output, re.IGNORECASE)
        if ttl_match:
            return int(ttl_match.group(1))
        else:
            raise ValueError("No se encontró el TTL en la respuesta del ping.")
    
    except subprocess.CalledProcessError:
        raise ConnectionError(f"No se pudo alcanzar la IP {ip_address}. Verifica la conexión o la dirección.")
    except Exception as e:
        raise RuntimeError(f"Error al obtener el TTL para {ip_address}: {e}")

def get_os(ttl):
    """Determina el sistema operativo en función del TTL."""
    if ttl >= 0 and ttl <= 64:
        return "Linux/Unix"
    elif ttl >= 65 and ttl <= 128:
        return "Windows"
    elif ttl >= 129 and ttl <= 255:
        return "Otros (posiblemente dispositivos de red)"
    else:
        return "No identificado"

def analyze_ips(ip_addresses):
    """Analiza una lista de direcciones IP para determinar su sistema operativo."""
    results = []
    for ip in ip_addresses:
        try:
            if not validate_ip(ip):
                print(f"[!] Dirección IP inválida: {ip}")
                continue

            print(f"[INFO] Analizando {ip}...")
            ttl = get_ttl(ip)
            os_name = get_os(ttl)
            results.append((ip, ttl, os_name))
        except Exception as e:
            print(f"[ERROR] {e}")
    return results

def display_results(results):
    """Muestra los resultados del análisis."""
    if not results:
        print("[!] No se obtuvieron resultados.")
        return

    print("\nResultados del análisis:")
    print("-" * 50)
    for ip, ttl, os_name in results:
        print(f"IP: {ip} | TTL: {ttl} | Sistema Operativo: {os_name}")
    print("-" * 50)

def save_results(results, file_name="results.txt"):
    """Guarda los resultados en un archivo de texto."""
    try:
        with open(file_name, "w") as f:
            f.write("Resultados del análisis:\n")
            f.write("-" * 50 + "\n")
            for ip, ttl, os_name in results:
                f.write(f"IP: {ip} | TTL: {ttl} | Sistema Operativo: {os_name}\n")
            f.write("-" * 50 + "\n")
        print(f"[INFO] Resultados guardados en {file_name}")
    except Exception as e:
        print(f"[ERROR] No se pudo guardar el archivo: {e}")

if __name__ == "__main__":
    # Validar entrada
    if len(sys.argv) < 2:
        print("\n[!] Uso: python3 " + sys.argv[0] + " <direccion-ip> [<direccion-ip> ...]\n")
        sys.exit(1)

    ip_addresses = sys.argv[1:]
    results = analyze_ips(ip_addresses)

    # Mostrar resultados
    display_results(results)

    # Preguntar si se desean guardar los resultados
    save = input("\n¿Deseas guardar los resultados en un archivo? (s/n): ").strip().lower()
    if save == "s":
        save_results(results)
