from netmiko import ConnectHandler
import datetime, os, shutil
import threading
from multiprocessing.dummy import Pool as ThreadPool

Host_File = 'hosts.yaml'
Threads_Limits = 100

def getdata_worker(device_params):

    device = device_params[0]
    dt = device_params[1]
    
    print("Connecting to Device: ", device)
    hostname = device
    jnpr_device = {
        'device_type': 'juniper',
        'ip': hostname,
        'username': 'regress',
        'password': 'MaRtInI'
    }

    host_config_file = dt + "/" + device + ".config"
    host_hw_file = dt + "/" + device + ".hw"

    try:
        Net_handle = ConnectHandler(**jnpr_device)
    except Exception as unknown_error:
        print("Connection Error to ", device)
    
    try:
        output_config = Net_handle.send_command("show configuration | no-more")
        output_hw = Net_handle.send_command("show chassis hardware | no-more")

        with open(host_config_file, "w") as f:
            f.write(output_config)
        with open(host_hw_file, "w") as f:
            f.write(output_hw)
    except Exception as unknown_error:
        print("Get data Error from:", device)

def main():
    
    starting_time = datetime.datetime.now()
    
    #Create a directory with current date time, 2019-09-11-13
    dt = datetime.datetime.now().strftime('%Y-%m-%d-%H')
    if os.path.isdir(dt):
        shutil.rmtree(dt)
    os.mkdir(dt)

    with open(Host_File) as f:
        device_list = f.read().splitlines()

    device_params = []
    for device in device_list:
        device_params.append((device, dt))

    threads = ThreadPool( Threads_Limits )
    threads_map_results = threads.map( getdata_worker, device_params )

    threads.close()
    threads.join()

    '''
    # Create thread_list for all devices
    threads_list = []

    for device in device_list:
        threads_list.append( threading.Thread( target = getdata_worker, args = (device, dt)) )

    for work_threads in threads_list:
        work_threads.start()
    
    for work_threads in threads_list:
        work_threads.join()
    '''

    end_time = datetime.datetime.now()
    
    print("Script Execution time: ", end_time- starting_time)

if __name__ == "__main__":
    main()
