from subprocess import (
    run, PIPE
)


if __name__ == '__main__':
    import subprocess

    result = subprocess.run(["get-process"], capture_output=True)
    #print(result.stdout.decode())
    print(result.stdout)
