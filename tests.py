from time import sleep
from selenium import webdriver
from datetime import datetime, timedelta
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import assistants_functions


# Set the URL of the website to be tested
# url = "https://control-staging.wint.ai/en"
# driver = webdriver.Firefox()
# driver.get(url)


def loggin(driver,user_name_json, password_json):
    user_name = driver.find_element(By.XPATH,"//*[@id=\"user_email\"]")
    password = driver.find_element(By.XPATH,"//*[@id=\"user_password\"]")
    user_name.send_keys(user_name_json)
    password.send_keys(password_json)
    sign_in_button = driver.find_element(By.XPATH,"//*[@id=\"login-btn\"]")
    sign_in_button.click()
    admin_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/div/header/nav/ul[1]/li[2]/a")))
    assert admin_button.text == 'Admin'


def connect_to_product(driver,site_number_json, water_system_number_json):
    sleep(2)
    site_number = site_number_json
    water_system_number = water_system_number_json
    water_system_url = "https://control-staging.wint.ai/en/sites/{}/water_systems/{}".format(site_number, water_system_number)
    driver.get(water_system_url)
    edit_button =WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[4]/div/a[1]")))
    assert edit_button.text == "Edit"


def delete_waiting(driver):
    commands_button = driver.find_element(By.XPATH, "/html/body/div/div[4]/div/a[3]")
    commands_button.click()
    sleep(3)
    delete_wating_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[4]/div[1]/a[4]")))
    delete_wating_button.click()
    alert = driver.switch_to.alert
    alert.accept()
    new_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[4]/div[1]/a[2]")))
    assert new_button.text == 'New'


def open_valve_from_system_control(driver,product_number_json,site_number_json, water_system_number_json):
    open_valve_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id=\"command_open_vlv\"]")))
    open_valve_button.click()
    now = datetime.now()
    sleep(2)
    alert = driver.switch_to.alert
    alert.accept()
    close_button_popup_message =WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[8]/div[1]/div/div[2]/div[1]/div/div/div/div[3]/button")))
    close_button_popup_message.click()
    sleep(15)
    commands_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//a[@href='/en/sites/{}/water_systems/{}/products/{}/commands']".format(site_number_json,water_system_number_json,product_number_json))))
    commands_button.click()
    try:
        assistants_functions.check_commands_arrived_in_portal(driver,3,1,'OP_EVT_VALVE_OPEN_FL3',now)
    except:
        assert False


def close_valve_from_system_control(driver,product_number_json,site_number_json, water_system_number_json):
    close_valve_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//*[@id=\"command_close_vlv\"]")))
    close_valve_button.click()
    now = datetime.now()
    sleep(2)
    alert = driver.switch_to.alert
    alert.accept()
    close_button_popup_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/div[1]/div[8]/div[1]/div/div[2]/div[1]/div/div/div/div[3]/button")))
    close_button_popup_message.click()
    sleep(15)
    commands_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//a[@href='/en/sites/{}/water_systems/{}/products/{}/commands']".format(site_number_json,water_system_number_json,product_number_json))))
    commands_button.click()
    try:
        assistants_functions.check_commands_arrived_in_portal(driver,3,1,'OP_EVT_VALVE_CLOSE_FL3',now)
    except:
        assert False


def clear_all_leaks(driver, site_number, water_system_number, product_number):
    commands_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[4]/div/a[3]")))
    commands_button.click()
    sleep(3)

    try:
        now = datetime.now()
        assistants_functions.set_new_command_and_check_command_arrived_in_portal(
            driver, site_number, water_system_number, product_number, 'clear',8,1,'OP_RES_ALG_CLEAR_ALL_LEAKS',now)
    except:
        assert False


def delete_valve_error(driver, site_number, water_system_number, product_number):
    commands_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/div/div[4]/div/a[3]")))
    commands_button.click()
    sleep(3)
    try:
        now = datetime.now()
        assistants_functions.set_new_command_and_check_command_arrived_in_portal(
            driver, site_number, water_system_number, product_number, 'delete',8,1,'OP_RES_CLEAN_VALVE_ERROR',now)
    except:
        assert False


def set_policy(driver, site_number, water_system_number, product_number, valve_status, auto_shutoff, detection_mode, algo_mode,
               warning_threshold, close_threshold):
    #  for now, it is for default, need to add recurring and exception
    policy_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH,
                                          "//a[@href='/en/sites/{}/water_systems/{}/policies']".format(
                                              site_number, water_system_number))))
    policy_button.click()
    assistants_functions.set_policy_valve_status(driver, valve_status)
    assistants_functions.set_policy_shutoff_status(driver, auto_shutoff)
    assistants_functions.set_policy_detection_mode(driver, detection_mode, warning_threshold, close_threshold, algo_mode)
    sleep(3)
    apply_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@type='submit'][@value='Apply']")))
    apply_button.click()
    alert = driver.switch_to.alert
    alert.accept()
    now = datetime.now()
    sleep(3)
    connect_to_product(driver, site_number, water_system_number)
    sleep(8)
    commands_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH,
                                          "//a[@href='/en/sites/{}/water_systems/{}/products/{}/commands']".format(
                                              site_number, water_system_number, product_number))))
    commands_button.click()
    sleep(5)
    try:
        assistants_functions.check_commands_arrived_in_portal(driver, 8, 1, 'OP_RES_INSERT_DEVICE_CONF_FL3', now)
    except:
        assert False

def start_inject_water(flow_level):




