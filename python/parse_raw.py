import sys,re
import time
from multiprocessing.dummy import Pool as ThreadPool

def parsedataWorker(data):
    start_time = time.time()
    res = parse_raw(data)
    print(f"Time spent: {(time.time() - start_time)} seconds")
    result1 = data+".csv"
    f = open(result1, "w")
    for k,v in res.items():
        f.write(k + ";" + ";".join(v) + "\n")
    f.close()
    return res

def parse_raw(input):
    pathDict = dict()
    with open(input) as f:
        line = f.readline()
        prefix, path, value = '', '', ''

        while line:
            try:
                if 'system_id: ' in line:
                    prefix, path, value = '', '', ''
                    line = f.readline()
                    continue
                
                if 'key: __prefix__' in line:
                    line = f.readline()
                    prefix = line.split('value: ')[-1].strip()
                    continue

                if 'key: ' in line:
                    key = line.split()[-1].strip()
                    path_raw = prefix + key
                    patter1 = re.compile('\[name=.*?\]')
                    path = patter1.sub('[name=xxx]', path_raw, count = 1)
                    #path = re.sub(r"\[neighbor-address=.*?\]", '', path)
                    pattern2 = re.compile("'.*?'")
                    path = pattern2.sub('xxx', path)
                    #path = re.sub(r"tunnel\[name=.*?\]", 'tunnel', path)
                    #path = re.sub(r"path\[name=.*?\]", 'path', path)
                    #path = re.sub(r"interface\[name=.*?\]", 'interface', path)

                    value_raw = f.readline().strip()

                    if re.match(r'\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}', value_raw):
                        # if 'value: ' in value_raw:
                        value = value_raw.split()[2]
                        # else:
                        #     value = value_raw.split()[-2]
                    else:
                        # if 'value: ' in value_raw:
                        value = value_raw.split()[0]
                        # else:
                        #     value = value_raw.split()[-2]

            except Exception as error:
                print(f'Error pase the line {line}, with error {error}')

            line = f.readline()

            if not path: continue

            if path not in pathDict:
                pathDict[path] = {value}
            elif value not in pathDict[path]:
                pathDict[path].add(value)
    return pathDict

if __name__ == '__main__':

    input_files = [sys.argv[1], sys.argv[2]]
    threads = ThreadPool()
    threads_map_results = threads.map( parsedataWorker, input_files)

    threads.close()
    threads.join()

    file1 = threads_map_results[0]
    file2 = threads_map_results[1]

    print(f'Error Data type between {sys.argv[1]} and {sys.argv[2]}')
    for k,v in file1.items():
        if k in file2.keys() and v == file2[k]:
            continue
        elif k in file2.keys() and v != file2[k]:
            print(f'\tData Type Error for path {k}. {sys.argv[1]}: {file1[k]}; {sys.argv[2]}: {file2[k]}')

    print(f'Unique Path in {sys.argv[1]}')
    for k,v in file1.items():
        if k not in file2.keys():
            print(f'\t {k}, {v}')

    print(f'Unique Path in {sys.argv[2]}')
    for k,v in file2.items():
        if k not in file1.keys():
            print(f'\t {k}, {v}')
