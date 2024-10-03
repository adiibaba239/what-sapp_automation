
import time

from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException

def click_element_with_retry(element, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            element.click()
            return True
        except ElementClickInterceptedException:
            retries += 1
            time.sleep(1)
    return False

    # Function to find an element with retries


def find_element_with_retry(driver, by, value, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            element = driver.find_element(by, value)
            return element
        except NoSuchElementException:
            retries += 1
            time.sleep(1)
    return None
