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
    (
        processes,
        load_averages,
        cpu_usage,
        overall_usage,
        vm,
        network_info,
        disk_info,
    ) = upper_diagnostics()

    processes = process_stats()
    newnow = datetime.now()
    # add user - readable version, change bit values to GB values
    # exec call , sys package, shell = True; look into textual for better option
    print(
        f"Processes: {len(processes)} total, _ running, _ sleeping, _ threads",
        "{:>25}".format(newnow.strftime("%H:%M:%S")),
    )
    print(
        f"Load Avg: {round(load_averages[0], 2)}, {round(load_averages[1], 2)}, {round(load_averages[2], 2)}  CPU usage: {round((cpu_usage[0]/overall_usage) * 100, 2)}% user, {round((cpu_usage[2]/overall_usage) * 100,2)}% sys, {round((cpu_usage[3]/overall_usage) * 100,2)}% idle"
    )
    print(f"SharedLibs: _ resident, _ data, _ linkedit.")
    print(f"MemRegions: _ total, _ resident, _ private, _ shared.")
    print(f"PhysMem: _ used (_ wired), _ unused.")
    print(
        f"VM: {vm[0]} vsize, {vm[7]} wired, {vm[2]} available, {vm[4]} active, {vm[5]} inactive."
    )
    print(
        f"Networks: packets: {network_info[3]}/{network_info[3] / (1024.0 ** 3)}G in, {network_info[2]}/{network_info[2] / (1024.0 ** 3)}G out."
    )
    print(
        f"Disks: {disk_info[0]}/{disk_info[0] >> 20}G read, {disk_info[1]}/{disk_info[1] >> 20}G written"
    )

    # lower section print
    print("PID         COMMAND        CPU%           TIME             STATUS")
    for i in range(15):
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
