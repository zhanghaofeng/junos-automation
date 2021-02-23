#!/usr/bin/python3

import subprocess
import time
from influxdb import InfluxDBClient
from datetime import datetime

# Global Variables
server = "1.1.1.1"
count = 1
wait_sec = 10

user = "influx"
password = "influx"
dbname = "latency"
host = "localhost"
port = 8086

client = InfluxDBClient(host, port, user, password, dbname)
#client.drop_database(dbname)
client.create_database(dbname)

def ping(server=server, count=1, wait_sec=10):

    json_point = []

    while True:
        cmd = "ping -c {} -W {} {}".format(count, wait_sec, server).split(' ')
        try:
            date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            output = subprocess.check_output(cmd).decode().strip()
            lines = output.split("\n")
            total = lines[-2].split(',')[3].split()[1]
            loss = lines[-2].split(',')[2].split()[0]
            timing = lines[-1].split()[3].split('/')
            average = timing[1]

            json_point.append(
                {
                    "measurement": "latency",
                    '''
                    "tags": {
                        "county": county,
                    },
                    '''
                    "time": date,
                    "fields": {
                        "latency": average,
                        "loss": loss,
                        "date": date,
                    }
                }
            )

            if len(json_point) >=1:
                client.write_points(json_point)
                #print "Write database %s datapoints" % (len(json_point))
                json_point = []

            time.sleep(1)
            '''
            return {
                'type': 'rtt',
                'min': timing[0],
                'avg': timing[1],
                'max': timing[2],
                'mdev': timing[3],
                'total': total,
                'loss': loss,
            }
            '''
        except KeyboardInterrupt:
            client.write_points(json_point)
            return None
        except Exception as e:
            print(e)
            client.write_points(json_point)
    
if __name__ == "__main__":
    ping(server, count, wait_sec)
