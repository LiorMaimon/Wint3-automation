import os
import psutil
import signal
import subprocess
from time import sleep
from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import assistants_functions


NUMBER_OF_COMMANDS_TO_CHECK = 8
TIME_RANGE = 1


def loggin(driver, user_name_json, password_json):
    user_name = driver.find_element(By.XPATH, "//*[@id=\"user_email\"]")
    password = driver.find_element(By.XPATH, "//*[@id=\"user_password\"]")
    user_name.send_keys(user_name_json)
    password.send_keys(password_json)
    sign_in_button = driver.find_element(By.XPATH, "//*[@id=\"login-btn\"]")
    sign_in_button.click()
    admin_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/div/header/nav/ul[1]/li[2]/a")))
    assert admin_button.text == 'Admin'


def connect_to_product(driver, site_number_json, water_system_number_json):
    sleep(2)
    site_number = site_number_json
    water_system_number = water_system_number_json
    water_system_url = "https://control.wint.ai/en/sites/{}/water_systems/{}".format(site_number,
                                                                                             water_system_number)
    driver.get(water_system_url)
    edit_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[4]/div/a[1]")))
    assert edit_button.text == "Edit"


def connect_to_policy_page(driver, site_number_json, water_system_number_json):
    sleep(2)
    site_number = site_number_json
    water_system_number = water_system_number_json
    water_system_url = "https://control.wint.ai/en/sites/{}/water_systems/{}/policies".format(site_number,
                                                                                             water_system_number)
    driver.get(water_system_url)
    policy_title = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//h3[@class='panel-title' and text()='Policy']")))
    assert policy_title.text == "Policy"


def delete_waiting(driver):
    assistants_functions.find_element_by_xpath_and_click_it(driver, "/html/body/div/div[4]/div/a[3]")
    sleep(3)
    assistants_functions.find_element_by_xpath_and_click_it(driver, "/html/body/div/div[4]/div[1]/a[4]")
    alert = driver.switch_to.alert
    alert.accept()
    new_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[4]/div[1]/a[2]")))
    assert new_button.text == 'New'


def open_valve_from_system_control(driver, product_number, site_number, water_system_number):
    assistants_functions.find_element_by_xpath_and_click_it(driver, "//*[@id=\"command_open_vlv\"]")
    now = datetime.now()
    sleep(2)
    alert = driver.switch_to.alert
    alert.accept()
    close_button_popup_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH, "/html/body/div[1]/div[8]/div[1]/div/div[2]/div[1]/div/div/div/div[3]/button")))
    close_button_popup_message.click()
    sleep(15)
    assistants_functions.find_element_by_xpath_and_click_it(driver,
                "//a[@href='/en/sites/{}/water_systems/{}/products/{}/commands']".format(
                                              site_number, water_system_number, product_number))
    try:
        assistants_functions.check_commands_arrived_in_portal(driver, NUMBER_OF_COMMANDS_TO_CHECK, TIME_RANGE,
                                                              'OP_EVT_VALVE_OPEN_FL3', now)
    except:
        assert False


def close_valve_from_system_control(driver, product_number, site_number, water_system_number):
    assistants_functions.find_element_by_xpath_and_click_it(driver, "//*[@id=\"command_close_vlv\"]")
    now = datetime.now()
    sleep(2)
    alert = driver.switch_to.alert
    alert.accept()
    close_button_popup_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH,
                                          "/html/body/div[1]/div[8]/div[1]/div/div[2]/div[1]/div/div/div/div[3]/button")))
    close_button_popup_message.click()
    sleep(15)
    assistants_functions.find_element_by_xpath_and_click_it(driver,
                "//a[@href='/en/sites/{}/water_systems/{}/products/{}/commands']".format(
                                              site_number, water_system_number, product_number))
    try:
        assistants_functions.check_commands_arrived_in_portal(driver, NUMBER_OF_COMMANDS_TO_CHECK, TIME_RANGE,
                                                              'OP_EVT_VALVE_CLOSE_FL3', now)
    except:
        assert False


