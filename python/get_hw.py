import yaml
import os, sys, logging
import datetime
import shutil
import paramiko
from scp import SCPClient

from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from lxml import etree 
from jnpr.junos.utils.start_shell import StartShell


timeout = 300

def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client

def get_hardware(host):
    
    dev = Device(host=host, user="regress", passwd="MaRtInI", port=22)
    
    try:
        ss = StartShell(dev)
    except Exception as err:
        logging.error('Cannot connect to device: {0}\n'.format(err))
        return       
         
    try:
        ss.open()
    except Exception as err:
        logging.error('Cannot open to device: {0}\n'.format(err))
        return

    cli_conf  = 'cli -c "show configuration | save /var/tmp/"' + host + '.conf'
    cli_hw = 'cli -c "show chassis hardware | save /var/tmp/"' + host + '.hw'
    ss.run(cli_conf)
    ss.run(cli_hw)
    ss.close()
    
    remote_conf = '/var/tmp/' + host + '.conf'
    remote_hw = '/var/tmp/' + host + '.hw'
    
    ssh = createSSHClient(host, 22, "regress", "MaRtInI")
    scp = SCPClient(ssh.get_transport())
    
    scp.get(remote_conf)
    scp.get(remote_hw)
    
    '''
    hw = dev.rpc.get_chassis_inventory({'format':'text'}, dev_timeout=120)
    hw_filename = "hw_" + host
    file = open(hw_filename, "w")
    file.write(etree.tostring(hw))
    file.close()
    
    
    try:
        #config = dev.rpc.get_config(dev_timeout=timeout, options={'format':'set'})
        config = dev.rpc.get_config(dev_timeout=timeout)
    except Exception as err:
        logging.error('Get config error {0}\n'.format(err))
        return
        
    config_filename = "config_" + host
    file = open(config_filename, "w")
    file.write(etree.tostring(config, encoding='unicode', pretty_print=True))
    file.close()
    '''
    # End the NETCONF session and close the connection
    dev.close()

def main():
    
    #Create a directory with current date time, 2019-09-11-13
    dt = datetime.datetime.now()
    dt2 = dt.strftime('%Y-%m-%d-%H')

    if os.path.isdir(dt2):
        shutil.rmtree(dt2)    
    os.mkdir(dt2)
    
    f = open('hosts.yaml', 'r')
    host_name = f.read().splitlines()

    os.chdir(dt2)
    for host in host_name:
        host = host.strip()
        print "host info:%s" % host
        get_hardware(host)

if __name__ == "__main__":
    main()