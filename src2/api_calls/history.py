# -*- coding: utf-8 -*-
import httpx
from tqdm import tqdm
import secrets
import random

base_url: str = "http://localhost:8080/engine-rest"
auth = ("admin", "rules")


# def random_auth():
#     return random.choice(auth_list)

def get_assignment_history(proc_id: str):
    url = f"{base_url}/history/user-operation?processInstanceId={proc_id}"
    r = httpx.get(url, auth=auth)
    data = r.json()
    # print(data)
    return data

def get_comment_history(proc_id: str):
    url = f"{base_url}/history/user-operation?processInstanceId={proc_id}"
    r = httpx.get(url, auth=auth)
    data = r.json()
    # print(data)
    return data

def get_process_history(proc_id: str):
    url = f"{base_url}/history/user-operation?processInstanceId={proc_id}"
    r = httpx.get(url, auth=auth)
    data = r.json()
    # print(data)
    return data

def run():
    url = f"{base_url}/history/activity-instance"
    r = httpx.get(url, auth=auth)
    data = r.json()

    # print(data)
    get_process_history(data[0]["processInstanceId"])
    # for rx in tqdm(data):
    #     get_process_history(rx['processInstanceId'])


if __name__ == "__main__":
    run()
