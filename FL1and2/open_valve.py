from time import sleep
import pytest
from selenium import webdriver
import json
import tests


with open("C:\\Users\\liorm\\Desktop\\Automation-Selenium\\FL1and2\\configuration_json.json") as f:
    configuration_date = json.load(f)

    # Set the URL of the website to be tested
url = configuration_date['portal']["url"]
driver = webdriver.Firefox()
driver.get(url)

user_name = configuration_date['portal']['user_name']
password = configuration_date['portal']['password']
site_number = configuration_date['portal']['site_number']
water_system_number = configuration_date['portal']['water_system_number']
product_id = configuration_date['portal']['product_id']


def test_login():
    try:
        tests.loggin(driver, user_name, password)
    except:
        pytest.fail("failed to login")


def test_delete_waiting():
    try:
        tests.connect_to_product(driver, site_number, water_system_number)
        tests.delete_waiting(driver)
    except:
        pytest.fail("failed to delete waiting")


def test_clear_all_leaks():
    try:
        tests.connect_to_product(driver, site_number, water_system_number)
        tests.clear_all_leaks(driver, site_number, water_system_number, product_id)
    except Exception as e:
        pytest.fail(str(e))


def test_delete_valve_error():
    try:
        tests.connect_to_product(driver, site_number, water_system_number)
        tests.delete_valve_error(driver, site_number, water_system_number, product_id)
    except Exception as e:
        pytest.fail(str(e))


def test_open_valve_from_system_control():
    try:
        tests.connect_to_product(driver, site_number, water_system_number)
        tests.open_valve_from_system_control(driver, product_id, site_number, water_system_number)
    except:
        pytest.fail("No event was received")



def test_close_connection():
    sleep(3)
    driver.quit()


# test_login()
# test_connect_to_product()
# test_delete_waiting()
# test_clear_all_leaks()
# test_open_valve_from_system_control()
# test_close_connection()