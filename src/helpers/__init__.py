import random
import os

file_path = 'wordlist_proxies.txt'

def random_index(array):
    return random.randint(0, len(array) - 1)


def identify():
    if os.path.isfile(file_path):
        return True
    else:
        return False

def get_list_file():
    list_proxy_all = []

    with open(file_path, 'r') as file:
        lines = file.readlines()
    for line in lines:
        list_proxy_all.append(line.strip())
    return list_proxy_all

def insert_data_to_file(arrayValue):
    for data in arrayValue:
        with open(file_path, 'a') as file:
            file.write(data + '\n')

def get_list_ip():
    list_proxy_all = get_list_file()
    index = random_index(list_proxy_all)
    randm_proxy = list_proxy_all[index].split(":")
    list_proxy_all = []
    return randm_proxy


def remove_content_file():
    with open(file_path, "w") as file:
        pass


def remove_ip_list(ip, port):
    item_remove = f'{ip}:{port}'
    list_proxy_all = get_list_file()
    if item_remove in list_proxy_all:
        list_proxy_all.remove(item_remove)

    with open(file_path, "w") as file:
        for item in list_proxy_all:
            file.write("%s\n" % item)