def clear_all_leaks(driver, site_number, water_system_number, product_number):
    assistants_functions.find_element_by_xpath_and_click_it(driver,
                                            "//a[@href='/en/sites/{}/water_systems/{}/products/{}/commands']".format(
                                              site_number, water_system_number, product_number))
    sleep(3)

    try:
        now = datetime.now()
        assistants_functions.set_new_command_and_check_command_arrived_in_portal(
            driver, site_number, water_system_number, product_number, 'clear', NUMBER_OF_COMMANDS_TO_CHECK, TIME_RANGE,
            'OP_RES_ALG_CLEAR_ALL_LEAKS', now)
    except:
        raise Exception("no OP_RES_ALG_CLEAR_ALL_LEAKS message was arrived")


def delete_valve_error(driver, site_number, water_system_number, product_number):
    assistants_functions.find_element_by_xpath_and_click_it(driver,
                                            "//a[@href='/en/sites/{}/water_systems/{}/products/{}/commands']".format(
                                              site_number, water_system_number, product_number))
    sleep(3)
    try:
        now = datetime.now()
        assistants_functions.set_new_command_and_check_command_arrived_in_portal(
            driver, site_number, water_system_number, product_number, 'delete', NUMBER_OF_COMMANDS_TO_CHECK, TIME_RANGE,
            'OP_RES_CLEAN_VALVE_ERROR', now)
    except:
        raise Exception("no OP_RES_CLEAN_VALVE_ERROR message was arrived")


def set_policy(driver, site_number, water_system_number, product_number, valve_status, auto_shutoff, detection_mode,
               algo_mode, warning_threshold, close_threshold, policy_kind='default_policy', start_time='0',
               end_time="5"):
    #  for now, it is for default and recurring need exception
    assistants_functions.find_element_by_xpath_and_click_it(driver,
                                            "//a[@href='/en/sites/{}/water_systems/{}/policies']".format(
                                              site_number, water_system_number))
    if policy_kind == "exception_policy":
        assistants_functions.find_element_by_xpath_and_click_it(driver, "//*[text()='Add Exception']")
        assistants_functions.set_policy_name(driver)
        assistants_functions.set_exception_policy_time(driver, int(start_time), int(end_time))
    if policy_kind == 'recurring_policy':
        assistants_functions.find_element_by_xpath_and_click_it(driver, "//*[text()='Add Recurring Policy']")
        assistants_functions.set_policy_name(driver)
        assistants_functions.set_recurring_policy_time(driver, int(start_time), int(end_time))

    assistants_functions.set_policy_valve_status(driver, valve_status)
    assistants_functions.set_policy_shutoff_status(driver, auto_shutoff)
    assistants_functions.set_policy_detection_mode(driver, detection_mode, warning_threshold, close_threshold,
                                                   algo_mode)
    sleep(3)
    if policy_kind == 'default_policy':
        apply_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@type='submit'][@value='Apply']")))
        apply_button.click()
        alert = driver.switch_to.alert
        alert.accept()
    if policy_kind == 'recurring_policy':
        create_policy_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'create_button')))
        create_policy_button.click()
        text = "Recurring - The Recurring policy conflicts with"
        try:
            element = driver.find_element(By.XPATH, "//*[contains(text(), '" + text + "')]")
            if text in element.text:
                raise Exception("The text '" + text + "' is present on the page.")
        except:
            print("")
    if policy_kind == 'exception_policy':
        create_policy_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'create_button')))
        create_policy_button.click()
        text = "conflicts with"
        try:
            element = driver.find_element(By.XPATH, "//*[contains(text(), '" + text + "')]")
            if text in element.text:
                raise Exception("The text '" + text + "' is present on the page.")
        except:
            print("")
    now = datetime.now()
    sleep(3)
    connect_to_product(driver, site_number, water_system_number)
    sleep(8)
    assistants_functions.find_element_by_xpath_and_click_it(driver,
                                            "//a[@href='/en/sites/{}/water_systems/{}/products/{}/commands']".format(
                                              site_number, water_system_number, product_number))
    sleep(5)
    try:
        policy_content = assistants_functions.check_commands_arrived_in_portal(driver, NUMBER_OF_COMMANDS_TO_CHECK, TIME_RANGE,
                                                              'OP_RES_INSERT_DEVICE_CONF_FL3', now, True)
        if not assistants_functions.policy_check(policy_content, policy_kind):
            assert False
    except:
        raise Exception("no "+"OP_RES_INSERT_DEVICE_CONF_FL3 command was arrived")


