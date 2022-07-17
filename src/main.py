from ast import keyword
from sys import stdout

from utils import checkInputValid
from worker import FetchManager;

def main(keyword, pageNum, artwork):
  print(artwork);
  print(keyword);
  print(pageNum);
  manager = FetchManager(keyword, pageNum, artwork)


stdout.write("Input the keyword:\n")
keyword = input();
stdout.write("Input how many pages of pics you wish to fetch:\n")
pageNum = input();
stdout.write("(Optional) Input the artwork under which you wish to search,\ndefault to be as same as the keyword:\n")
artwork = input();

pageNum = int(pageNum);
artwork = artwork if len(artwork) else keyword;

checkInputValid(keyword, pageNum)

main(keyword, pageNum, artwork)