from weakref import proxy
from numpy import NaN
from aiohttp import ClientSession
import os
from const import PIXIV_HOST

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

  async def getList(self):
    async with ClientSession() as session:
      async with session.get(getListApi(self.__artwork__, self.__keyword__), proxy=self.__proxy__) as res:
        res = await res.json();
        imageList = res["body"]["illustManga"]["data"]
        imageList = list(filter(lambda imageObj: imageObj.get("title") and imageObj.get("url"), imageList))
        return list(map(lambda imageObj: {
          "title": imageObj["title"],
          "url": imageObj["url"]
        } ,imageList or []))


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
          with open(os.path.join(".", "tmp", f"{filterUnSuppportedFileName(self.__title__)}.jpg"), "wb") as fd:
            while True:
              chunk = await res.content.read()
              if not chunk:
                  break
              fd.write(chunk)