def delete_all_recurring_policies(driver, site_number, water_system_number, product_number):
    assistants_functions.find_element_by_xpath_and_click_it(driver,
                                                            "//a[@href='/en/sites/{}/water_systems/{}/policies']"
                                                            .format(site_number, water_system_number))
    assistants_functions.find_element_by_xpath_and_click_it(driver,
                                                            '//a[@data-toggle="tab" and text()="Recurring Policy"]')
    recurring_policies_tbody = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//tbody[@role="alert"]')))
    rows = recurring_policies_tbody.find_elements(By.CSS_SELECTOR, "tr")
    while rows:
        cells = rows[-1].find_elements(By.CSS_SELECTOR, "td")
        delete_symbol = cells[12].find_element(By.XPATH,
                                               '//a[@data-method="delete" and @data-confirm="Are you sure?"]')
        delete_symbol.click()
        alert = driver.switch_to.alert
        alert.accept()
        sleep(3)
        assistants_functions.find_element_by_xpath_and_click_it(driver,
                                                                '//a[@data-toggle="tab" and text()="Recurring Policy"]')
        connect_to_product(driver, site_number, water_system_number)
        assistants_functions.find_element_by_xpath_and_click_it(driver,
                                                                "//a[@href='/en/sites/{}/water_systems/{}/products/{}/commands']".format(
                                                                    site_number, water_system_number, product_number))
        assistants_functions.check_commands_arrived_in_portal(driver, NUMBER_OF_COMMANDS_TO_CHECK, TIME_RANGE,
                                                              "OP_RES_INSERT_DEVICE_CONF_FL3", datetime.now())
        connect_to_policy_page(driver, site_number, water_system_number)

        assistants_functions.find_element_by_xpath_and_click_it(driver,
                                                                '//a[@data-toggle="tab" and text()="Recurring Policy"]')
        recurring_policies_tbody = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH,
                                              '//tbody[@role="alert"]')))
        rows = recurring_policies_tbody.find_elements(By.CSS_SELECTOR, "tr")


def delete_all_exception_policies(driver, site_number, water_system_number, product_number):
    assistants_functions.find_element_by_xpath_and_click_it(driver,
                                                            "//a[@href='/en/sites/{}/water_systems/{}/policies']"
                                                            .format(site_number, water_system_number))
    assistants_functions.find_element_by_xpath_and_click_it(driver,
                                                            '//a[@data-toggle="tab" and text()="Policy Exceptions"]')
    exception_policies_tbody = driver.find_element(By.XPATH, '/html/body/div/div[6]/div[3]/div/div/div/div/div/div/div[2]/div/div/table/tbody')
    rows = exception_policies_tbody.find_elements(By.CSS_SELECTOR, "tr")
    while rows:
        cells = rows[-1].find_elements(By.CSS_SELECTOR, "td")
        delete_symbol = cells[11].find_element(By.XPATH,
                                               '//a[@data-method="delete" and @data-confirm="Are you sure?"]')
        delete_symbol.click()
        alert = driver.switch_to.alert
        alert.accept()
        sleep(3)
        assistants_functions.find_element_by_xpath_and_click_it(driver,
                                                                '//a[@data-toggle="tab" and text()="Policy Exceptions"]')
        connect_to_product(driver, site_number, water_system_number)
        assistants_functions.find_element_by_xpath_and_click_it(driver,
                                                                "//a[@href='/en/sites/{}/water_systems/{}/products/{}/commands']".format(
                                                                    site_number, water_system_number, product_number))
        assistants_functions.check_commands_arrived_in_portal(driver, NUMBER_OF_COMMANDS_TO_CHECK, TIME_RANGE,
                                                              "OP_RES_INSERT_DEVICE_CONF_FL3", datetime.now())
        connect_to_policy_page(driver, site_number, water_system_number)

        assistants_functions.find_element_by_xpath_and_click_it(driver,
                                                                '//a[@data-toggle="tab" and text()="Policy Exceptions"]')
        recurring_policies_tbody = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH,
                                              '/html/body/div/div[6]/div[3]/div/div/div/div/div/div/div[2]/div/div/table/tbody')))
        rows = recurring_policies_tbody.find_elements(By.CSS_SELECTOR, "tr")

