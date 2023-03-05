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
valve_status = configuration_date['exception_policy_1']['valve_status']
auto_shutoff = configuration_date['exception_policy_1']['auto_shutoff']
detection_mode = configuration_date['exception_policy_1']['detection_mode']
algo_mode = configuration_date['exception_policy_1']['algo_mode']
warning_threshold = configuration_date['exception_policy_1']['warning_threshold']
close_threshold = configuration_date['exception_policy_1']['close_threshold']
start_time = configuration_date['exception_policy_1']['start_time']
end_time = configuration_date['exception_policy_1']['end_time']

def test_login():
    try:
        tests.loggin(driver, user_name, password)
    except:
        pytest.fail("failed to login")



def test_pre_testing():
    try:
        tests.connect_to_product(driver, site_number, water_system_number)
        tests.delete_waiting(driver)
    except:
        pytest.fail("failed to delete waiting")

    try:
        tests.connect_to_product(driver, site_number, water_system_number)
        tests.clear_all_leaks(driver, site_number, water_system_number, product_id)
    except Exception as e:
        pytest.fail(str(e))

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


def test_set_exception_policy_close_valve():
    try:
        tests.connect_to_product(driver, site_number, water_system_number)
        tests.set_policy(driver, site_number, water_system_number, product_id,
                     valve_status, auto_shutoff, detection_mode, algo_mode, warning_threshold, close_threshold,
                         'exception_policy',start_time, end_time)
    except:
        pytest.fail("fail to set exception policy")


def test_close_valve_command_arrived():
    try:
        tests.connect_to_product(driver, site_number, water_system_number)
        tests.check_close_content(driver, site_number,water_system_number,product_id, int(start_time))
    except Exception as e:
        pytest.fail(str(e))

def test_delete_all_policies():
    try:
        tests.connect_to_product(driver, site_number, water_system_number)
        tests.delete_all_exception_policies(driver, site_number, water_system_number, product_id)
    except:
        pytest.fail("fail to delete policies")


def test_close_connection():
    sleep(3)
    driver.quit()
