from flask import Flask

app = Flask(__name__)

app.secret_key = "logging in in secret"           # Needs to be added for session; secret_key can be set to anything in the string

database = "login_and_registration_schema"