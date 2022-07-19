from numpy import NaN
import requests
import os

from utils import getListApi

class FetchStaff:
  __proxy__ = None

  def __init__(self):
    PROXY = os.environ.get("PROXY")
    if (PROXY):
      self.__proxy__ = {
        "http"  : PROXY, 
        "https" : PROXY, 
      }

class FetchManager(FetchStaff):
  __keyword__ = None
  __pageNum__ = NaN
  __artwork__ = None
  
  def __init__(self, keyword, pageNum, artwork):
    self.__keyword__ = keyword
    self.__pageNum__ = pageNum
    self.__artwork__ = artwork

  def getList(self):
    res = requests.get(getListApi(self.__artwork__, self.__keyword__), proxies=self.__proxy__)
    res = res.json()
    imageList = res["body"]["illustManga"]["data"]
    return map(lambda imageObj: {
      "title": imageObj["title"],
      "url": imageObj["url"]
    } ,imageList or [])


class FetchWorker(FetchStaff):
  __title__ = None
  __url__ = None

  def __init__(self, title, url):
    self.__title__ = title
    self.__url__ = url
    
  
  def fetchImageToLocal(self):
    res = requests.get(self.__url__, proxies=self.__proxy__)
