import multiprocessing
from time import sleep
import pytest
from selenium import webdriver
import json
import tests
import subprocess

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
                         'open', 'enabled', 'fixed', 'event based', '50', '150')
    except:
        pytest.fail('fail to set default policy')
#need to check the details if it is like we sent


def test_inject_simulated_water_flow():
    injection_process = None
    try:
        tests.connect_to_product(driver, configuration_date['site_number'], configuration_date['water_system_number'])
        injection_process = tests.start_inject_water()

    except:
        pytest.fail('fail to inject water')


def test_warning_message_arrived():
    tests.connect_to_product(driver, configuration_date['site_number'], configuration_date['water_system_number'])
    warning_gotten = tests.is_warning_command_was_gotten(driver, configuration_date['site_number'],
                                                         configuration_date['water_system_number'],
                                                         configuration_date['product_id'])
    if warning_gotten:
        assert True
    else:
        assert False


def test_close_message_arrived():
    sleep(60)
    tests.connect_to_product(driver, configuration_date['site_number'], configuration_date['water_system_number'])
    close_gotten = tests.is_close_command_was_gotten(driver, configuration_date['site_number'],
                                                         configuration_date['water_system_number'],
                                                         configuration_date['product_id'])
    if close_gotten:
        assert True
    else:
        assert False
