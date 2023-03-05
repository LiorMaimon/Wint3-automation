import json
from datetime import datetime, timedelta
from time import sleep
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PULSE_RATIO = 0.049

def check_commands_arrived_in_portal(driver,number_of_commands_to_check,time_range,message_to_check,now_time, content=False):
    sleep(10)
    driver.refresh()
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
    assert False


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


def set_recurring_policy_time(driver, start_time, end_time):
    start_time_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div/div/form/div[8]/div[1]/span/span")
    end_time_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div/div/form/div[8]/div[3]/span/span")
    start_time_button.click()
    start_hour = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div/div[1]/table/tbody/tr[2]/td[1]/span')))
    start_hour.click()
    start_hour = (datetime.now()).hour
    start_hour_str = "{:02d}".format(start_hour)
    start_hour_table = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div/div[2]/table/tbody')))
    sleep(1)
    try:
        picked_hour = iterate_tbody(start_hour_table, start_hour_str)
        picked_hour.click()
    except:
        raise Exception("not valid hour")
    if start_time>=0:
        up_hour_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div/div[1]/table/tbody/tr[1]/td[3]/a/span')))
        for i in range(start_time):
            up_hour_button.click()
    else:
        down_hour_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/div/div[1]/table/tbody/tr[3]/td[3]/a/span')))
        for i in range(start_time):
            down_hour_button.click()

    end_time_button.click()
    end_hour = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div[1]/table/tbody/tr[2]/td[1]/span')))
    end_hour.click()
    end_hour = (datetime.now()).hour
    start_hour_str = "{:02d}".format(end_hour)
    end_hour_table = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div[2]/table/tbody')))
    sleep(1)
    try:
        picked_hour = iterate_tbody(end_hour_table, start_hour_str)
        picked_hour.click()
    except:
        raise Exception("not valid hour")
    if end_time>=0:
        up_minute_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div[1]/table/tbody/tr[1]/td[3]/a/span')))
        for i in range(end_time):
            up_minute_button.click()
    else:
        down_minute_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/div/div[1]/table/tbody/tr[3]/td[3]/a/span')))
        for i in range(end_time):
            down_minute_button.click()


def set_exception_policy_time(driver, start_time, end_time):
    start_time_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div/div/form/div[8]/div/span/span")
    end_time_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div/div/form/div[9]/div/span/span")
    start_time_button.click()
    find_element_by_xpath_and_click_it(driver, "/html/body/div[2]/ul/li[2]/a/span")
    start_hour = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/ul/li[3]/div/div[1]/table/tbody/tr[2]/td[1]/span')))
    start_hour.click()
    start_hour = (datetime.now()).hour
    start_hour_str = "{:02d}".format(start_hour)
    start_hour_table = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/ul/li[3]/div/div[2]/table/tbody')))
    sleep(1)
    try:
        picked_hour = iterate_tbody(start_hour_table, start_hour_str)
        picked_hour.click()
    except:
        raise Exception("not valid hour")
    if start_time >= 0:
        up_hour_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/ul/li[3]/div/div[1]/table/tbody/tr[1]/td[3]/a/span')))
        for i in range(start_time):
            up_hour_button.click()
    else:
        down_hour_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[2]/ul/li[3]/div/div[1]/table/tbody/tr[3]/td[3]/a/span')))
        for i in range(start_time):
            down_hour_button.click()

    end_time_button.click()
    find_element_by_xpath_and_click_it(driver, "/html/body/div[3]/ul/li[2]/a/span")
    end_hour = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/ul/li[3]/div/div[1]/table/tbody/tr[2]/td[1]/span')))
    end_hour.click()
    end_hour = (datetime.now()).hour
    start_hour_str = "{:02d}".format(end_hour)
    end_hour_table = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/ul/li[3]/div/div[2]/table/tbody')))
    sleep(1)
    try:
        picked_hour = iterate_tbody(end_hour_table, start_hour_str)
        picked_hour.click()
    except:
        raise Exception("not valid hour")
    if end_time >= 0:
        up_minute_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/ul/li[3]/div/div[1]/table/tbody/tr[1]/td[3]/a/span')))
        for i in range(end_time):
            up_minute_button.click()
    else:
        down_minute_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/div[3]/ul/li[3]/div/div[1]/table/tbody/tr[3]/td[3]/a/span')))
        for i in range(end_time):
            down_minute_button.click()


def policy_check(policy_command_content, kind_of_policy):
    with open("C:\\Users\\liorm\\Desktop\\Automation-Selenium\\FL1and2\\configuration_json.json") as f:
        configuration_date = json.load(f)
    valve_status = configuration_date[f'{kind_of_policy}_1']['valve_status']
    if valve_status == 'close':
        valve_status = "0"
    else:
        valve_status = '1'
    auto_shutoff = configuration_date[f'{kind_of_policy}_1']['auto_shutoff']
    if auto_shutoff == 'enabled':
        auto_shutoff = '1'
    else:
        auto_shutoff = '0'
    detection_mode = configuration_date[f'{kind_of_policy}_1']['detection_mode']
    if detection_mode == 'fixed':
        detection_mode = 1
    else:
        detection_mode = 0
    algo_mode = configuration_date[f'{kind_of_policy}_1']['algo_mode']
    if algo_mode == 'event based':
        algo_mode = 0
    else:
        algo_mode = 1
    warning_threshold = configuration_date[f'{kind_of_policy}_1']['warning_threshold']
    close_threshold = configuration_date[f'{kind_of_policy}_1']['close_threshold']

    valve_status_check = f"\"valveAction\"=>{valve_status}".lower() in policy_command_content.lower()
    auto_shutoff_check = f"\"autoShutoff\"=>{auto_shutoff}".lower() in policy_command_content.lower()
    detection_mode_check = f"\"fixed\"=>{detection_mode}".lower() in policy_command_content.lower()
    algo_mode_check = f"\"cumulative\"=>{algo_mode}".lower() in policy_command_content.lower()
    warning_threshold_check = f"\"WarningThreshold\"=>{str(int(int(warning_threshold)/PULSE_RATIO))}".lower() in policy_command_content.lower()
    close_threshold_check = f"\"CloseThreshold\"=>{str(int(int(close_threshold)/PULSE_RATIO))}".lower() in policy_command_content.lower()
    return valve_status_check and auto_shutoff_check and detection_mode_check and algo_mode_check \
        and warning_threshold_check and close_threshold_check


def iterate_tbody(tbody, text_to_find):
    rows = tbody.find_elements(By.CSS_SELECTOR, "tr")
    for row in rows:
        cells = row.find_elements(By.CSS_SELECTOR, "td")
        for cell in cells:
            if cell.text == text_to_find:
                return cell
    assert False

def set_policy_name(driver):
    policy_name = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'policy_name')))
    policy_name.send_keys('automation test')


def find_element_by_xpath_and_click_it(driver, xpath_str):
    button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, xpath_str)))
    button.click()


