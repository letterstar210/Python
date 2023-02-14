import paramiko
import datetime

def get_ssh_client(host, username, password):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=host, username=username, password=password)
    return ssh_client

def get_ram_usage(ssh_client):
    stdin, stdout, stderr = ssh_client.exec_command("free -m | awk '/Mem/ {print $3/$2 * 100.0}'")
    ram_usage = round(float(stdout.read().decode("utf-8").strip()), 2)
    return ram_usage

#def get_disk_usage(ssh_client, partitions):
#    disk_usage = []
#    for partition in partitions:
#        stdin, stdout, stderr = ssh_client.exec_command(f"df -h {partition}")
#        disk_info_output = stdout.read().decode("utf-8").strip().split("\n")
#        if len(disk_info_output) > 1:
#            disk_info = disk_info_output[1].split()
#            disk_usage.append(disk_info)
#    return disk_usage
def get_disk_usage(ssh_client, partitions):
    disk_usage = {}
    for partition in partitions:
        stdin, stdout, stderr = ssh_client.exec_command(f"df -h {partition}")
        disk_info = stdout.read().decode("utf-8").strip().split("\n")[1].split()
        if len(disk_info) < 5:
            print(f"Error: Unexpected output for partition {partition}")
            continue
        disk_usage[partition] = f"{disk_info[0]} ({disk_info[4]})"
    return disk_usage

def main():
    hosts = ['172.28.27.56','172.28.27.57','172.28.27.58','172.28.27.59','172.28.27.60','172.28.27.61','172.28.27.62','172.28.27.63','172.28.27.64','172.28.27.65','172.28.27.66','172.28.27.67','172.28.27.68','172.28.27.69','172.28.27.70','172.28.27.71','172.28.27.72','172.28.27.73','172.28.27.74','172.28.27.75','172.28.27.76','172.28.27.77','172.28.27.78','172.28.27.79','172.28.27.80','172.28.27.81','172.28.27.82','172.28.27.83','172.28.27.84','172.28.27.85','172.28.27.86','172.28.27.87','172.28.27.88','172.28.27.89','172.28.27.90','172.28.27.91','172.28.27.92','172.28.27.93','172.28.27.94','172.28.27.95','172.28.27.96','172.28.27.97','172.28.27.98','172.28.27.99','172.28.27.100']
    username = 'root'
    password = 'P@ssw0rd'
    partitions = ['/boot','/','/home']
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d")
    filename = f"results_{timestamp}.txt"
     
    results = []
    for host in hosts:
        ssh_client = get_ssh_client(host, username, password)
        ram_usage = get_ram_usage(ssh_client)
        disk_usage = get_disk_usage(ssh_client, partitions)
        results.append({'host': host, 'ram_usage': ram_usage, 'disk_usage': disk_usage})
        ssh_client.close()

    with open(filename, "w") as f:
        f.write("Host\tRAM Usage\tDisk Usage\n")
        for result in results:
            f.write(f"{result['host']}\t{result['ram_usage']}\t")
            for partition, usage in result['disk_usage'].items():
                f.write(f"{partition}: {usage}\t")
            f.write("\n")

if __name__ == '__main__':
    main()
    print("Code execution complete.")
