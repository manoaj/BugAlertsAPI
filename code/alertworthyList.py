import re
import paramiko
import Cred

def get_alertworthies():
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.load_system_host_keys()
        ssh_client.connect(Cred.hostname, Cred.port, Cred.username, Cred.password)

        stdin, stdout, stderr = ssh_client.exec_command("b4 alertworthies")
        lines = stdout.read().decode('utf-8', errors='replace')

        alert_pattern = r"BUG(\d+)(?: \(bugalert owner: ([^\)]+)\))?(?: \(added: ([^\)]+)\))?\n(?:description: ([^\n]+(?:\n\s+[^\n]+)*))?\nseverity: ([^\n]+)\nproduct: ([^\n]+)\nversions introduced: (\[.*?\])\nversions fixed: (\[.*?\])(?:\nCVEs: (\[.*?\]))?\nbites: (\d+)\nSR case numbers: ([^\n]+)(?:\nlast bite time: ([^\n]+))?\nrule: ([^\n]+)\n(?:alert summary: ([^\n]+(?:\n\s+[^\n]+)*))?\n(?:release note: ([^\n]+(?:\n\s+[^\n]+)*))?\nsupported: ([\S\s]*?)\n\n"

        matches = re.findall(alert_pattern, lines, re.MULTILINE | re.DOTALL,)

        alert_list = []
        for match in matches:
            alert_data = {
            "id": match[0],
            "bugalertOwner": match[1] if match[1] else "",
            "added": match[2] if match[2] else "",
            "description": ' '.join(match[3].split()), #' '.join(release_note.split())
            "severity": match[4],
            "product": match[5],
            "versionsIntroduced": match[6],
            "versionFixed": match[7],
            "CVE":match[8] if match[8] else "",
            "bites": match[9],
            "srCaseNumbers": match[10],
            "lastBiteTime": match[11] if match[11] else "",
            "rule": match[12],
            "alertSummary": ' '.join(match[13].split()),
            "releaseNote": ' '.join(match[14].split()),
            "supported": ' '.join(match[15].split())
            }
            alert_list.append(alert_data)
            
        ssh_client.close()

        return(alert_list)
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


def get_one_alertworthies(bug_id):
    try:
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.load_system_host_keys()
        ssh_client.connect(Cred.hostname, Cred.port, Cred.username, Cred.password)

        stdin, stdout, stderr = ssh_client.exec_command("b4 alertworthies "+ str(bug_id))
        lines = stdout.read().decode('utf-8', errors='replace')

        alert_pattern = r"BUG(\d+)(?: \(bugalert owner: ([^\)]+)\))?(?: \(added: ([^\)]+)\))?\n(?:description: ([^\n]+(?:\n\s+[^\n]+)*))?\nseverity: ([^\n]+)\nproduct: ([^\n]+)\nversions introduced: (\[.*?\])\nversions fixed: (\[.*?\])(?:\nCVEs: (\[.*?\]))?\nbites: (\d+)\nSR case numbers: ([^\n]+)(?:\nlast bite time: ([^\n]+))?\nrule: ([^\n]+)\n(?:alert summary: ([^\n]+(?:\n\s+[^\n]+)*))?\n(?:release note: ([^\n]+(?:\n\s+[^\n]+)*))?\nsupported: ([\S\s]*?)\n\n"

        matches = re.findall(alert_pattern, lines, re.MULTILINE | re.DOTALL,)

        alert_list = []
        for match in matches:
            alert_data = {
            "id": match[0],
            "bugalertOwner": match[1] if match[1] else "",
            "added": match[2] if match[2] else "",
            "description": ' '.join(match[3].split()), #' '.join(release_note.split())
            "severity": match[4],
            "product": match[5],
            "versionsIntroduced": match[6],
            "versionFixed": match[7],
            "CVE":match[8] if match[8] else "",
            "bites": match[9],
            "srCaseNumbers": match[10],
            "lastBiteTime": match[11] if match[11] else "",
            "rule": match[12],
            "alertSummary": ' '.join(match[13].split()),
            "releaseNote": ' '.join(match[14].split()),
            "supported": ' '.join(match[15].split())
            }
            alert_list.append(alert_data)
            
        ssh_client.close()

        return(alert_list)

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
