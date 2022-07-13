from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.safari.options import Options

options = Options()
options.add_argument('--headless')
options.add_argument('disable-gpu')
# base_url = 'https://tieba.baidu.com/p/7902566441'
driver = webdriver.Safari(options=options)
base_url = "https://jx3.seasunwbl.com/buyer"
driver.get(base_url)
driver.implicitly_wait(0.5)
text = driver.find_element(by=By.CLASS_NAME, value="p_content")
author = driver.find_element(by=By.CLASS_NAME, value='d_name')
print(author.text)
print(text.text)
driver.quit()