
filename = 'routerlist'

# Input filename
# Output DS:
# {
#     'region1': {'role1':[name1,name2], 'role2':[name1,name2]...},
#     'region2': {'role1':[name1,name2], 'role2':[name1,name2]...}
# }

def parse_file():
    with open(filename) as f:
        lines = f.readlines()

    res = {}

    for line in lines:
        try:
            line = line.strip()
            region = line.split("_")[0]
            role = line.split("_")[1]
            routername = line.split("_")[2]
        except Exception as e:
            print(f"Error to deal with line: '{line}'. Error is '{e}'")
            continue
        
        if region in res.keys():
            if role in res[region].keys():
                res[region][role].append(routername)
            else:
                res[region][role] = [routername]
        else:
            res[region] = {role:[routername]}

    yield res

if __name__ == "__main__":
    result = parse_file()
    res = {}
    for i in result:
        print(i)

    print(f"No. of regions: {len(res)}.")
    for region,layer in res.items():
        print(f"\tRegion {region}, No. of Routers: {len(layer)}")
        for k,v in layer.items():
            print(f"\t\tRegion: {region}, Layer: {k}, No. router: {len(v)}")