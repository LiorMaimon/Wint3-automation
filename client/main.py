import json
import subprocess
from time import sleep
import server_assistant
from flask import Flask, render_template, request, send_file
app = Flask(__name__)


@app.route("/")
def index():
    file_path = "C:\\Users\\liorm\\Desktop\\Automation-Selenium\\client\\test-output.txt"
    with open(file_path, 'w') as f:
        f.write('')
    return render_template("index.html")

@app.route("/javascript/<path>")
def load_javascript(path):
    return send_file(path, mimetype='text/javascript')


@app.route("/results")
def tests_results():
    file_path = "C:\\Users\\liorm\\Desktop\\Automation-Selenium\\client\\test-output.txt"
    try:

         with open(file_path, 'r') as f:
            lines = f.readlines()
            response = {}
            try:
                for i in range(3, len(lines)):# from line 3
                    if not lines[i]:
                        break
                    words = lines[i].split()
                    word_from_index_3 = words[0][4:len(words[0])].find('.')+4
                    key = words[0][3:word_from_index_3]
                    if key not in response:
                        response[key] = ''
                    step_name = words[0][words[0].find('test_')+5:len(words[0])]
                    response[key] += step_name + ' '
                    response[key] += words[1] + ' '
                    response[key] += lines[i][lines[i].find('['):len(lines)-1] + '<br><br>'
            except:
                return json.dumps(response)
            return json.dumps(response)

    except:
        sleep(1)
        return json.loads('{}')


@app.route('/run_command', methods=['POST'])
def run_command():
    selected = request.get_json()['selected']
    reports = []

    if 'open_valve' in selected:
        server_assistant.run_test_commandline('open_valve', reports)
    if 'close_valve' in selected:
        server_assistant.run_test_commandline('close_valve', reports)
    if 'inject_water' in selected:
        server_assistant.run_test_commandline('Leak_detection_constant_flow_major_fixed_mode', reports)
    if 'set_policy' in selected:
        server_assistant.run_test_commandline('set_policy', reports)
    if 'recurring_policy' in selected:
        server_assistant.run_test_commandline('recurring_policy', reports)
    if 'exception_policy' in selected:
        server_assistant.run_test_commandline('exception_policy', reports)
    combined_reports = "".join(reports)
    return combined_reports


def main():
    app.run(host="0.0.0.0", port=5000, debug=True)


if __name__ == '__main__':
    main()
