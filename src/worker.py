from numpy import NaN
import requests
import os

from utils import getListApi

class FetchManager:
  __keyword__ = None
  __pageNum__ = NaN
  __artwork__ = None
  __proxy__ = None
  
  def __init__(self, keyword, pageNum, artwork):
    self.__keyword__ = keyword
    self.__pageNum__ = pageNum
    PROXY = os.environ.get("PROXY")
    if (PROXY):
      self.__proxy__ = {
        "http"  : PROXY, 
        "https" : PROXY, 
      }

  def getList(self):
    res = requests.get(getListApi(self.__artwork__, self.__keyword__), proxies=self.__proxy__)
    res = res.json()
    imageList = res["body"]["illustManga"]["data"]
    return map(lambda imageObj: {
      "title": imageObj["title"],
      "url": imageObj["url"]
    } ,imageList or [])