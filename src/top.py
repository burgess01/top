""" Program in order to create a 'top' command implemented in Python. """

# needed imports
import schedule
import psutil
from datetime import date
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

    # cannot get shared libs due to Mac, showing other stats instead
    cpu_count = psutil.cpu_count()
    phys_cpus = psutil.cpu_count(logical=False)

    # Cannot get memory regions due to having a Mac, showing other stats instead
    numUsers = len(psutil.users())
    bootTime = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")

    # physical memory
    vm = psutil.virtual_memory()

    # VM
    totalvm = psutil.virtual_memory().total
    swap = psutil.swap_memory()

    # Networks
    network_info = psutil.net_io_counters()

    # Disks
    disk_info = psutil.disk_io_counters()

    # return all of the metrics calculated in this function
    return (
        processes,
        load_averages,
        cpu_usage,
        overall_usage,
        cpu_count,
        phys_cpus,
        numUsers,
        bootTime,
        vm,
        totalvm,
        swap,
        network_info,
        disk_info,
    )


def process_stats():
    """Function to calculate order of processes in top command."""
    # create process list and initializations of needed func variables
    processes = []
    sleeping = 0
    running = 0
    threads = 0
    overallCPUPerc = 0

    # calculate the overall CPU percentage
    # over all processes psutil can grab
    for process in psutil.process_iter():
        try:
            overallCPUPerc += psutil.Process(process.pid).memory_info()[0] / 2.0**30
        except:
            overallCPUPerc += 0

    # calculate various statistics over every process
    # psutil can grab
    for process in psutil.process_iter():
        # PID
        id = process.pid
        # process name
        name = process.name()
        # CPU percent
        proc = psutil.Process(id)
        # status
        status = process.status()

        # get username that process is from
        user = process.username()

        try:
            # try to calculate the memory usage
            memoryUse = proc.memory_info()[0] / 2.0**30
        except:
            memoryUse = 0

        if process.status() == "sleeping":
            # count process if it is sleeping
            sleeping += 1
        elif process.status() == "running":
            # count process if it is running
            running += 1

        try:
            # count all threads from the process if able
            threads += process.num_threads()
        except:
            threads += 0

        # sum up memory usage and divide for CPU %
        cpuPerc = (memoryUse / overallCPUPerc) * 100

        # calculate the time that the process begin running
        seconds = process.create_time()
        start = datetime.fromtimestamp(seconds)

        # get the current time
        current = datetime.now()

        # calculate the difference between the process
        # start time and the current time
        difference = current - start

        # change the time difference into a usable format
        seconds = int(difference.total_seconds())
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        # concatenate together the calculated difference
        formatted_time = str(hours) + ":" + str(minutes) + ":" + str(seconds)

        # create a list in the list containing the calculated process info
        processes.append(
            [id, name[:12], round(cpuPerc, 2), formatted_time, user, status]
        )
    # order the list in descending order of cpu percentage
    processes.sort(key=lambda processes: processes[2], reverse=True)

    # return calculated metrics
    return processes, sleeping, running, threads


def top():
    """Function to compile all diagnostic information into a organized display."""
    # call needed function metrics
    (
        processes,
        load_averages,
        cpu_usage,
        overall_usage,
        cpu_count,
        phys_cpus,
        numUsers,
        bootTime,
        vm,
        totalvm,
        swap,
        network_info,
        disk_info,
    ) = upper_diagnostics()

    processes, sleeping, running, threads = process_stats()

    # create now variable for accurate timekeeping
    newnow = datetime.now()

    print(
        f"Processes: {len(processes)} total, {running} running, {sleeping} sleeping, {threads} threads",
        "{:>20}".format(newnow.strftime("%H:%M:%S")),
    )
    print(
        f"Load Avg: {round(load_averages[0], 2)}, {round(load_averages[1], 2)}, {round(load_averages[2], 2)}  CPU usage: {round((cpu_usage[0]/overall_usage) * 100, 2)}% user, {round((cpu_usage[2]/overall_usage) * 100,2)}% sys, {round((cpu_usage[3]/overall_usage) * 100,2)}% idle"
    )
    print(
        f"CPU counts: {cpu_count} total, {phys_cpus} physical  Users: {numUsers}  Boot Time: {bootTime}"
    )
    print(f"PhysMem: {size(vm[0])} used, {size(vm[7])} wired, {vm[5]} inactive.")
    print(f"VM: {size(totalvm)} vsize, {swap[4]}(0) swapins, {swap[5]}(0) swapouts")
    print(
        f"Networks: packets: {network_info[3]}/{size(network_info[3])} in, {network_info[2]}/{size(network_info[2])} out."
    )
    print(
        f"Disks: {disk_info[0]}/{size(disk_info[0])}G read, {disk_info[1]}/{size(disk_info[1])} written"
    )

    # lower section print
    print("\nPID       COMMAND    CPU%   TIME       USER     STATUS")
    for i in range(14):
        proc = processes[i]
        print("{: <7} {: <12} {: <5} {: <8} {: <11} {: <10}".format(*proc))


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
        try:
            iterations = int(sys.argv[1])
            # run for the amount of times entered
            for i in range(iterations):
                top()
                time.sleep(1)
        except:
            print(
                "Please enter an integer value for the amount of times you want the program to run."
            )


if __name__ == "__main__":
    main()
