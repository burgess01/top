""" Program in order to create a 'top' command implemented in Python. """

# needed imports
import schedule
import psutil
from datetime import datetime
from datetime import timedelta
from hurry.filesize import size
import time
import os
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
    vm = psutil.virtual_memory()

    # VM
    totalvm = psutil.virtual_memory().total
    swap = psutil.swap_memory()

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
        totalvm,
        swap,
        network_info,
        disk_info,
    )


def process_stats():
    """Function to calculate order of processes in top command."""
    # for all processes, get: (list of lists)
    processes = []
    sleeping = 0
    running = 0

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

        if process.status() == psutil.STATUS_SLEEPING:
            sleeping += 1
        elif process.status() == psutil.STATUS_RUNNING:
            running += 1

        # sum up memory usage and divide for CPU %

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

    return processes, sleeping, running


def top():
    """Function to compile all diagnostic information into a organized display."""
    (
        processes,
        load_averages,
        cpu_usage,
        overall_usage,
        vm,
        totalvm,
        swap,
        network_info,
        disk_info,
    ) = upper_diagnostics()

    processes, sleeping, running = process_stats()
    newnow = datetime.now()
    # add user - readable version, change bit values to GB values
    # exec call , sys package, shell = True; look into textual for better option
    print(
        f"Processes: {len(processes)} total, {running} running, {sleeping} sleeping, _ threads",
        "{:>25}".format(newnow.strftime("%H:%M:%S")),
    )
    print(
        f"Load Avg: {round(load_averages[0], 2)}, {round(load_averages[1], 2)}, {round(load_averages[2], 2)}  CPU usage: {round((cpu_usage[0]/overall_usage) * 100, 2)}% user, {round((cpu_usage[2]/overall_usage) * 100,2)}% sys, {round((cpu_usage[3]/overall_usage) * 100,2)}% idle"
    )
    print(f"SharedLibs: _ resident, _ data, _ linkedit.")
    print(f"MemRegions: _ total, _ resident, _ private, _ shared.")
    print(f"PhysMem: {size(vm[0])} used, {size(vm[7])} wired, {vm[5]} inactive.")
    print(f"VM: {totalvm} vsize, {swap[4]}(0) swapins, {swap[5]}(0) swapouts")
    print(
        f"Networks: packets: {network_info[3]}/{size(network_info[3])} in, {network_info[2]}/{size(network_info[2])} out."
    )
    print(
        f"Disks: {disk_info[0]}/{size(disk_info[0])}G read, {disk_info[1]}/{size(disk_info[1])} written"
    )

    # lower section print
    print("PID         COMMAND        CPU%           TIME             STATUS")
    for i in range(14):
        proc = processes[i]
        print("{: <10} {: <15} {: <10} {: <20} {: <20}".format(*proc))


def main():

    if len(sys.argv) == 1:
        try:
            # if they want to run it iteratively
            schedule.every(1).seconds.do(top)
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            sys.exit(0)
    else:
        # run once through a single top call
        top()


if __name__ == "__main__":
    main()