def wait_policy_changed(driver, site_number, water_system_number, product_number, time_to_wait):
    sleep(time_to_wait*60)
    assistants_functions.find_element_by_xpath_and_click_it(driver,
                                            "//a[@href='/en/sites/{}/water_systems/{}/products/{}/commands']".format(
                                              site_number, water_system_number, product_number))
    assistants_functions.check_commands_arrived_in_portal(driver, NUMBER_OF_COMMANDS_TO_CHECK-4,TIME_RANGE+1,
                                                          "OP_EVT_VALVE_OPEN_FL3", datetime.now())


def check_close_content(driver, site_number, water_system_number, product_number, time_to_wait):
    sleep(time_to_wait * 60)
    assistants_functions.find_element_by_xpath_and_click_it(driver,
                                            "//a[@href='/en/sites/{}/water_systems/{}/products/{}/commands']".format(
                                                    site_number, water_system_number, product_number))
    close_content = assistants_functions.check_commands_arrived_in_portal(driver, NUMBER_OF_COMMANDS_TO_CHECK - 4, TIME_RANGE + 1,
                                                          "OP_EVT_VALVE_CLOSE_FL3", datetime.now(),True)
    if '"OwnerId"=>3' in close_content and '"PlungerPos"=>1' in close_content:
        return
    raise Exception('no "PlungerPos"=>1, "OwnerId"=>3 shown')


def start_inject_water(flow_level='major'):
    try:
        file_path = "C:\\Users\\liorm\\Desktop\\Automation-Selenium\\injection"
        command1 = "cd " + file_path
        command2 = "python inject_simulated_water.py"
        inject_process = subprocess.Popen(f"{command1} && {command2}", shell=True)
        return inject_process
    except:
        raise Exception("fail to start inject")


def stop_inject_water(injection_process):
    try:
        parent = psutil.Process(injection_process.pid)
        children = parent.children(recursive=True)
        os.kill(children[0].pid, signal.SIGTERM)
    except:
        raise Exception("fail to stop water flow")


def is_command_was_gotten_loop(driver, site_number, water_system_number, product_number, command_to_check,
                               content_to_check=None, relevant_content=True):
    assistants_functions.find_element_by_xpath_and_click_it(driver,
                                            "//a[@href='/en/sites/{}/water_systems/{}/products/{}/commands']".format(
                                                site_number, water_system_number, product_number))
    for i in range(30):
        now = datetime.now()
        try:
            leak_detect_content = assistants_functions.check_commands_arrived_in_portal(driver,
                                                                                        NUMBER_OF_COMMANDS_TO_CHECK,
                                                                                        TIME_RANGE,
                                                                                        command_to_check, now,
                                                                                        True)
            if leak_detect_content:
                if not relevant_content:
                    return True
                if content_to_check in leak_detect_content:
                    return True
        except:
            print("")
        sleep(10)
        driver.refresh()

    return False

