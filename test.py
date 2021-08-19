from time import sleep

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture
def browser():
    chrome_driver = webdriver.Chrome("./chromedriver.exe")
    chrome_driver.implicitly_wait(10)
    yield chrome_driver
    chrome_driver.quit()


# Test case 1
def test_contact_page_for_mandatory_email_field(browser):
    # Loads the target page url
    browser.get('http://jupiter.cloud.planittesting.com')
    browser.maximize_window()

    # Navigates to contact page and clicks on submit
    browser.find_element_by_id("nav-contact").click()
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Submit")))
    browser.find_element_by_link_text("Submit").click()

    # Checks for validation error message
    sleep(2)
    assert "but we won't get it unless you complete the form correctly" in browser.page_source

    # test mandatory email field
    browser.find_element_by_id("forename").send_keys("John")
    browser.find_element_by_id("message").send_keys(
        "Hey, I want to contact you, Please reach out to me on email")
    assert len(browser.find_elements_by_id("email-err")) == 1
    assert "but we won't get it unless you complete the form correctly" in browser.page_source


def test_contact_page_for_mandatory_message_field(browser):
    # Loads the target page url
    browser.get('http://jupiter.cloud.planittesting.com')
    browser.maximize_window()

    # Navigates to contact page and clicks on submit
    browser.find_element_by_id("nav-contact").click()
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Submit")))
    browser.find_element_by_link_text("Submit").click()

    # Populates forename and email fields but not message field and validates for the error message
    browser.find_element_by_id("forename").send_keys("John")
    browser.find_element_by_id("email").send_keys("John.example@gmail.com")
    assert "but we won't get it unless you complete the form correctly" in browser.page_source


def test_contact_page_for_mandatory_forename_field(browser):
    # Loads the target page url
    browser.get('http://jupiter.cloud.planittesting.com')
    browser.maximize_window()

    # Navigates to contact page and clicks on submit
    browser.find_element_by_id("nav-contact").click()
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Submit")))
    browser.find_element_by_link_text("Submit").click()

    # Populates email and message fields but not forename field and validates for the error message
    browser.find_element_by_id("email").send_keys("John.example@gmail.com")
    browser.find_element_by_id("message").send_keys(
        "Hey, I want to contact you, Please reach out to me on email")
    assert "but we won't get it unless you complete the form correctly" in browser.page_source


def test_contact_page_for_mandatory_fields(browser):
    # Loads the target page url
    browser.get('http://jupiter.cloud.planittesting.com')
    browser.maximize_window()

    # Navigates to contact page and clicks on submit
    browser.find_element_by_id("nav-contact").click()
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((By.LINK_TEXT, "Submit")))
    browser.find_element_by_link_text("Submit").click()

    # Populates all fields and verifies that there is no error message
    browser.find_element_by_id("email").send_keys("John.example@gmail.com")
    browser.find_element_by_id("forename").send_keys("John")
    browser.find_element_by_id("message").send_keys(
        "Hey, I want to contact you, Please reach out to me on email")
    assert "but we won't get it unless you complete the form correctly" not in browser.page_source


# Test case 2

def test_contact_page_successful_submission(browser):
    # Loads the target page url
    browser.get('http://jupiter.cloud.planittesting.com')
    browser.maximize_window()

    # Navigates to contact page
    browser.find_element_by_id("nav-contact").click()

    # Populates all fields, clicks on Submit
    browser.find_element_by_id("forename").send_keys("John")
    browser.find_element_by_id("email").send_keys("John.example@gmail.com")
    browser.find_element_by_id("message").send_keys(
        "Hey, I want to contact you, Please reach out to me on email")
    browser.find_element_by_link_text("Submit").click()

    # validates for the success message
    sleep(7)
    assert "Thanks John" in browser.page_source

# Test case 3


def test_contact_page_with_invalid_email_data(browser):
    # Loads the target page url
    browser.get('http://jupiter.cloud.planittesting.com')
    browser.maximize_window()

    # Navigates to contact page
    browser.find_element_by_id("nav-contact").click()

    # Populates email field with invalid email and verifies for the error message.
    browser.find_element_by_id("email").send_keys("John.example")
    sleep(2)
    assert "Please enter a valid email" in browser.page_source

    # Populates email field with empty email and verifies for the error message.
    browser.find_element_by_id("email").clear()
    browser.find_element_by_id("email").send_keys("")
    sleep(2)
    assert "Please enter a valid email" in browser.page_source


def test_contact_page_with_invalid_telephone_data(browser):
    # Loads the target page url
    browser.get('http://jupiter.cloud.planittesting.com')
    browser.maximize_window()

    # Navigates to contact page
    browser.find_element_by_id("nav-contact").click()

    # Populates telephone field with invalid (string) data and verifies for the error message.
    browser.find_element_by_id("telephone").send_keys("John")
    assert "Please enter a valid telephone number" in browser.page_source
    sleep(2)


def test_cart_items(browser):
    # Loads the target page url
    browser.get('http://jupiter.cloud.planittesting.com')
    browser.maximize_window()

    # Navigates to shop page, clicks on buy twice for "Funny Cow" and once for "Fluffy Bunny"
    browser.find_element_by_id("nav-shop").click()
    sleep(3)
    browser.find_elements_by_link_text("Buy")[5].click()
    browser.find_elements_by_link_text("Buy")[5].click()
    browser.find_elements_by_link_text("Buy")[3].click()

    # Navigates to cart page, validates for the presence of items and their quantities.
    browser.find_element_by_id("nav-cart").click()
    sleep(3)
    assert "Funny Cow" in browser.page_source
    assert "Fluffy Bunny" in browser.page_source
    assert browser.find_elements_by_name(
        "quantity")[0].get_property("value") == '2'
    assert browser.find_elements_by_name(
        "quantity")[1].get_property("value") == '1'
