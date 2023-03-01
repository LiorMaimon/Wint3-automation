import multiprocessing
import os
import signal
from time import sleep

import psutil
import pytest
from selenium import webdriver
import json
import tests
import threading

with open("C:\\Users\\liorm\\Desktop\\Automation-Selenium\\FL1&2\\configuration_json.json") as f:
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
valve_status = configuration_date['default_policy_1']['valve_status']
auto_shutoff = configuration_date['default_policy_1']['auto_shutoff']
detection_mode = configuration_date['default_policy_1']['detection_mode']
algo_mode = configuration_date['default_policy_1']['algo_mode']
warning_threshold = configuration_date['default_policy_1']['warning_threshold']
close_threshold = configuration_date['default_policy_1']['close_threshold']
injection_process = None

def test_login():
    try:
        tests.loggin(driver, user_name, password)
    except:
        pytest.fail("failed to login")


def test_pre_testing():
    try:
        tests.connect_to_product(driver, site_number,
                                 water_system_number)
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


def test_set_default_policy():
    try:
        tests.connect_to_product(driver, site_number, water_system_number)
        tests.set_policy(driver, site_number, water_system_number,product_id,
                         valve_status, auto_shutoff, detection_mode, algo_mode, warning_threshold, close_threshold)
    except Exception as e:
        pytest.fail(str(e))


def test_inject_simulated_water_flow():
    global injection_process
    try:
        injection_process = tests.start_inject_water()

    except Exception as e:
        pytest.fail(str(e))


def test_warning_message_arrived():
    try:
        tests.connect_to_product(driver, site_number, water_system_number)
        warning_gotten = tests.is_warning_command_was_gotten(driver, site_number, water_system_number, product_id)
        if warning_gotten:
            assert True
        else:
            assert False
    except:
        pytest.fail('fail to get warning')


def test_close_message_arrived():
    try:
        sleep(60)
        tests.connect_to_product(driver, site_number, water_system_number)
        close_gotten = tests.is_close_command_was_gotten(driver, site_number, water_system_number, product_id)
        if close_gotten:
            assert True
        else:
            assert False
    except:
        pytest.fail('fail to get close')


def test_stop_water_simulator():
    try:
        global injection_process
        tests.stop_inject_water(injection_process)
    except Exception as e:
        pytest.fail(str(e))


def test_close_connection():
    try:
        sleep(3)
        driver.quit()
    except Exception as e:
        pytest.fail(str(e))
