import uuid
from numpy import NaN
from aiohttp import ClientSession
import os
from const import PIXIV_HOST
import asyncio

from utils import filterUnSuppportedFileName, getListApi

class FetchStaff:
  __proxy__ = os.environ.get("PROXY")
class FetchManager(FetchStaff):
  __keyword__ = None
  __pageNum__ = NaN
  __artwork__ = None
  
  def __init__(self, keyword, pageNum, artwork):
    self.__keyword__ = keyword
    self.__pageNum__ = pageNum
    self.__artwork__ = artwork

  async def lead(self):
    taskList = []
    for currentPageNum in range(1, 1 + self.__pageNum__):
    # TODO 协程过多是否会导致event loop塞不下？对下面代码进行troubleshooting
    # TODO throttling是否必要？
    # taskList.append(asyncio.create_task(self.hireWorkerForCurrentPage(currentPageNum)))
    # await asyncio.gather(*taskList)
      # 分批下载，一批下载一页
      await self.hireWorkerForCurrentPage(currentPageNum)

  
  async def hireWorkerForCurrentPage(self, currentPage):
    async with ClientSession() as session:
      async with session.get(getListApi(self.__artwork__, self.__keyword__, currentPage), proxy=self.__proxy__) as res:
        res = await res.json();
        imageList = res["body"]["illustManga"]["data"]
        imageList = list(filter(lambda imageObj: imageObj.get("title") and imageObj.get("url"), imageList))
        imageList = list(map(lambda imageObj: {
          "title": imageObj["title"],
          "url": imageObj["url"]
        } ,imageList or []))
        await self.arrangeWorkers(imageList)

  async def arrangeWorkers(self, currentPageImageList):
      workerList = [FetchWorker(item["title"], item["url"]) for item in currentPageImageList]
      taskList = [asyncio.create_task(worker.fetchToLocal()) for worker in workerList]
      await asyncio.gather(*taskList)

class FetchWorker(FetchStaff):
  __title__ = None
  __url__ = None

  def __init__(self, title, url):
    self.__title__ = title
    self.__url__ = url

  async def fetchToLocal(self):
    async with ClientSession() as session:
      headers = {'referer': f'{PIXIV_HOST}'}
      async with session.get(self.__url__, headers=headers, proxy=self.__proxy__) as res:
        try:
          os.mkdir("tmp")
        except FileExistsError:
          pass
        finally:
          with open(os.path.join(".", "tmp", f"{filterUnSuppportedFileName(self.__title__)}_{str(uuid.uuid4())}.jpg"), "wb") as fd:
            while True:
              chunk = await res.content.read()
              if not chunk:
                  break
              fd.write(chunk)
