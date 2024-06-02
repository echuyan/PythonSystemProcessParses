import subprocess
import const
from datetime import datetime
from subprocess import (
    run, PIPE
)

def get_processes(sortby = "mem"):
    if sortby == "cpu":
        result = subprocess.run(["ps","-eo","user,pid,%cpu,%mem,command","--sort=-%cpu"], capture_output=True, text = True)
            
        lines = result.stdout.splitlines()
        headers = lines[0].split()

        processes = []

        for line in lines[1:]:
            columns = line.split(maxsplit=len(headers)-1)
            proc_dict = dict(zip(headers,columns))
            processes.append(proc_dict)

        return(processes)
    else:
        result = subprocess.run(["ps","-eo","user,pid,%cpu,%mem,command","--sort=-%mem"], capture_output=True, text = True)
            
        lines = result.stdout.splitlines()
        headers = lines[0].split()

        processes = []

        for line in lines[1:]:
            columns = line.split(maxsplit=len(headers)-1)
            proc_dict = dict(zip(headers,columns))
            processes.append(proc_dict)

        return(processes)

if __name__ == '__main__':
    text = str()
    print(const.HEADING, end="")
    text += const.HEADING 
    print(const.USERS,end="")
    text += const.USERS
    processes = get_processes()
    total_mem = 0
    total_cpu = 0
    users_set=set()
    for process in processes:
        total_cpu += float(process["%CPU"])
        total_mem += float(process["%MEM"])
        users_set.add(process["USER"])
    
    users_list = list(users_set)
    for i, user in enumerate(users_list):
        if i != len(users_list)-1: 
            print(user,", ",end="", sep='')
            text += user + ", "
        else:
            print(user,sep='')
            text += user 
    text +="\n"
    
    print(const.PROCESSES, end="")
    text += const.PROCESSES
    print(len(processes),"\n")
    text += str(len(processes))
    text += '\n' + '\n'
   
    print(const.USERS_PROCESSES)
    text += const.USERS_PROCESSES + '\n'
    for user in users_set:
        print(user,": ", end="")
        text += user+": "
        i = 0
        for process in processes:
            if process["USER"] == user:
                i+=1
        print(i)
        text += str(i) +"\n"
    print('\n')
    text += '\n'
    print(const.RAM_USED, end="")
    text += const.RAM_USED
    print(total_mem,"%")
    text += str(total_mem) + "%" + '\n'
    print(const.CPU_USED, end="")
    text += const.CPU_USED
    print(total_cpu,"%")
    text += str(total_cpu) + "%" +'\n'
    print(const.MAX_RAM, end = "")
    text += const.MAX_RAM
    print(processes[0]["COMMAND"][:20])
    text += processes[0]["COMMAND"][:20] + '\n'
    print(const.MAX_CPU, end = "")
    text += const.MAX_CPU
    processes = get_processes("cpu")
    print(processes[0]["COMMAND"][:20])
    text += processes[0]["COMMAND"][:20] + '\n'

    filename = str(datetime.now())
    with open(filename,"w") as file:
        print(text, file = file)