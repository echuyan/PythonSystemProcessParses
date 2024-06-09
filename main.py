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
    text += const.HEADING 
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
            text += user + ", "
        else:
            text += user 
    text +="\n"
    
    text += const.PROCESSES
    text += str(len(processes))
    text += '\n' + '\n'
   
    text += const.USERS_PROCESSES + '\n'
    for user in users_set:
        text += user+": "
        i = 0
        for process in processes:
            if process["USER"] == user:
                i+=1
        text += str(i) +"\n"
    text += '\n'
    text += const.RAM_USED
    text += str(total_mem) + "%" + '\n'
    text += const.CPU_USED
    text += str(total_cpu) + "%" +'\n'
    text += const.MAX_RAM
    text += processes[0]["COMMAND"][:20] + '\n'
    text += const.MAX_CPU
    processes = get_processes("cpu")
    text += processes[0]["COMMAND"][:20] + '\n'

    print(text)
    filename = str(datetime.now()) +'.txt'
    with open(filename,"w") as file:
        print(text, file = file)