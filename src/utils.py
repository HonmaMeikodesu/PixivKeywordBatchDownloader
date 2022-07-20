import re
from const import PIXIV_AJAX_SEARCH_URL


def checkInputValid(keyword, pageNum):
  if (not len(keyword) or pageNum <= 0):
    raise Exception("Invalid input")

def getListApi(artwork, keyword, pageNum):
  return f"{PIXIV_AJAX_SEARCH_URL}/{artwork}?word={keyword}&pageNum={pageNum}"

def filterUnSuppportedFileName(fileName):
  return re.sub(r"[\/\\\*\?\<\>\|]", "", fileName)