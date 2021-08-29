# -*- coding: utf-8 -*-
import httpx
from tqdm import tqdm
import secrets
import random
from datetime import datetime,date

base_url: str = "http://localhost:8080/engine-rest"
auth = ("admin", "rules")

def get_process_instance_tasks(proc_id: str) -> list:
    """
    Get all tasks for a process instance
    :param proc_id: process instance id
    :return: list of tasks
    """
    url = url = f"{base_url}/task?processInstanceId={proc_id}"
    response = httpx.get(url, auth=auth)
    if response.status_code == 200:
        data=response.json()
        updated_data=process_task_list(data)
        return updated_data
    else:
        return []

def process_task_list(data:list):

    # 'due': '2021-09-04T18:17:29.289-0400'
    # .strftime('%Y-%m-%d %I:%M') 2021-09-11T18:17:29.202-0400
    for i in data:
        due_date= i['due'].split('T')
        simple_date =due_date[0]
        i['simple_due_date'] =simple_date

        create_date= i['due'].split('T')
        simple_create_date =create_date[0]
        i['simple_create_date'] =simple_create_date
        prioritization = define_priority(i)
        i['prioritization'] = prioritization

    return data

def define_priority(data:dict):
    priority_list = []
    priority_list.append(round(data['priority']/25))

    
    start = datetime.now()
    end =datetime.strptime(data['simple_due_date'], '%Y-%m-%d')
    diff = end-start
    priority_list.append(diff.days)
    return sum(priority_list)
    
def get_process_instance_tasks_comments(proc_id: str) -> list:
    """
    Get all tasks for a process instance
    :param proc_id: process instance id
    :return: list of tasks
    """
    url = url = f"{base_url}/task?processInstanceId={proc_id}"
    response = httpx.get(url, auth=auth)
    if response.status_code == 200:
        return response.json()
    else:
        return []
