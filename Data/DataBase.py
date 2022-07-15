from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def Datas():
    try:
        service = Service(executable_path="/Users/yandereneko/Downloads/chromedriver")

        options = Options()
        options.add_argument('--headless')
        options.add_argument('disable-gpu')

        driver = webdriver.Chrome(service=service, options=options)
        return driver
    except:
        print("Drive获取失败")