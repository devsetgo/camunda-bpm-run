# -*- coding: utf-8 -*-
import requests
from tqdm import tqdm
import secrets


def get_history(process_id:str):
    print(process_id['id'])
    url:str=f"http://localhost:8080/engine-rest/history/task?processInstanceId={process_id['id']}"
    r = requests.get(url=url)
    print(r.json())

def get_process_id():
    r = requests.get(url="http://localhost:8080/engine-rest/process-instance")
    if r.status_code == 200:
        return r.json()

def main():
    data = get_process_id()
    for d in tqdm(data):
        get_history(process_id=d)

if __name__ == "__main__":
    main()
