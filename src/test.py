from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

import os

options = Options()
options.headless = True

with webdriver.Firefox(options=options) as browser:
    browser.get(f'file://{os.getcwd()}/dist/index.html')

    webdriver.ActionChains(browser)\
        .move_by_offset(50, 50)\
        .click_and_hold()\
        .move_by_offset(150, 200)\
        .release()\
        .send_keys("Box")\
        .perform()

    assert('Box' in browser.page_source)

    webdriver.ActionChains(browser)\
        .move_by_offset(0, -50)\
        .click_and_hold()\
        .move_by_offset(100, 0)\
        .release()\
        .send_keys("Line")\
        .perform()

    assert('Line' in browser.page_source)

    webdriver.ActionChains(browser)\
        .move_by_offset(0, 10)\
        .click_and_hold()\
        .release()\
        .send_keys("Text")\
        .perform()

    assert('Text' in browser.page_source)

    assert(browser.find_element_by_css_selector('body').get_attribute('innerHTML').strip() == '<section style="width: 126px; height: 190px; left: 62px; top: 62px;"><p contenteditable="true">Box</p></section><section style="width: 126px; left: 190px; top: 190px;"><p style="top: -66px;" contenteditable="true">Line</p></section><p style="left: 318px; top: 190px;" contenteditable="true">Text</p>')
