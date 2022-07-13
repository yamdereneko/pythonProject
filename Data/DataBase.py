from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


def Datas():
    service = Service(executable_path="/Users/yandereneko/Downloads/chromedriver")
    options = Options()
    options.add_argument('--headless')
    options.add_argument('disable-gpu')

    driver = webdriver.Chrome(service=service,options=options)
    comments = []
    comment = {}
    base_url = 'https://jx3.seasunwbl.com/buyer'
    driver.get(base_url)
    content = driver.find_elements(by=By.CLASS_NAME, value="app-web-components-bordered-item-index-m__borderedItem--1qEaG")
    driver.find_element(by=By.XPATH, value="//*[@id='app']/div/div[3]/div/div[2]/div[1]/div[2]/div/div[2]").click()
    driver.find_element(by=By.XPATH, value="//*[@id='app']/div/div[3]/div/div[2]/div[2]/div[2]/div/div[2]").click()
    price = driver.find_element(by=By.XPATH, value="//*[@id='app']/div/div[3]/div/div[3]")
    print(price.text)
    # comment["author"] = driver.find_elements_by_class_name('d_name')
    # comment["kick"] = driver.find_elements_by_class_name('post-tail-wrap')
    # comment["pid"] = driver.find_elements_by_class_name('d_post_content j_d_post_content ')
    # comment["test"] = driver.find_elements_by_xpath('//*[@id="j_p_postlist"]/div[4]')
    # print(content)

    driver.quit()


if __name__ == '__main__':
    Datas()
