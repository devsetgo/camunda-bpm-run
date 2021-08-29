# -*- coding: utf-8 -*-
import httpx
from tqdm import tqdm
import uuid
import random

base_url: str = "http://localhost:8080/engine-rest"
auth_list = [("admin", "rules"), ("bob", "bob")]


def random_auth():
    return random.choice(auth_list)


def make_tasks(qty: str = None):
    if qty is None:
        qty = 100

    url: str = (
        "http://localhost:8080/engine-rest/process-definition/key/test_process/start"
    )
    for t in tqdm(range(qty)):
        # print(t)
        data: dict = {
            "FormField_0bd4rco": {
                "type": "String",
                "value": "Something, something",
                "valueInfo": {},
            },
            "businessKey": f"CASE-{uuid.uuid4()}",
        }
        r = httpx.post(url, json=data, auth=random_auth())


if __name__ == "__main__":
    make_tasks()
