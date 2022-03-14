import sys
import os
import time
import subprocess
import psutil
from tqdm import tqdm
import psutil
import platform
from datetime import datetime

os.system("color f0")
os.system("echo off")
os.system("cls")

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

class System_Information:
    def SystemInfo():
        print("="*40, "System Information", "="*40)
        uname = platform.uname()
        print(f"System: {uname.system}")
        print(f"Node Name: {uname.node}")
        print(f"Release: {uname.release}")
        print(f"Version: {uname.version}")
        print(f"Machine: {uname.machine}")
        print(f"Processor: {uname.processor}")

# Boot Time
class Boot_Time:
    def BootTime():
        print("="*40, "Boot Time", "="*40)
        boot_time_timestamp = psutil.boot_time()
        bt = datetime.fromtimestamp(boot_time_timestamp)
        print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")

#CPU
class CPUINFO:
    def CpuInfo():
        print("="*40, "CPU Info", "="*40)
        # number of cores
        print("Physical cores:", psutil.cpu_count(logical=False))
        print("Total cores:", psutil.cpu_count(logical=True))
        # CPU frequencies
        cpufreq = psutil.cpu_freq()
        print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
        print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
        print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
        # CPU usage
        print("CPU Usage Per Core:")
        for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
            print(f"Core {i}: {percentage}%")
        print(f"Total CPU Usage: {psutil.cpu_percent()}%")

#MEMORY
class MemoryInfo:
    def MemoryInformation():
        # Memory Information
        print("="*40, "Memory Information", "="*40)
        # get the memory details
        svmem = psutil.virtual_memory()
        print(f"Total: {get_size(svmem.total)}")
        print(f"Available: {get_size(svmem.available)}")
        print(f"Used: {get_size(svmem.used)}")
        print(f"Percentage: {svmem.percent}%")
        print("="*20, "SWAP", "="*20)
        # get the swap memory details (if exists)
        swap = psutil.swap_memory()
        print(f"Total: {get_size(swap.total)}")
        print(f"Free: {get_size(swap.free)}")
        print(f"Used: {get_size(swap.used)}")
        print(f"Percentage: {swap.percent}%")

#DISK
class DISK:
    def DiskInformation():
        # Disk Information
        print("="*40, "Disk Information", "="*40)
        print("Partitions and Usage:")
        # get all disk partitions
        partitions = psutil.disk_partitions()
        for partition in partitions:
            print(f"=== Device: {partition.device} ===")
            print(f"  Mountpoint: {partition.mountpoint}")
            print(f"  File system type: {partition.fstype}")
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                # this can be catched due to the disk that
                # isn't ready
                continue
            print(f"  Total Size: {get_size(partition_usage.total)}")
            print(f"  Used: {get_size(partition_usage.used)}")
            print(f"  Free: {get_size(partition_usage.free)}")
            print(f"  Percentage: {partition_usage.percent}%")
        # get IO statistics since boot
        disk_io = psutil.disk_io_counters()
        print(f"Total read: {get_size(disk_io.read_bytes)}")
        print(f"Total write: {get_size(disk_io.write_bytes)}")

def getListOfProcessSortedByMemory():
    '''
    Get list of running process sorted by Memory Usage
    '''
    listOfProcObjects = []
    # Iterate over the list
    for proc in psutil.process_iter():
       try:
           # Fetch process details as dict
           pinfo = proc.as_dict(attrs=['pid', 'name', 'username'])
           pinfo['vms'] = proc.memory_info().vms / (1024 * 1024)
           # Append dict to list
           listOfProcObjects.append(pinfo);
       except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
           pass

    # Sort list of dict by key vms i.e. memory usage
    listOfProcObjects = sorted(listOfProcObjects, key=lambda procObj: procObj['vms'], reverse=True)

    for process in listOfProcObjects:
        print(process)

def root(Loop):
    username = "root"
    password = "admin"
    while Loop:
        attach_username = input(str("[+] Enter username: "))
        if attach_username != username:
            print(f"Wrong username. Please try again. You wrote - {attach_username}")
        else:
            attach_password = input(str("[+] Enter password: "))
            if attach_password == password:
                print("Logged in!")
                Loop = False
                menu()
            else:
                print(f"Wrong password. Please try again. You wrote - {attach_password}")



