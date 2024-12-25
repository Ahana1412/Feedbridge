# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""


import os
from flask_migrate import Migrate
from flask_minify import Minify
from sys import exit

from apps.config import config_dict
from apps import create_app, db
from apps.chatbot.routes import chatbot_blueprint
# Import the chatbot blueprint

import pymysql
pymysql.install_as_MySQLdb()

# WARNING: Don't run with debug turned on in production!
DEBUG = (os.getenv('DEBUG', 'False') == 'True')

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:
    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]
except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)
Migrate(app, db)

# Register Chatbot Blueprint
app.register_blueprint(chatbot_blueprint, url_prefix="/chatbot")  # Prefix routes with /chatbot

if not DEBUG:
    Minify(app=app, html=True, js=False, cssless=False)

if DEBUG:
    app.logger.info('DEBUG            = ' + str(DEBUG))
    app.logger.info('Page Compression = ' + ('FALSE' if DEBUG else 'TRUE'))
    app.logger.info('DBMS             = ' + str(app_config.SQLALCHEMY_DATABASE_URI))
    app.logger.info('ASSETS_ROOT      = ' + str(app_config.ASSETS_ROOT))

    # Additional Debug Logs for Chatbot
    app.logger.info('Chatbot Blueprint Registered at /chatbot')

if __name__ == "__main__":
    app.run()

