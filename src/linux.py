"""file to hold all files related to running top on Linux"""

# needed imports
import psutil
from datetime import datetime
from hurry.filesize import size

# create objects
now = datetime.now()


def upper_diagnostics():
    """This function calculates all 'upper' diagnostics"""

    # load average
    load_avg = psutil.getloadavg()

    # cpu usage:
    # usage
    cpu_usage = psutil.cpu_times()
    # overall usage
    overall_usage = cpu_usage[0] + cpu_usage[2] + cpu_usage[3]

    # memory regions
    p = psutil.Process()
    mem_regions = p.memory_maps()

    # VM
    vm = psutil.virtual_memory()

    # swap memory
    swap = psutil.swap_memory()

    # networks
    network_info = psutil.net_io_counters()

    # disks
    disk_info = psutil.disk_io_counters()

    # return all metrics calculated
    return (
        load_avg,
        cpu_usage,
        overall_usage,
        mem_regions,
        vm,
        swap,
        network_info,
        disk_info,
    )


def process_stats():
    """This function calculates the order of processes in terms of CPU%"""

    # create process list and initializations of needed variables
    processes = []
    sleeping = 0
    running = 0
    totalproc = 0
    threads = 0
    overallCPUPerc = 0

    # get total processes number
    totalproc = len(list(psutil.process_iter()))

    # calculate overall CPU percentage
    # over all processes psutil can grab
    for process in psutil.process_iter():
        try:
            overallCPUPerc += psutil.Process(process.pid).memory_info()[0] / 2.0**30
        except:
            overallCPUPerc += 0

    # iterate through all processes and grab info for all
    for process in psutil.process_iter():
        memoryUse = 0
        cpuPerc = 0

        # pid
        id = process.pid

        # process name
        name = process.name()

        # status
        status = process.status()

        # username
        user = process.username()

        # calculate CPU perc
        try:
            proc = psutil.Process(id)
            memoryUse = proc.memory_info()[0] / 2.0**30
            cpuPerc = (memoryUse / overallCPUPerc) * 100
        except:
            pass

        # sleeping or running
        if process.status() == "sleeping":
            # count process if it is sleeping
            sleeping += 1
        elif process.status() == "running":
            # count process if it is running
            running += 1

        # threads
        try:
            # count all threads from the process if able
            threads += process.num_threads()
        except:
            threads += 0

        # time running
        start = datetime.fromtimestamp(process.create_time())
        current = datetime.now()

        difference = current - start

        # change the time difference into a usable format
        seconds = int(difference.total_seconds())
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        # concatenate together the calculated difference
        formatted_time = str(hours) + ":" + str(minutes) + ":" + str(seconds)

        # add process info to process list
        # create a list in the list containing the calculated process info
        processes.append(
            [id, name[:12], round(cpuPerc, 2), formatted_time, user, status]
        )

    # order the list in descending order of cpu percentage
    processes.sort(key=lambda processes: processes[2], reverse=True)

    # return list and other metrics
    return processes, totalproc, sleeping, running, threads


def top():
    """This function compiles all diagnostic info and prints it to the terminal"""

    updatedTime = datetime.now()

    (
        load_avg,
        cpu_usage,
        overall_usage,
        mem_regions,
        vm,
        swap,
        network_info,
        disk_info,
    ) = upper_diagnostics()

    processes, totalproc, sleeping, running, threads = process_stats()

    print(
        f"Processes: {totalproc} total, {running} running, {sleeping} sleeping, {threads} threads",
        "{:>20}".format(updatedTime.strftime("%H:%M:%S")),
    )
    print(
        f"Load Avg: {round(load_avg[0], 2)}, {round(load_avg[1], 2)}, {round(load_avg[2], 2)}  CPU usage: {round((cpu_usage[0]/overall_usage) * 100, 2)}% user, {round((cpu_usage[2]/overall_usage) * 100,2)}% sys, {round((cpu_usage[3]/overall_usage) * 100,2)}% idle"
    )
    print(
        f"MemRegions: {mem_regions[2]} total, {mem_regions[1]} resident, {mem_regions[3]} private"
    )
    print(f"PhysMem: {size(vm[0])} total, {size(vm[1])} available")
    print(f"VM: {size(vm[0])} vsize, {swap[4]}(0) swapins, {swap[5]}(0) swapouts")
    print(f"Networks: packets: {network_info[2]} in, {network_info[3]} out")
    print(f"Disks: {disk_info[0]} read, {disk_info[1]} written")

    # lower section print
    print("\nPID       COMMAND    CPU%   TIME       USER     STATUS")
    for i in range(14):
        proc = processes[i]
        print("{: <7} {: <12} {: <5} {: <8} {: <11} {: <10}".format(*proc))
