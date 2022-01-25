# import libraries
from logging import root
import asyncfunctions as af
import command as printer
import time, json, os
import numpy as np
import requests
import asyncio
import logic
import sys

def manual(index,urls):
    for i, url in zip(index,urls):
        try:
            req = requests.get(url,headers=logic.headers)
            result = logic.scraper(url,req.content)
            if result != None:
                dest_file = root + f"{i:06d}.json"
                if not os.path.exists(dest_file):
                    json.dump(result,open(dest_file,"w"))
        except: pass

# get the start input
try: st = int(sys.argv[1])
except: st = 0

# clear the terminal
os.system("cls")
beginning = time.time()
print("program start..")

# prepare the destionation folder
root = "./data/"
speed = []

# read all the product urls
urls = json.load(open("./urls/product_urls.json"))
scraped = json.load(open("./urls/scraped_urls.json"))
urls = list(dict.fromkeys(urls))

# iterate the scraping process in batches
index = list(range(0,len(urls)))

# filter the scraped urls
for i in scraped:
    urls.remove(scraped[i])
    index.remove(int(i))

x, R = af.batchers(urls,80)
print(f"{len(urls)} data will be devided into {R} batch")
for r in range(st,R):
    print(f">> batch{r:04d}", end=" ")
    try:
        start = time.time()
        a, b = x[r], x[r+1]
        results = asyncio.run(af.render_all(logic.scraper,urls[a:b]))
        for i, result in zip(index[a:b],results):
            if result != None:
                dest_file = root + f"{i:06d}.json"
                if not os.path.exists(dest_file):
                    json.dump(result,open(dest_file,"w"))
        # manual(index[a:b],urls[a:b])
        end = time.time()
        speed.append(time.time()-start)
        est = af.sec2hms(int(np.mean(speed)*(R-r)))
        printer.green(f"{end-start:.2f} sec (est. {est} left)")
    except:
        printer.red("failed")

# end statement
end = time.time()
time_str = f"{af.sec2hms(end-beginning)}"
printer.yellow("done in " + time_str)