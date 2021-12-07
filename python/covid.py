import urllib.request, json
from datetime import datetime
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# Constants
url = 'https://data.sccgov.org/resource/t8ae-ku7k.json'
token = "ZMK70VfGla8vOs8svh_vLmomld_B71lOP36jn9AH1pmq5HmVMpRNSnwyiCiINCwWEd6xj7qBOmRdXYd4QlmxXg=="
org = "hfzhang.cn@gmail.com"
bucket = "hfzhang.cn's Bucket"


response = urllib.request.urlopen(url)
data = json.load(response)
json_point = list()

for sets in data:
    try:
        city = sets['city']
        population = int(sets['population'])
        date = sets['end_date'].split('T')[0] + 'T23:59:59Z'
        cases = int(sets['case_count'])
        json_point.append(
            {
                'measurement': 'covid',
                'tags': {
                    'city': city
                },
                'time': date,
                'fields': {
                    'city': city,
                    'population': population,
                    'date': date,
                    'cases': cases
                }
            }
        )
    except Exception as error:
        pass
with InfluxDBClient(url="https://us-west-2-1.aws.cloud2.influxdata.com", token=token, org=org) as client:
    write_api = client.write_api(write_options=SYNCHRONOUS)
    response = write_api.write(bucket, org, json_point)
    print(json_point)

client.close()

