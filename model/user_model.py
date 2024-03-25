import mysql.connector
import json
from flask import make_response # for response code.
from datetime import datetime,timedelta
from Config.config import db_config
import jwt

class user_model:

    def __init__(self):
        # connection establishment code:
        try:
            self.conn = mysql.connector.connect(**db_config)
            self.conn.autocommit = True # required whenever we insert or update or delete data.
            self.cur = self.conn.cursor(dictionary=True) # true : because we want data in dic formate.

            print("Connection successfully established!")
        except Exception as e:
            print(f"Error: {e}")
            
    def user_getall_model(self):
        self.cur.execute("SELECT * FROM users")
        result  = self.cur.fetchall()
        # print(result)
        self.cur.close()
        if len(result)>0:
            res = make_response({"payload":result},200)
            res.headers['Access-Control-Allow-Origin'] = '*'  # adding header
            return  res
        return make_response({"message":"No data found"},204) # 204: for no content found.
    

    def user_addone_model(self,data):
        
        self.cur.execute(f"Insert into users (name,email,phone,role_id,password) values('{data['name']}','{data['email']}','{data['phone']}','{data['role_id']}','{data['password']}')")
        
        return {'message':"User created successfully!"}
    

    def user_update_model(self,data):
        self.cur.execute(f"update users set name='{data['name']}',email='{data['email']}',phone='{data['phone']}',role_id='{data['role_id']}',password='{data['password']}' where id={data['id']}")
        if self.cur.rowcount>0:
            return {'message':'User updated successfully'}
        return {'message':'Nothing to update'}
    

    # Delete:

    def user_delete_model(self, id):
        self.cur.execute(f"DELETE FROM users WHERE ID={id}")
        if self.cur.rowcount>0:
            return {'message':"User Deleted Successfully"}
        return {'message':"Nothing to delete"}
    

    # patch:
    
    def user_patch_model(self,data,id):
        # NORMAL UPDATE QUERY: update users set column1 = value1, column2 = value2,.. where id = someid

        # little change when we use patch method:
        qry = "UPDATE users SET"
        for key in data:    # we can send any number of update value.
            qry = f"{qry} {key}='{data[key]}', "

        qry = qry.removesuffix(', ') # remove last ','
        qry+=f' where id = {id}'

        self.cur.execute(qry)

        if self.cur.rowcount>0:
            return {'message':'User updated successfully'}
        return {'message':'Nothing to update'}
    


    # pagination:
    def user_pagination_model(self,limit,page):
        limit = int(limit)
        page = int(page)
        start = (page*limit)-limit
        qry = f'SELECT * FROM users LIMIT {start},{limit}'

        #rest will remain same:
        self.cur.execute(qry)
        result  = self.cur.fetchall()
        self.cur.close()
        if len(result)>0:
            res = make_response({"payload":result,"Current Page no":page,"limit":limit},200)
            res.headers['Access-Control-Allow-Origin'] = '*'  # adding header
            return  res
        return make_response({"message":"No data found"},204) # 204: for no content found.
    

    #  files:

    def user_upload_avatar_model(self,uid,filePath):
        self.cur.execute(f"Update users Set avatar='{filePath}' where id={uid}")
        if self.cur.rowcount>0:
            return {'message':'File Uploaded successfully'}
        return {'message':'Nothing to Upload'}
    

    # JWT:
    
    def user_login_model(self,data):
        # we will not select password because JWT can be decrypted by anyone so anyone would able to password:
        self.cur.execute(f"select id, name, email, phone, avatar, role_id from users where email='{data['email']}' and password = '{data['password']}'")
        result = self.cur.fetchall()
        user_data = result[0]   # this will be our payload in jwt.
        # also we need add expiration time for token:
        exp_time = datetime.now() + timedelta(minutes=15)   # to set expiration time for 15 min.
        exp_epoch_time = int(exp_time.timestamp())  # expiration time

        # if you visit jwt.io you can see there all encryption algo, you can use any one of them for encryption:
        # now import jwt module.
        payload = {
            "payload": user_data,
            "exp": exp_epoch_time
        }
        jwt_token = jwt.encode(payload,key="aditya",algorithm="HS256")
        return make_response({"token": jwt_token},200)  # now after run sending request from postman: you will find jwt token.
    # if you copy paste this token to jwt.io : you will see your payload and expiration . And it can be done by any that's we don't include passwords to create jwt token.
    #  But this recreate if one don't know the key.
    #  we keep this secreat key ('65dity97') at here (server side) because if we send it to
    #  browser then anyone can recreate it by finding this secret key there by inspect.



    # for multiple data insertion:

    def usr_addMultiple_model(self, data):
        qry = "INSERT INTO users (name,email,phone,role_id,password) VALUES "
        for user_data in data:
            qry+=f"('{user_data['name']}','{user_data['email']}','{user_data['phone']}',{user_data['role_id']},'{user_data['password']}'),"
        
        qry = qry.removesuffix(',')
        self.cur.execute(qry)
        return {'message':f"{len(data)} Users created successfully!"}

   