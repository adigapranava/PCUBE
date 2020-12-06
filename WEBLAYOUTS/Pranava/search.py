from bs4 import BeautifulSoup
import urllib.request

urls = "https://www.youtube.com/results?search_query="
def search_url(content):
    cont = content.split(' ')
    urls = urls + cont[0]
    print(urls)
    url = urllib.request.urlopen()

search_url("hello hai")
