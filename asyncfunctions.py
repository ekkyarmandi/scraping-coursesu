# import search_barcode as sb
import asyncio, aiohttp
from math import ceil

# ignore event loop policy warnings
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def batchers(files,batch_size=80):
    n = len(files)
    z = ceil(n/batch_size)
    x = [i*batch_size for i in range(z+1)]
    x[-1] = n
    return x, len(x)-1

def sec2hms(sec):
    m, s = divmod(sec, 60)
    if m <= 60:
        time_str = f"{int(m):02d}m {int(s):02d}s"
    elif m > 60:
        h, m = divmod(m, 60)
        time_str = f"{int(h):02d}h {int(m):02d}m"
    return time_str

# asynchronous functions
async def render(session, functions, url):
    loop = asyncio.get_event_loop()
    try:
        async with session.get(url) as r:
            result = await loop.run_in_executor(None, functions, url, await r.text())
            return result
    except:
        return None

async def gather(session, functions, urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(render(session, functions, url))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results

headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}
async def render_all(functions, urls):
    async with aiohttp.ClientSession(headers=headers) as session:
        data = await gather(session, functions, urls)
        return data