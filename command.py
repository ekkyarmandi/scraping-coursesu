from math import ceil
import os, json

from colorama import init, Fore, Style
init()

def green(text):
    print(Fore.GREEN + str(text) + Style.RESET_ALL)

def red(text):
    print(Fore.RED + str(text) + Style.RESET_ALL)

def yellow(text):
    print(Fore.YELLOW + str(text) + Style.RESET_ALL)

def batchers(files,batch_size=80):
    n = len(files)
    z = ceil(n/batch_size)
    x = [i*batch_size for i in range(z+1)]
    x[-1] = n
    return x

def merge(path,file_name):
    data = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith("json"):
                file_path = os.path.join(root,file)
                d = json.load(open(file_path))
                data.extend(d)                
    data = [d for d in data if d != None]
    file_path = os.path.join(path,file_name)
    json.dump(data,open(file_path,"w"))

def update():
    pass

if __name__ == "__main__":

    path = "./urls/"
    file_name = "product_urls.json"
    merge(path,file_name)