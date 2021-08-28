# -*- coding: utf-8 -*-
import requests
from tqdm import tqdm
import secrets
import random
import silly

base_url: str = "http://localhost:8080/engine-rest"
auth_list = [("admin", "rules"), ("bob", "bob")]


def get_history(process_id: str):
    print(process_id["id"])
    url: str = f"{base_url}/history/task?processInstanceId={process_id['id']}"
    r = requests.get(url=url, auth=auth)
    print(r.json())


def get_process_id():
    r = requests.get(url=f"{base_url}/process-instance", auth=random_auth())
    if r.status_code != 200:
        print(r.status_code)
    else:
        return r.json()


def random_auth():
    return random.choice(auth_list)


def get_task_id(proc_id: str):
    r = requests.get(
        url=f"{base_url}/task?processInstanceId={proc_id}", auth=random_auth()
    )

    if r.status_code == 200:
        data = r.json()
        for d in data:
            unclaim_task(task_id=d["id"])
            make_comment(task_id=d["id"], proc_id=proc_id)
            claim_task(task_id=d["id"])
            make_comment(task_id=d["id"], proc_id=proc_id)
            assign_task(task_id=d["id"])
            make_comment(task_id=d["id"], proc_id=proc_id)
            submit_task_one(task_id=d["id"])


def submit_task_one(task_id: str):
    data = {"test2": {"type": "String", "value": silly.sentence(), "valueInfo": {}}}
    url = f"{base_url}/task/{task_id}/submit-form"
    r = requests.post(url=url, json={"userId": random_name()}, auth=random_auth())



def unclaim_task(task_id: str):
    url = f"{base_url}/task/{task_id}/unclaim"
    r = requests.post(url=url, json={"userId": ""}, auth=random_auth())


def claim_task(task_id: str):
    url = f"{base_url}/task/{task_id}/claim"
    r = requests.post(url=url, json={"userId": random_name()}, auth=random_auth())


def assign_task(task_id: str):
    url = f"{base_url}/task/{task_id}/assign"
    r = requests.post(url=url, json={"userId": random_name()}, auth=random_auth())


def make_comment(task_id: str, proc_id: str):
    url = f"{base_url}/task/{task_id}/comment/create"

    data = {"message": silly.sentence(), "processInstanceId": proc_id}
    r = requests.post(url=url, json=data, auth=random_auth())


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
    data = get_process_id()
    if data is not None:
        for p in tqdm(data):
            get_task_id(proc_id=p["id"])

    # for d in tqdm(data):
    #     get_history(process_id=d)


if __name__ == "__main__":
    main()
