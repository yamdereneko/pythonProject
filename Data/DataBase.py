import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ChromeOptions


def main():
    path = '/Users/yandereneko/Downloads/chromedriver'
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('disable-gpu')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(executable_path=path, options=options)  # 相当于 driver =
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {'source': 'Object.defineProperty(navigator,'
                                                                               '"webdriver",{get:()=>undefind})'})
    comments = []
    comment = {}
    base_url = 'http://c.tieba.baidu.com/p/7780456938'
    driver.implicitly_wait(5)
    driver.get(base_url)
    comment["text"] = driver.find_elements_by_class_name('p_content')
    comment["author"] = driver.find_elements_by_class_name('d_name')
    comment["kick"] = driver.find_elements_by_class_name('post-tail-wrap')
    # comment["pid"] = driver.find_elements_by_class_name('d_post_content j_d_post_content ')
    comment["test"] = driver.find_elements_by_xpath('//*[@id="j_p_postlist"]/div[4]')
    # print(d_text)
    # print(d_author)
    # print(pid)
    comments.append(comment)
    for i in comment:
        print(1)
        # for text, author, kick,pid in zip(d_text, d_author, d_kick,d_pid):
        #     print(author.text)
        #     print(text.text)
        #     print(kick.text)
        #
        #     print("=" * 20)
    driver.quit()


if __name__ == '__main__':
    main()
