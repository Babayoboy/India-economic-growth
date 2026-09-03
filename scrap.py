import requests
from bs4 import BeautifulSoup

url = "https://www.macrotrends.net/global-metrics/countries/ind/india/gdp-gross-domestic-product"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
