from sqlite3 import connect
from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import database
import re
from flask import flash, session

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE email =%(email)s;"
        result = connectToMySQL(database).query_db(query, data)
        if len(result) > 0:
            return cls(result[0])
        else:
            return None

    @classmethod
    def create(cls, data):
        query = "INSERT into users(first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        result = connectToMySQL(database).query_db(query, data)
        return result

    @staticmethod
    def validate_registration(data):
        isValid = True
        if data['first_name'] == "":
            flash("You must provide a first name.", "error_register_first_name")
            isValid = False
        if len(data['first_name']) < 2:
            flash("You must provide a first name with more than 2 characters.", "error_register_first_name")
            isValid = False
        if data['last_name'] == "":
            flash("You must provide a last name.", "error_register_last_name")
            isValid = False
        if len(data['last_name']) < 2:
            flash("You must provide a first name with more than 2 characters.", "error_register_last_name")
            isValid = False
        if data['email'] == "":
            flash("You must provide an email.", "error_register_email")
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!", "error_register_email")
            isValid = False
        if data['password'] == "":
            flash("You must provide a password.", "error_register_password")
            isValid = False
        if len(data['password']) < 8:
            flash("You must provide a password that's at least 8 characters long.", "error_register_password")
            isValid = False
        if data['password_confirmation'] != data['password']:
            flash("Your password confirmation doesn't match.", "error_register_password_confirmation")
            isValid = False
        return isValid

    @staticmethod
    def validate_login(data):
        isValid = True
        if data['email'] == "":
            flash("Please provide your email.", "error_email_login")
            isValid = False
        if data['password'] == "":
            flash("Please provide your password.", "error_password_login")
            isValid = False
        return isValid

    @staticmethod
    def validate_session():
        if "id" in session:
            return True
        else:
            return False
    
    @staticmethod
    def validate_user(user):
        isValid = True
        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            isValid = False
        return isValid