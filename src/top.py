""" Program in order to create a 'top' command implemented in Python. """

# needed imports
import schedule
import psutil
from datetime import datetime
from datetime import timedelta
import time
import os
import typer
import sys

# create objects
now = datetime.now()


def upper_diagnostics():
    """Function to calculate all 'upper' diagnostics."""
    # maybe make a class/enumeration?
    # processes
    processes = list(psutil.process_iter())

    # load average
    load_averages = psutil.getloadavg()

    # cpu usage
    cpu_usage = psutil.cpu_times()
    overall_usage = cpu_usage[0] + cpu_usage[2] + cpu_usage[3]

    # shared libs

    # mem regions

    # physical memory

    # VM
    vm = psutil.virtual_memory()

    # Networks
    network_info = psutil.net_io_counters()

    # Disks
    disk_info = psutil.disk_io_counters()

    return (
        processes,
        load_averages,
        cpu_usage,
        overall_usage,
        vm,
        network_info,
        disk_info,
    )


def process_stats():
    """Function to calculate order of processes in top command."""
    # for all processes, get: (list of lists)
    processes = []

    for process in psutil.process_iter():
        # PID
        id = process.pid
        # process name
        name = process.name()
        # CPU percent
        proc = psutil.Process(id)
        # status
        status = process.status()

        try:
            memoryUse = proc.memory_info()[0] / 2.0**30
        except:
            memoryUse = 0

        # time created
        seconds = process.create_time()
        start = datetime.fromtimestamp(seconds)
        current = datetime.now()
        difference = current - start

        formatted_time = str(difference).split(".")[0]

        processes.append(
            [id, name[:12], round((memoryUse * 100), 1), formatted_time, status]
        )
    processes.sort(key=lambda processes: processes[2], reverse=True)

    return processes


def top():
    """Function to compile all diagnostic information into a organized display."""
    upper_diagnostics()
    pass


def main(
    nonInteract: bool = typer.Option(
        None,
        "--non-interactive",
        help="if you want the program to run only one time or iteratively.",
    )
):
    if nonInteract is not None:
        # if they want to run it more than once:
        schedule.every(1).seconds.do(top(nonInteract))
    else:
        # run normally through schedule
        top(nonInteract)


if __name__ == "__main__":
    main()
