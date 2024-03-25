
from app import app
from model.user_model import user_model
from flask import request
from datetime import datetime
from model.auth_model import auth_model
from flask import send_file

auth = auth_model()



@app.route('/user/getall')
@auth.token_auth()
def user_getall_controller():
    obj = user_model()
    return obj.user_getall_model()

# we have to explicitly need to give (method=['POST']) because it's by default GET:
@app.route('/user/addone',methods=['POST'])
@auth.token_auth()
def user_addone_controller():
    obj = user_model()
    # to catch data send by postman(or data from form that suppose to be add in database):
    # request.form :It is a variable which recieve data as immutable dictionary.
    return obj.user_addone_model(request.form)

# for multiple data insertion:
@app.route('/user/addmultiple',methods=['POST'])
def user_addMultiple_controller():
    obj = user_model()
    # to catch data send by postman(or data from form that suppose to be add in database):
    # request.form :It is a variable which recieve data as immutable dictionary.
    
    return obj.usr_addMultiple_model(request.json)



# we have to explicitly need to give (method=['PUT']) because it's by default GET:
@app.route('/user/update',methods=['PUT'])
@auth.token_auth()
def user_update_controller():
    obj = user_model()
    return obj.user_update_model(request.form)


@app.route('/user/delete/<id>',methods=['DELETE'])

def user_delete_controller(id):
    obj = user_model()
    return obj.user_delete_model(id)


# patch:

@app.route('/user/patch/<id>',methods=['PATCH'])
def user_patch_controller(id):
    obj = user_model()
    return obj.user_patch_model(request.form,id)

#pagination:

@app.route('/user/getall/limit/<limit>/page/<page>',methods=['GET'])
def user_pagination_controller(limit,page):
    obj = user_model()
    return obj.user_pagination_model(limit,page)




# files:

@app.route('/user/<uid>/upload/avatar',methods = ['PUT']) # uid: id
def user_upload_avatar_controller(uid):

    obj = user_model()
    # step 1:
    # for file:
    file = request.files['avatar']

    # step 2: saving with unique file name:

    # to save file in filesystem: save(path where to save your file)
    # file.save(file.filename) # for this file path, it will save here only in our current directory.
    # file.save(f"uploads/{file.filename}")
    
    uniqFileName = str(datetime.now().timestamp()).replace('.','')

    fileNameSplit = file.filename.split('.')  # to split extension of file (.jpg,.png, etc)

    ext = fileNameSplit[len(fileNameSplit)-1]

    finalFilePath = f'uploads/{uniqFileName}.{ext}'
    file.save(finalFilePath)

    return obj.user_upload_avatar_model(uid,filePath=finalFilePath)




#  fetch file:
@app.route("/uploads/<fileName>")
def user_getAvatar_controller(fileName):
    return send_file(f"uploads/{fileName}")


# JWT:

@app.route('/user/login',methods = ['POST'])
def user_login_controller():
    obj = user_model()
    return obj.user_login_model(request.form)