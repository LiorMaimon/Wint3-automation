import json
import subprocess
from time import sleep

from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/results")
def tests_results():
    file_path = "C:\\Users\\liorm\\Desktop\\Automation-Selenium\\client\\test-output.txt"
    #file_path = 'stam.txt'
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            last_line = lines[-1]
            words = last_line.split()
            for i, word in enumerate(words):
                if word.__contains__("test_"):
                    test_name = word.split("_")[-1]
                    next_word = words[i + 1] if i + 1 < len(words) else None
                    py_index = last_line.find(".py")
                    if py_index != -1:
                        module_name = last_line[3:py_index]
                    else:
                        module_name = None
                    result = {"test_name": test_name, "next_word": next_word, "module_name": module_name}
                    return json.dumps(result)
    except:
        sleep(1)
        return json.loads('{}')

tests_results()
@app.route('/run_command', methods=['POST'])
def run_command():
    selected = request.get_json()['selected']
    reports = []

    if 'open_valve' in selected:
        # Run the command "pytest main.py --no-header -vv --html=report.html"
        result = subprocess.run(
            ["pytest", "C:\\Users\\liorm\\Desktop\\Automation-Selenium\\open_valve.py", "--no-header", "-vv",
             "--html=C:\\Users\\liorm\\Desktop\\Automation-Selenium\\client\\templates\\report_open_valve.html"
                ],
            #, ">", "C:\\Users\\liorm\\Desktop\\Automation-Selenium\\client\\test-output.txt"
            shell=True, )
        sleep(2)
        filename = "C:\\Users\\liorm\Desktop\Automation-Selenium\\client\\templates\\report_open_valve.html"
        with open(filename, "r") as file:
            contents = file.read()

        contents = contents.replace("href=\"assets/style.css\"", "href=\"static/assets/style.css\"")

        with open(filename, "w") as file:
            file.write(contents)
        reports.append(render_template("report_open_valve.html"))
    if 'close_valve' in selected:
        result = subprocess.run(
            ["pytest", "C:\\Users\\liorm\\Desktop\\Automation-Selenium\\close_valve.py", "--no-header", "-vv",
             "--html=C:\\Users\\liorm\\Desktop\\Automation-Selenium\\client\\templates\\report_close_valve.html"],
            shell=True, )
        sleep(2)
        filename = "C:\\Users\\liorm\Desktop\Automation-Selenium\\client\\templates\\report_close_valve.html"
        with open(filename, "r") as file:
            contents = file.read()

        contents = contents.replace("href=\"assets/style.css\"", "href=\"static/assets/style.css\"")

        with open(filename, "w") as file:
            file.write(contents)
        reports.append(render_template("report_close_valve.html"))
    if 'inject_water' in selected:
        result = subprocess.run(
            ["pytest", "C:\\Users\\liorm\\Desktop\\Automation-Selenium\\"
                       "Leak_detection_constant_flow_major_fixed_mode.py", "--no-header", "-vv",
             "--html=C:\\Users\\liorm\\Desktop\\Automation-Selenium\\client\\templates\\report_inject_water.html"],
            shell=True, )
        sleep(2)
        filename = "C:\\Users\\liorm\Desktop\Automation-Selenium\\client\\templates\\report_inject_water.html"
        with open(filename, "r") as file:
            contents = file.read()

        contents = contents.replace("href=\"assets/style.css\"", "href=\"static/assets/style.css\"")

        with open(filename, "w") as file:
            file.write(contents)
        reports.append(render_template("report_inject_water.html"))
    if 'set_policy' in selected:
        result = subprocess.run(
            ["pytest", "C:\\Users\\liorm\\Desktop\\Automation-Selenium\\set_policy.py", "--no-header", "-vv",
             "--html=C:\\Users\\liorm\\Desktop\\Automation-Selenium\\client\\templates\\report_set_policy.html"],
            shell=True, )
        sleep(2)
        filename = "C:\\Users\\liorm\Desktop\Automation-Selenium\\client\\templates\\report_set_policy.html"
        with open(filename, "r") as file:
            contents = file.read()

        contents = contents.replace("href=\"assets/style.css\"", "href=\"static/assets/style.css\"")

        with open(filename, "w") as file:
            file.write(contents)
        reports.append(render_template("report_set_policy.html"))
    if 'set_recurring_policy' in selected:
        result = subprocess.run(
            ["pytest", "C:\\Users\\liorm\\Desktop\\Automation-Selenium\\recurring_policy.py", "--no-header", "-vv",
             "--html=C:\\Users\\liorm\\Desktop\\Automation-Selenium\\client\\templates\\recurring_policy.html"],
            shell=True, )
        sleep(2)
        filename = "C:\\Users\\liorm\Desktop\Automation-Selenium\\client\\templates\\recurring_policy.html"
        with open(filename, "r") as file:
            contents = file.read()

        contents = contents.replace("href=\"assets/style.css\"", "href=\"static/assets/style.css\"")

        with open(filename, "w") as file:
            file.write(contents)
        reports.append(render_template("recurring_policy.html"))
    combined_reports = "".join(reports)
    return combined_reports
