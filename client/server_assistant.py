
import json
import subprocess
from time import sleep

from flask import Flask, render_template, request, send_file

def run_test_commandline(test_name, reports, prod_type):

    # Run the command "pytest main.py --no-header -vv --html=report.html"
    if prod_type == 'Wint3':
        # Open the source and destination files
        with open('C:\\Users\\liorm\\Desktop\\Automation-Selenium\\configuration_json_wint3.json', 'r') as f:
            source_data = json.load(f)

        with open('C:\\Users\\liorm\\Desktop\\Automation-Selenium\\configuration_json.json', 'w') as f:
            # Replace the data in the destination file with the data from the source file
            json.dump(source_data, f, indent=4)

    else:
        # Open the source and destination files
        with open('C:\\Users\\liorm\\Desktop\\Automation-Selenium\\configuration_json_FL.json', 'r') as f:
            source_data = json.load(f)

        with open('C:\\Users\\liorm\\Desktop\\Automation-Selenium\\configuration_json.json', 'w') as f:
            # Replace the data in the destination file with the data from the source file
            json.dump(source_data, f, indent=4)

    result = subprocess.run(
        ["pytest", f"C:\\Users\\liorm\\Desktop\\Automation-Selenium\\{test_name}.py", "--no-header", "-vv",
         f"--html=C:\\Users\\liorm\\Desktop\\Automation-Selenium\\client\\templates\\report_{test_name}.html"
            , '>', "C:\\Users\\liorm\\Desktop\\Automation-Selenium\\client\\test-output.txt"],
        shell=True,)
    sleep(2)
    filename = f"C:\\Users\\liorm\Desktop\Automation-Selenium\\client\\templates\\report_{test_name}.html"
    with open(filename, "r") as file:
        contents = file.read()

    contents = contents.replace("href=\"assets/style.css\"", "href=\"static/assets/style.css\"")

    with open(filename, "w") as file:
        file.write(contents)
    reports.append(render_template(f"report_{test_name}.html"))
