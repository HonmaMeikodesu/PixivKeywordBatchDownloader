from ast import keyword
import asyncio
from sys import stdout

from utils import checkInputValid
from fetchCompany import FetchManager, FetchWorker;

async def main(keyword, pageNum, artwork):
  manager = FetchManager(keyword, pageNum, artwork)
  imageList = await manager.getList();
  workerList = [FetchWorker(item["title"], item["url"]) for item in imageList]
  taskList = [asyncio.create_task(worker.fetchToLocal()) for worker in workerList]
  for task in taskList:
    await task


stdout.write("Input the keyword:\n")
keyword = input();
stdout.write("Input how many pages of pics you wish to fetch:\n")
pageNum = input();
stdout.write("(Optional) Input the artwork under which you wish to search,\ndefault to be as same as the keyword:\n")
artwork = input();

pageNum = int(pageNum);
artwork = artwork if len(artwork) else keyword;

checkInputValid(keyword, pageNum)

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main(keyword, pageNum, artwork))