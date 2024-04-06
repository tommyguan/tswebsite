import subprocess
import json
from ib_insync_util.global_vars import python_path


def run_python_file(filename):
    process = subprocess.Popen(
        python_path + filename, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()

    # Convert output to JSON array
    data_array = []
    for line in output.decode("utf-8").splitlines():
        try:
            json_object = json.loads(line)
            data_array.append(json_object)
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)

    return data_array
