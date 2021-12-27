# -*- coding: utf-8 -*-
import process_start
import task_processing
import user
import history


def run():
    user.run()
    process_start.make_tasks(qty=10)
    task_processing.main()
    history.run()

if __name__ == "__main__":
    run()
