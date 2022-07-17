from const import PIXIV_AJAX_SEARCH_URL


def checkInputValid(keyword, pageNum):
  if (not len(keyword) or pageNum <= 0):
    raise Exception("Invalid input")

def getListApi(artwork, keyword):
  return f"{PIXIV_AJAX_SEARCH_URL}/{artwork}?word={keyword}"