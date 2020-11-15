from jnpr.junos import Device
from jnpr.junos.utils.start_shell import StartShell
from lxml import etree
import os
import filecmp
from shutil import copyfile

f = open("router.list")

if not os.path.isfile("result.log"):
    os.system("touch result.log")

copyfile("result.log", "result.log.old")
res = open("result.log", "w")

for router in f:
    router = router.replace("\n","")
    print("Checking Router: ", router)
    
    dev = Device(host=router, user='regress', password='MaRtInI', mode='telnet')
    dev.open()
    shell = StartShell(dev)
    shell.open()
    
    op = shell.run('cli -c "show system core-dumps | match root "')
    
    for line in op:
        if isinstance(line, str) and "root  wheel" in line:
            line = line.replace("%","")
            line = line[45:]
            res.write(router + ":" + line)
    dev.close()

res.close()

if os.stat("result.log").st_size and not filecmp.cmp("result.log", "result.log.old"):
    print("New Cores Generated")
    content = "cat result.log | mail -s 'Google Escalation - New Cores Found' hfzhang@juniper.net msanthanam@juniper.net harib@juniper.net bpchoi@juniper.net"
    #content = "cat result.log | mail -s 'Google Escalation - New Cores Found' hfzhang@juniper.net"
    res = os.system(content)
