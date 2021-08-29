# -*- coding: utf-8 -*-
import httpx
from tqdm import tqdm
import secrets
import random
import silly

base_url: str = "http://localhost:8080/engine-rest"
auth_list = [("admin", "rules"), ("bob", "bob")]


def get_process_id(qty:int=None):
    if qty is None:
        qty = 9
    r = httpx.get(url=f"{base_url}/process-instance?maxResults={qty}", auth=random_auth())
    if r.status_code != 200:
        print(r.status_code)
    else:
        return r.json()


def random_auth():
    return random.choice(auth_list)


def get_task_id(proc_id: str):
    r = httpx.get(
        url=f"{base_url}/task?processInstanceId={proc_id}", auth=random_auth()
    )

    if r.status_code == 200:
        data = r.json()
        for d in data:
            for _ in range(5):
                unclaim_task(task_id=d["id"])
                claim_task(task_id=d["id"])
                make_comment(task_id=d["id"], proc_id=proc_id)
                assign_task(task_id=d["id"])
                
            # submit_task_one(task_id=d["id"])


def submit_task_one(task_id: str):
    data = {"test2": {"type": "String", "value": silly.sentence(), "valueInfo": {}}}
    url = f"{base_url}/task/{task_id}/submit-form"
    r = httpx.post(url=url, json={"userId": random_name()}, auth=random_auth())
    # print(r.status_code)

def unclaim_task(task_id: str):
    url = f"{base_url}/task/{task_id}/unclaim"
    r = httpx.post(url=url, json={"userId": ""}, auth=random_auth())
    # print(r.status_code)

def claim_task(task_id: str):
    url = f"{base_url}/task/{task_id}/claim"
    r = httpx.post(url=url, json={"userId": random_name()}, auth=random_auth())
    # print(r.status_code)

def assign_task(task_id: str,name:str=None):
    url = f"{base_url}/task/{task_id}/assign"
    auth=random_auth()
    
    if name is None:
        name=''
    r = httpx.post(url=url, json={"userId": random_name()}, auth=auth)
    # # print(r.status_code)

def make_comment(task_id: str, proc_id: str):
    url = f"{base_url}/task/{task_id}/comment/create"
    for _ in range(random.randint(1, 5)):
        data = {"message": silly.sentence(), "processInstanceId": proc_id}
        r = httpx.post(url=url, json=data, auth=random_auth())
        

def random_name():
    names: list = [
        "bob",
        "jim",
        "joe",
        "jane",
        "terry",
        "gene",
        "al",
        "linda",
        "cindy",
        "tony",
    ]
    return random.choice(names)


def main():
    data = get_process_id(qty=500)
    if data is not None:
        for p in tqdm(data):
            get_task_id(proc_id=p["id"])


if __name__ == "__main__":
    main()
