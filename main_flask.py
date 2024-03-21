import logging
from pathlib import Path

from flask import Flask, render_template, request
# from flask_minify import Minify

from google_forms import create_google_apps_script

# https://medium.com/swlh/how-to-host-your-flask-app-on-pythonanywhere-for-free-df8486eb6a42
# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
_logger = logging.getLogger(__name__)
TITLE = 'Markdown to Google Forms'
app = Flask(__name__)
# Minify(app=app, html=True, js=True, cssless=True)

@app.route('/', methods=['GET', 'POST'])
def _root():
    if request.method == 'POST':
        if 'create' in request.form:
            code = request.form.get('markdown_code')

            if code is not None and len(code) > 0:
                values = {
                    'code': code,
                    'form_script': create_google_apps_script(code),
                    'title': TITLE,
                }

                return render_template('index.html', **values)

        elif 'reset' in request.form:
            code = Path('sample.md').read_text()
            values = {
                'code': code,
                'form_script': create_google_apps_script(code),
                'title': TITLE,
            }

            return render_template('index.html', **values)

    values = {
        'code': '',
        'form_script': '',
        'title': TITLE,
    }

    return render_template('index.html', **values)


if __name__ == '__main__':
    # create a handler to log to stderr
    stderr_handler = logging.StreamHandler()

    # create a logging format
    stderr_formatter = logging.Formatter('{message}', style='{')
    stderr_handler.setFormatter(stderr_formatter)

    # add the handler to the root logger
    logging.basicConfig(level=logging.INFO, handlers=[stderr_handler])

    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(debug=True, host='0.0.0.0', port=5000)
