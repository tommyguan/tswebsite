from flask import Flask

import subprocess
app = Flask(__name__)

# Route to retrieve account summary


@app.route('/')
def account_summary():
    p = subprocess.Popen(
        'python3 ./ib_insync_util/open_orders.py', shell=True, stdout=subprocess.PIPE)
    result = p.communicate()
    return result


if __name__ == '__main__':
    app.run(debug=True)
