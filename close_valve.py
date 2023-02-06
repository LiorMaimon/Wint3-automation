from time import sleep
import pytest
from selenium import webdriver
import json
import tests

with open("configuration_json.json") as f:
    configuration_date = json.load(f)

    # Set the URL of the website to be tested
url = configuration_date['portal']["url"]
driver = webdriver.Firefox()
driver.get(url)


def test_login():
    try:
        tests.loggin(driver, configuration_date['portal']['user_name'], configuration_date['portal']['password'])
    except:
        pytest.fail("failed to login")


def test_delete_waiting():
    try:
        tests.connect_to_product(driver, configuration_date['portal']['site_number'], configuration_date['portal']['water_system_number'])
        tests.delete_waiting(driver)
    except:
        pytest.fail("failed to delete waiting")


def test_clear_all_leaks():
    try:
        tests.connect_to_product(driver, configuration_date['portal']['site_number'], configuration_date['portal']['water_system_number'])
        tests.clear_all_leaks(driver, configuration_date['portal']['site_number'], configuration_date['portal']['water_system_number'], configuration_date['portal']['product_id'])
    except:
        pytest.fail("failed to clear all leaks")


def test_delete_valve_error():
    try:
        tests.connect_to_product(driver, configuration_date['portal']['site_number'], configuration_date['portal']['water_system_number'])
        tests.delete_valve_error(driver, configuration_date['portal']['site_number'], configuration_date['portal']['water_system_number'], configuration_date['portal']['product_id'])
    except:
        pytest.fail("fail to delete valve error")


def test_open_valve_from_system_control():
    try:
        tests.connect_to_product(driver, configuration_date['portal']['site_number'], configuration_date['portal']['water_system_number'])
        tests.close_valve_from_system_control(driver, configuration_date['portal']['product_id'], configuration_date['portal']['site_number'],
                                         configuration_date['portal']['water_system_number'])
    except:
        pytest.fail("No event was received")


def test_close_connection():
    sleep(3)
    driver.close()

# test_login()
# test_connect_to_product()
# test_delete_waiting()
# test_clear_all_leaks()
# test_delete_valve_error()
# test_open_valve_from_system_control()
# test_close_connection()