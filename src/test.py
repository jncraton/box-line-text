from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.actions.action_builder import ActionBuilder

import os
import difflib

options = webdriver.FirefoxOptions()
options.add_argument("--headless")

with webdriver.Firefox(options=options) as browser:
    browser.get(f'file://{os.getcwd()}/dist/index.html')

    def assert_contents():
        expected = '<section style="width: 126px; height: 190px; left: 62px; top: 62px;"><p contenteditable="true">Box</p></section><section style="width: 126px; left: 190px; top: 190px;"><p style="top: -66px;" contenteditable="true">Line</p></section><p style="left: 318px; top: 190px;" contenteditable="true">Text♥</p><section style="width: 126px; height: 126px; left: 510px; top: 190px;"><p contenteditable="true">Small Box</p></section><section style="width: 126px; left: 638px; top: 382px;" data-decoration="1"><p style="top: -66px;" contenteditable="true">Right</p><arrow class="right"></arrow></section><section style="width: 126px; height: 126px; left: 958px; top: 382px;" data-decoration="3"><p contenteditable="true">Has color</p></section>'
        content = browser.find_element(By.CSS_SELECTOR, 'body').get_attribute('innerHTML')
        content = content.strip().replace('<br>', '')
        content = content.replace(' contenteditable="true"', '')
        expected = expected.replace(' contenteditable="true"', '')
        if expected != content:
            for diff in difflib.ndiff(expected.replace('<', '\n<').splitlines(), content.replace('<', '\n<').splitlines()):
                print(diff)
            raise AssertionError

    def create_contents():
        action = ActionBuilder(browser)
        action.pointer_action.move_to_location(0, 0)
        action.perform()

        # Create a box
        webdriver.ActionChains(browser)\
            .move_by_offset(50, 50)\
            .click_and_hold()\
            .move_by_offset(150, 200)\
            .release()\
            .send_keys("Box")\
            .perform()
        assert('Box' in browser.page_source)

        # Create a line
        webdriver.ActionChains(browser)\
            .move_by_offset(0, -50)\
            .click_and_hold()\
            .move_by_offset(100, 0)\
            .release()\
            .send_keys("Line")\
            .perform()
        assert('Line' in browser.page_source)

        # Create text
        webdriver.ActionChains(browser)\
            .move_by_offset(0, 10)\
            .click_and_hold()\
            .release()\
            .send_keys("Text")\
            .perform()
        assert('Text' in browser.page_source)

        # Create heart
        webdriver.ActionChains(browser)\
            .send_keys("♥")\
            .perform()
        assert('♥' in browser.page_source)

        # Create a small box that grows automatically
        webdriver.ActionChains(browser)\
            .move_by_offset(200, 0)\
            .click_and_hold()\
            .move_by_offset(64, 64)\
            .release()\
            .send_keys("Small Box")\
            .perform()
        assert('Small Box' in browser.page_source)

        # Create a line with arrows
        webdriver.ActionChains(browser)\
            .move_by_offset(100, 100)\
            .click_and_hold()\
            .move_by_offset(100, 0)\
            .release()\
            .send_keys(Keys.RIGHT, "Right")\
            .perform()
        assert('Right' in browser.page_source)

        # Create a decorated box
        webdriver.ActionChains(browser)\
            .move_by_offset(200, 0)\
            .click_and_hold()\
            .move_by_offset(128, 128)\
            .release()\
            .send_keys(Keys.UP, "Has color")\
            .perform()
        assert('Has color' in browser.page_source)

        assert_contents()

    create_contents()

    # Delete all elements via Shift+click
    # We may need to run this multiple time to remove elements hidden behind others
    for _ in range(2):
        for e in browser.find_elements(By.CSS_SELECTOR, 'body>*'):
            webdriver.ActionChains(browser)\
                .key_down(Keys.SHIFT)\
                .click(e)\
                .key_up(Keys.SHIFT)\
                .perform()
    assert(browser.find_element(By.CSS_SELECTOR, 'body').get_attribute('innerHTML').strip() == '')

    create_contents()

    # Save the URL and browse to it
    doc_url = browser.current_url
    browser.close()
    browser = webdriver.Firefox(options=options)
    browser.get(doc_url)
    assert_contents()
    browser.close()