def menu():
    print("""
[1] Diagnose PC
[2] Information
[3] Choose disk
[4] Check Network Interfaces
[5] Check Network Adapter Info
[6] Reboot
[7] Exit
""")
    choose_menu = input(str("Select > "))
    if choose_menu == "1":
        packages = ["python3","terminal","lib3sound","helpsystem"]
        for i in range(1):
            time.sleep(1)
            print("Checking for Windows Update!")
            working_dir=os.getcwd()
            with open("updatecheck.bat","a") as updatecheck:
                updatecheck.truncate(0)
                updatecheck.write("wmic qfe get Hotfixid > hotfixes ")
                updatecheck.close()
            time.sleep(1)
            subprocess.run(["updatecheck.bat"],cwd=working_dir)
            time.sleep(2)
            with open("hotfixes","r") as file:
                hotfixes=file.read().replace('\x00', '')
                print(hotfixes)

            class CPU_RAM:
                os.system("cls")
                print("Checking RAM: ")
                print("Virtual Memory",psutil.virtual_memory())  # physical memory usage
                memory_used = psutil.virtual_memory()[2]
                print('Memory % used:',memory_used,"%")
                if memory_used > 50:
                    print("Average percentage. Good yet.")
                if memory_used > 78:
                    print("High percentage. Your Memory is being highly used.")
                if memory_used > 90:
                    print("Very high percentage.")
                try:
                    print('\033[91m'+"CTRL+C TO INTERRUPT"+'\033[0m')
                    with tqdm(total=100, desc='cpu%', position=1) as cpubar, tqdm(total=100, desc='ram%', position=0) as rambar:
                        while True:
                            rambar.n=psutil.virtual_memory().percent
                            cpubar.n=psutil.cpu_percent()
                            rambar.refresh()
                            cpubar.refresh()
                            time.sleep(0.5)
                except KeyboardInterrupt:
                    listProcesses = input(str("List All Running Processes ? y/n: "))
                    if listProcesses == "y":
                        getListOfProcessSortedByMemory()
                        input("Write anything to next step. ")
                        os.system("color f0")
                        os.system("cls")
                        System_Information.SystemInfo()
                        currentPage=1
                        runInfo = True
                        while runInfo:
                            next1 = int(input(f"Page {currentPage}/5, write 2,3,4,5 to move to next page. (write 99 if back to menu.)> "))
                            if next1 == 1:
                                os.system("color f0")
                                os.system("cls")
                                currentPage = 1
                                System_Information.SystemInfo()
                            elif next1 == 2:
                                os.system("color f0")
                                os.system("cls")
                                currentPage = 2
                                Boot_Time.BootTime()
                            elif next1 == 3:
                                os.system("color f0")
                                os.system("cls")
                                currentPage = 3
                                CPUINFO.CpuInfo()
                            elif next1 == 4:
                                os.system("color f0")
                                os.system("cls")
                                currentPage = 4
                                MemoryInfo.MemoryInformation()
                            elif next1 == 5:
                                os.system("color f0")
                                os.system("cls")
                                currentPage = 5
                                DISK.DiskInformation()
                            elif next1 == 99:
                                os.system("color f0")
                                runInfo = False
                                os.system("cls")
                                menu()
                            else:
                                print("None of this page exists.")

                    elif listProcesses == "n":
                        os.system("color f0")
                        os.system("cls")
                        System_Information.SystemInfo()
                        currentPage=1
                        runInfo = True
                        while runInfo:
                            next1 = int(input(f"Page {currentPage}/5, write 2,3,4,5 to move to next page. (write 99 if back to menu.)> "))
                            if next1 == 1:
                                os.system("color f0")
                                os.system("cls")
                                currentPage = 1
                                System_Information.SystemInfo()
                            elif next1 == 2:
                                os.system("color f0")
                                os.system("cls")
                                currentPage = 2
                                Boot_Time.BootTime()
                            elif next1 == 3:
                                os.system("color f0")
                                os.system("cls")
                                currentPage = 3
                                CPUINFO.CpuInfo()
                            elif next1 == 4:
                                os.system("color f0")
                                os.system("cls")
                                currentPage = 4
                                MemoryInfo.MemoryInformation()
                            elif next1 == 5:
                                os.system("color f0")
                                os.system("cls")
                                currentPage = 5
                                DISK.DiskInformation()
                            elif next1 == 99:
                                os.system("color f0")
                                runInfo = False
                                os.system("cls")
                                menu()
                            else:
                                print("None of this page exists.")

                    else:
                        print("Answer not acceptable.")
                        menu()


    if choose_menu == "2":
        print("""
OS Helper v1.0.0 Alpha
 This Software helps finding computer problems, its basically a diagnose. You can scan your computers to find
 some errors and problems, it checks for the hardware, updates, and other..
 
 Signature.
""")
    if choose_menu == "4":
        os.system("netsh interface show interface")
        os.system("netsh interface ip show addresses")
    if choose_menu == "5":
        os.system("powershell Get-NetAdapterBinding -IncludeHidden -AllBindings")
    if choose_menu == "6":
        rebootPC = input(str("Really want to reboot PC? y/n > "))
        if rebootPC == "y":
            os.system("reboot")
        elif rebootPC == "n":
            menu()
        else:
            print("Answer not acceptable.")
            menu()
    if choose_menu == "7":
        print("GoodBye!")
        sys.exit()
    menu()


if __name__ == "__main__":
    root(Loop=True)


