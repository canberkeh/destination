from flask import Flask
import os

template_dir = os.path.abspath('./project/templates')
app = Flask(__name__, template_folder=template_dir)
from project.views.api import *
from project.views.main import *


if __name__ == '__main__':
    app.run(debug=True)
