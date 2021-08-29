# -*- coding: utf-8 -*-
import httpx
from tqdm import tqdm
import secrets
import random

base_url: str = "http://localhost:8080/engine-rest"
auth = ("admin", "rules")


# def random_auth():
#     return random.choice(auth_list)


def run():
    # check for bob
    url = f"{base_url}/user?id=bob"
    r = httpx.get(url=url, auth=auth)
    data = r.json()
    print(len(data))
    if len(data) == 0:
        data_dict = {
            "profile": {
                "id": "bob",
                "firstName": "Bob",
                "lastName": "Smith",
                "email": "bob@bob.com",
            },
            "credentials": {"password": "bob"},
        }
        url_create = f"{base_url}/user/create"
        r = httpx.post(url=url_create, json=data_dict, auth=auth)
        print(r.status_code)
        r = httpx.get(url=url, auth=auth)
        print(r.json())
    else:
        print('bob exists')

if __name__ == "__main__":
    run()
