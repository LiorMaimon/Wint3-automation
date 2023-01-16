from time import sleep
import pytest
from selenium import webdriver
import json
import tests


with open("configuration_json.json") as f:
    configuration_date = json.load(f)

    # Set the URL of the website to be tested
url = configuration_date["url"]
driver = webdriver.Firefox()
driver.get(url)


def test_login():
    try:
        tests.loggin(driver, configuration_date['user_name'], configuration_date['password'])
    except:
        pytest.fail("failed to login")


def test_pre_testing():
    try:
        tests.connect_to_product(driver, configuration_date['site_number'],
                                 configuration_date['water_system_number'])
        tests.delete_waiting(driver)
    except:
        pytest.fail("failed to delete waiting")

    try:
        tests.connect_to_product(driver, configuration_date['site_number'], configuration_date['water_system_number'])
        tests.clear_all_leaks(driver, configuration_date['site_number'], configuration_date['water_system_number'], configuration_date['product_id'])
    except:
        pytest.fail("failed to clear all leaks")

    try:
        tests.connect_to_product(driver, configuration_date['site_number'], configuration_date['water_system_number'])
        tests.delete_valve_error(driver, configuration_date['site_number'], configuration_date['water_system_number'], configuration_date['product_id'])
    except:
        pytest.fail("fail to delete valve error")

def test_set_default_policy():
    try:
        tests.connect_to_product(driver, configuration_date['site_number'], configuration_date['water_system_number'])
        tests.set_policy(driver, configuration_date['site_number'], configuration_date['water_system_number'],configuration_date['product_id'],
                         'close', 'enabled', 'fixed', 'event based', '179', '348')
    except:
        pytest.fail('fail to set default policy')
#need to check the details if it is like we sent

def test_close_connection():
    sleep(3)
    driver.close()

