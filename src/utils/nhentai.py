from bs4 import BeautifulSoup
from selenium import webdriver

base_url = 'https://nhentai.net/api'
gallery_url = f'{base_url}/gallery'

options = webdriver.ChromeOptions()
options.add_argument('--disable-dev-shm-usage')
options.binary_location = '/root/chromedriver-linux64/chromedriver'

driver = webdriver.Chrome(options=options)

driver.get(f'{gallery_url}/177013')

bs = BeautifulSoup(driver.page_source,"lxml")

print(bs.text)
