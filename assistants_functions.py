import importlib
import multiprocessing
from datetime import datetime, timedelta
from time import sleep
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys


def check_commands_arrived_in_portal(driver,number_of_commands_to_check,time_range,message_to_check,now_time, content=False):
    sleep(3)
    tbodys = driver.find_elements(By.TAG_NAME, 'tbody')
    tbody_commands = tbodys[1]
    rows = tbody_commands.find_elements(By.CSS_SELECTOR, "tr")
    for i in range(number_of_commands_to_check):
        cells = rows[i].find_elements(By.CSS_SELECTOR, "td")
        words = cells[9].text.split(" ")
        hour_time = str(words[1])
        year_time = str(words[0])
        time_from_portal = datetime.strptime(year_time + ' ' + hour_time, '%Y-%m-%d %H:%M:%S')
        if (time_from_portal - timedelta(minutes=time_range) < now_time < time_from_portal + timedelta(minutes=time_range) and cells[
            1].text == message_to_check):
            if not content:
                return
            else:

                content = cells[2].find_element(By.TAG_NAME,"div")

                content.click()
                sleep(1)
                content_text = cells[2]
                return content_text.text




def set_new_command(driver,site_number_json,water_system_number_json,product_number_json, unique_text_command):
    new_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//a[@href='/en/sites/{}/water_systems/{}/products/{}/commands/new']"
                                          .format(site_number_json,water_system_number_json,product_number_json))))
    new_button.click()
    input_text = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "/html/body/div/form/div/div/div[1]/span/input")))
    input_text.send_keys(unique_text_command)
    input_text.send_keys(Keys.ARROW_DOWN)
    input_text.send_keys(Keys.ENTER)
    sleep(3)
    create_command_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "new_command_button")))
    create_command_button.click()
    sleep(2)


def set_new_command_and_check_command_arrived_in_portal(
        driver,site_number,water_system_number,product_number, unique_text_command,
        number_of_commands_to_check,time_range,message_to_check,now_time):

    set_new_command(driver,site_number,water_system_number,product_number, unique_text_command)
    sleep(8)
    all_commands_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH,
                                          "//a[@href='/en/sites/{}/water_systems/{}/products/{}/commands']".format(
                                              site_number, water_system_number, product_number))))
    all_commands_button.click()
    check_commands_arrived_in_portal(driver,number_of_commands_to_check,time_range,message_to_check,now_time)


def set_policy_valve_status(driver, valve_status):
    if valve_status == 'open':
        open_check = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'policy_valve_status_1')))
        open_check.click()
    else:
        open_check = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'policy_valve_status_0')))
        open_check.click()


def set_policy_shutoff_status(driver, shutoff_status):
    if shutoff_status == 'enabled':
        open_check = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'auto_shutoff_on')))
        open_check.click()
    else:
        open_check = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'auto_shutoff_off')))
        open_check.click()


def set_policy_detection_mode(driver, detection_mode_status, warning_threshold, close_threshold, algo_mode):
    if detection_mode_status == 'fixed':
        fixed_check = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'policy_detection_mode_fixed')))
        fixed_check.click()
        warning_check = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'policy_warning_thresholds')))
        warning_check.clear()
        warning_check.send_keys(warning_threshold)
        close_check = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'policy_closed_thresholds')))
        close_check.clear()
        close_check.send_keys(close_threshold)
        if algo_mode == 'event based':
            event_based_check = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'policy_algo_mode_0')))
            event_based_check.click()
        elif algo_mode == 'cumulative':
            cumulative_check = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID, 'policy_algo_mode_1')))
            cumulative_check.click()
    else:
        fixed_check = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'policy_detection_mode_adaptive')))
        fixed_check.click()


def inject_water_in_process(flow_level='major'):

    # injection_script_path = "/C:/Users/liorm/Desktop/Automation-Selenium/injection/inject_simulated_water.py"
    # sys.path.append(injection_script_path)
    # from injection.inject_simulated_water import main
    # main()
    from injection.inject_simulated_water import main
    main()
    # injection_process = multiprocessing.Process(target=injection.inject_simulated_water.main())
    # injection_process.start()
    # return injection_process
#ask uri why it is not running from test and run from function

