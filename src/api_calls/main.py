# -*- coding: utf-8 -*-
import process_start
import task_processing


def run():
    process_start.make_tasks(qty=1)
    task_processing.main()


if __name__ == "__main__":
    run()
