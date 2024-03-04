import requests
import threading

url_connection_ip = 'https://api.ipify.org?format=json'

word_list_proxy = "wordlist_proxies.txt"

valid_proxies = []

def write_file():
    with open(word_list_proxy, "w") as file:
        for proxy in valid_proxies:
            file.write(proxy + "\n")

def _validate_proxy(url, proxy, timeout):
    try:
        r = requests.get(url, proxies={"http": proxy, "https": proxy}, timeout=timeout)
        if r.ok:
            ip, _ = proxy.split(":")
            response = r.json()
            if response and response['ip'] == ip:
                print('Rotated IP %s succeed' % proxy)
                valid_proxies.append(proxy)
    except Exception as e:
        pass
    return valid_proxies


def check_connection(proxies, timeout=5):
    for proxy in proxies:
        t = threading.Thread(target=_validate_proxy, args=(url_connection_ip, proxy,timeout))
        t.start()
    for thread in threading.enumerate():
        if thread != threading.current_thread():
            thread.join()
    write_file()
    return valid_proxies
