import paramiko
import Cred

def get_tagimplications():
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.load_system_host_keys()
        ssh_client.connect(Cred.hostname, Cred.port, Cred.username, Cred.password)

        stdin, stdout, stderr = ssh_client.exec_command("b4 tagimplications")

        tag_implication = []

        for line in stdout.readlines():
            line = line.strip()
            if line: 
                tag, implication = line.split(' -> ')
                tag_implication.append({"Tag": tag.strip(), "Tag_implication": implication.strip()})


        ssh_client.close()

        return(tag_implication)
    except paramiko.AuthenticationException as auth_exception:
        print("Authentication failed:", auth_exception)
        # Handle authentication error here
    except paramiko.SSHException as ssh_exception:
        print("SSH connection failed:", ssh_exception)
        # Handle SSH connection error here
    except Exception as e:
        print("An error occurred:", e)
        # Handle other exceptions here

    return []