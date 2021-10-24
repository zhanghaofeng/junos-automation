import yaml

try:
    with open("cmis.yaml") as f:
        dic = dict(yaml.safe_load(f))
        for k in dic.keys():
            print(type(k))
        


except Exception as error:
    print("Error reported:", error)