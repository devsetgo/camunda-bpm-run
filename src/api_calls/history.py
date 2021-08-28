# -*- coding: utf-8 -*-
import requests
from tqdm import tqdm
import secrets
import random

base_url: str = "http://localhost:8080/engine-rest"
auth_list = [("admin", "rules"), ("bob", "bob")]


def random_auth():
    return random.choice(auth_list)


def get_process_history(proc_id: str):
    url=f"{base_url}/history/user-operation?processInstanceId={proc_id}"
    r = requests.get(url, auth=random_auth())
    data=r.json()
    

def run():
    url=f"{base_url}/history/activity-instance"
    r = requests.get(url, auth=random_auth())
    resp=r.json()
    for rx in tqdm(resp):
        
        get_process_history(rx['processInstanceId'])

if __name__ == "__main__":
    run()