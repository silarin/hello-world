# primarily for windows, checks the user for the running process, the environment it is run in, and execute a file.
import gc
import getpass
import os
import socket
import subprocess


def main():
    if getpass.getuser() != '@ALLOWED_USER@':
        print('This script must be executed by the user @ALLOWED_USER@.')
        exit()

    try:
        ipaddr = socket.gethostbyname(socket.gethostname())

        if ipaddr == '192.168.1.1':
            svrname = '@SERVER_NAME@'
            dbname = '@DB_NAME@'
        elif ipaddr == '192.168.1.2':
            svrname = '@SERVER_NAME@'
            dbname = '@DB_NAME@'
        else:
            print('This script should be executed on the @ENVIRONMENT@ server.')
            exit()

    except Exception as e:
        print('Unable to get host ip address.\r\n' + str(e))
        exit()

    execf = r'@PATH_TO_FILE@'

    if os.path.exists(execf):
        cmd = execf + ' @OPT_ARG_FOR_PROCESS@
        try:
            print(cmd)
            subprocess.call(cmd)

        except Exception as e:
            print('EXEC failed: ' + cmd + '\r\n' + str(e))
            exit()

        finally:
            gc.collect()
    else:
        print('Unable to locate path: ' + execf)
        exit()


if __name__ == '__main__':
    main()
