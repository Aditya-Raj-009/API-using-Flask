import mysql.connector
import json
from flask import make_response, request
import re
import jwt
from functools import wraps
from Config.config import db_config

class auth_model:


    def __init__(self):
        # connection establishment code:
        try:
            self.conn = mysql.connector.connect(**db_config)
            self.conn.autocommit = True # required whenever we insert or update or delete data.
            self.cur = self.conn.cursor(dictionary=True) # true : because we want data in dic formate.

            print("Connection successfully established!")
        except Exception as e:
            print(f"Error: {e}")
            return
        


    # decorator:
    
    def token_auth(self, endpoint=''):

        def inner1(func):
            @wraps(func)
            def inner2(*args):
                endpoint = request.url_rule # so that current reqst jis v endpoint ko aai h wo hume iss url_rule ke jariye mil jayega.

                print(endpoint) # /user/getall. we get when we send request from postman

                # print(request.headers.get("Authorization")) # after executing we see autorization token that we have sent through url (postman).
                authorization = request.headers.get("Authorization")
                if re.match("^Bearer *([^ ]+) *$",authorization,flags=0):
                    token = authorization.split(' ')[1]
                    try:
                        token_decoded = jwt.decode(token,'aditya',algorithms='HS256')
                    except jwt.ExpiredSignatureError:
                        return make_response({"ERROR":"TOKEN_EXPIRED"},404)
                    role_id = token_decoded['payload']['role_id']
                    self.cur.execute(f"SELECT roles from accessibility_view where endpoints='{endpoint}'")
                    result = self.cur.fetchall()
                    if len(result)>0:
                        allowed_role =json.loads(result[0]['roles'])
                        if role_id in allowed_role:

                            return func(*args)
                        else:
                            return make_response({"ERROR":"INVALID_ROLE_ID"},404)
                    else:
                        return make_response({"ERROR":"UNKNOWN_ENDPOINT"},404)
                else:
                    return make_response({'ERROR':'INVALID_TOKEN' },401)
            return inner2
        return inner1

            
            