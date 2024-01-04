import re
import paramiko
import Cred

def get_candidates():
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.load_system_host_keys()
        ssh_client.connect(Cred.hostname, Cred.port, Cred.username, Cred.password)

        stdin, stdout, stderr = ssh_client.exec_command("b4 candidates --severity 3")
        lines = stdout.read().decode('utf-8', errors='replace')

        candidate_pattern = r"BUG(\d+)(?: \( bugalert owner: ([^\)]+)\,)?(?: assigned ([^\)]+)\))?\n(?:description: ([^\n]+(?:\n\s+[^\n]+)*))?\nseverity: ([^\n]+)(?:\nCVE: (.*?))?\nproduct: ([^\n]+)\nversions introduced: (.*?)\nversions fixed: (.*?)\nbites: (\d+)\nSR case numbers: ([^\n]+)(?:\nlast bite time: ([^\n]+))?\nfixes: ([^\n]+)(?:\nlast fix time: ([^\n]+))?\nrelease note: ([\S\s]*?)\n\n"

        matches = re.findall(candidate_pattern, lines, re.MULTILINE | re.DOTALL,)

        candidate_list = []
        for match in matches:
            candidate_data = {
            "id": match[0],
            "bugalertOwner": match[1] if match[1] else "",
            "assignedOn": match[2] if match[2] else "",
            "description": ' '.join(match[3].split()),
            "severity": match[4],
            "CVE": match[5] if match[5] else "",
            "product": match[6],
            "versionsIntroduced": match[7],
            "versionFixed": match[8],
            "bites": match[9],
            "srCaseNumbers": match[10],
            "lastBiteTime": match[11] if match[11] else "",
            "fixes": match[12],
            "lastFixTime": match[13] if match[13] else "",
            "releaseNote": ' '.join(match[14].split())
            }
            candidate_list.append(candidate_data)

        ssh_client.close()

        return(candidate_list) 

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

def get_one_candidates(bug_id):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.load_system_host_keys()
        ssh_client.connect(Cred.hostname, Cred.port, Cred.username, Cred.password)

        stdin, stdout, stderr = ssh_client.exec_command("b4 candidates "+ str(bug_id) +" --severity 3")
        lines = stdout.read().decode('utf-8', errors='replace')
        
        candidate_pattern = r"BUG(\d+)(?: \( bugalert owner: ([^\)]+)\,)?(?: assigned ([^\)]+)\))?\n(?:description: ([^\n]+(?:\n\s+[^\n]+)*))?\nseverity: ([^\n]+)(?:\nCVE: (.*?))?\nproduct: ([^\n]+)\nversions introduced: (.*?)\nversions fixed: (.*?)\nbites: (\d+)\nSR case numbers: ([^\n]+)(?:\nlast bite time: ([^\n]+))?\nfixes: ([^\n]+)(?:\nlast fix time: ([^\n]+))?\nrelease note: ([\S\s]*?)\n\n"

        matches = re.findall(candidate_pattern, lines, re.MULTILINE | re.DOTALL,)

        candidate_list = []
        for match in matches:
            candidate_data = {
            "id": match[0],
            "bugalertOwner": match[1] if match[1] else "",
            "assignedOn": match[2] if match[2] else "",
            "description": ' '.join(match[3].split()),
            "severity": match[4],
            "CVE": match[5] if match[5] else "",
            "product": match[6],
            "versionsIntroduced": match[7],
            "versionFixed": match[8],
            "bites": match[9],
            "srCaseNumbers": match[10],
            "lastBiteTime": match[11] if match[11] else "",
            "fixes": match[12],
            "lastFixTime": match[13] if match[13] else "",
            "releaseNote": ' '.join(match[14].split())
            }
            candidate_list.append(candidate_data)

        ssh_client.close()

        return(candidate_list) 

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