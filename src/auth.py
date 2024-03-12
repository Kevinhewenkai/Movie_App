from email.message import EmailMessage
import ssl
import re
import jwt
import time
import sqlite3
import os
import helper
import base64
import requests
import smtplib
import random

email_sender = 'yukicyt0511@gmail.com'
email_password = 'idzvqhgxkswotizr'
EMAIL_ADDRESS = ''
EMAIL_PASSWORD = ''
reset_code = None
cwd = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
db_file = os.path.join(cwd, "db", "movieDB.db")


def auth_login(email, psw):
    '''
    Enables users to login
    '''
    # connect database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Checks if email is valid
    if not check_email(email):
        return {'400': 'Invalid email'}

    # password_hash = hashlib.sha256(psw.encode()).hexdigest()
    user_id = None
    user_name = None
    user_token = None
    # check if there is the email in database
    try:
        sql_1 = "SELECT COUNT(*) FROM User WHERE email = ?"
        data = (email,)
        cursor.execute(sql_1, data)
        cursor_result = cursor.fetchone()[0]
        if cursor_result == 0:
            # return {'400':"You have not registered")
            return {'400': "You have not registered"}
        sql_2 = '''
            SELECT * FROM User WHERE email = ?
        '''
        data = (email,)
        cursor.execute(sql_2, data)
        user_elements = cursor.fetchone()
        # print(user_elements)
        user_id = user_elements[0]
        user_name = user_elements[1]
        user_password = user_elements[2]
        user_token = user_elements[4]

        # if user_token is not None:
        #     raise ("User already logged in.")
        if user_password == psw:
            # generate token
            user_token = helper.gen_token()
            sql_3 = '''
                UPDATE User set token = ? WHERE email = ?
            '''
            data = (user_token, email,)
            cursor.execute(sql_3, data)
            conn.commit()
            print("token updated")
        # check if updating success
        sql_4 = "SELECT * FROM User WHERE token = ?"
        data = (user_token,)
        cursor.execute(sql_4, data)
        cursor_result = cursor.fetchone()[4]
        print(cursor_result)
        cursor.close()
    except sqlite3.Error as error:
        print("Fail to login check in database", error)

    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")

    return {'user_id': user_id, 'token': user_token, 'user_name': user_name}


def auth_logout(token):
    '''
    Enables users to logout

    '''
    # if token has been invalidated then it return success
    conn = sqlite3.connect(db_file)

    cursor = conn.cursor()
    try:
        print(token)
        sql_1 = '''
            SELECT COUNT(*) from User where token = ?
        '''
        data = (token,)
        cursor.execute(sql_1, data)
        cursor_result = cursor.fetchall()
        print(len(cursor_result))
        if len(cursor_result) == 1:

            sql_2 = '''UPDATE User SET token = ? where token = ?'''
            data = (None, token,)
            cursor.execute(sql_2, data)
            conn.commit()
        else:
            # raise ('cannot logout')
            return {'400': "cannot logout"}
    except sqlite3.Error as error:
        print("Fail to log out check in database", error)

    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")

    return


def auth_register(name, email, psw):
    '''
    Enables users to register
    '''
    user_id = None
    if not check_email(email):
        return {'400': "email not correct"}

    # Checks if the name is too short or too long
    if len(name) < 1 or len(name) > 50:
        # return {'400':'Name must be 1-50 characters inclusive')
        return {'400': "Name must be 1-50 characters inclusive"}

    # Checks if the password is too short or too long
    if len(psw) < 6 or len(psw) > 20:
        # return {'400':'Password must be 6-20 characters inclusive')
        return {'400': "Password must be 6-20 characters inclusive"}

    # Checks if the email has already been used
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    token = None
    try:
        sql_1 = '''
            SELECT * from User where email = ?
        '''
        data = (email,)
        cursor.execute(sql_1, data)
        cursor_result = cursor.fetchall()
        print(len(cursor_result))
        if len(cursor_result) == 1:
            # return {'400':"This email has been reigistered")
            return {'400': "This email has been reigistered"}
        # find the max_id to insert user_id
        # token generation
        token = helper.gen_token()
        sql_2 = '''
            INSERT INTO User(name, password, email, token)
            VALUES (?, ?, ?, ?)
        '''
        data = (name, psw, email, token,)
        cursor.execute(sql_2, data)
        conn.commit()
    except sqlite3.Error as error:
        print("Fail to register check in database", error)

    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")

    # Now that errors have been avoided, we register the user
    return {'token': token}
##
# def auth_passwordreset_request(email):
#     conn = sqlite3.connect(db_file)

#     cursor = conn.cursor()
#     try:
#         sql1 = '''
#             SELECT COUNT(*) from User where email  = ?
#         '''
#         data = (email,)
#         cursor.execute(sql1, data)
#         cursor_result = cursor.fetchall()

#         print(len(cursor_result))
#         if len(cursor_result) != 0:

#             seed(1)
#             code = randint(1000, 9999)
#             secrect = str(code)
#             s = smtplib.SMTP_SSL('smtp.gmail.com')
#             s.login(EMAIL_ADDRESS,EMAIL_PASSWORD)
#             msg = MIMEMultipart()
#             msg['From'] = EMAIL_ADDRESS
#             msg['To'] = email
#             msg['Subject'] = "flockr password reset code"
#             msg.attach(MIMEText(secrect, 'plain'))
#             s.send_message(msg)
#             s.quit()

#     except sqlite3.Error as error:
#         print("Fail to register check in database", error)
#     return { }


# def password_reset(vertification, new_pwd):

#     if vertification not in global_var.data['vertifiction_code'].keys():
#         return {'400':'Incorrect vertification code')
#     if len(new_pwd) < 6 or len(new_pwd) > 20:
#         return {'400':'Password must be 6-20 characters inclusive')
#     user_id = global_var.data['vertification_code'][vertification]
#     for user in global_var.data['user']:
#         if user['id'] == user_id:
#             user['psw'] = hashlib.sha256(new_pwd.encode()).hexdigest()
#         break

#     del global_var.data['vertification_code'][vertification]

#     return { }


def delete_account(token):

    conn = sqlite3.connect(db_file)

    cursor = conn.cursor()
    try:
        print(token)
        sql_1 = '''
            SELECT COUNT(*) from User where token = ?
        '''
        data = (token,)
        cursor.execute(sql_1, data)
        cursor_result = cursor.fetchall()
        print(len(cursor_result))
        if len(cursor_result) == 1:

            sql_2 = '''DELETE from User where token = ?'''
            data = (token,)
            cursor.execute(sql_2, data)
            conn.commit()
        else:
            return {'400': 'cannot delete'}
    except sqlite3.Error as error:
        print("Fail to delete check in database", error)

    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")

    return{}


def add_user_photo(token, photo_url):
    if token is None:
        return {'400': "Please login."}
    user = helper.get_user_from_token()
    if user is None:
        return {'400': "Please login."}
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    sql_1 = '''
            SELECT user_id from User where token = ?
        '''
    data = (token,)
    cursor.execute(sql_1, data)
    user_id = cursor.fetchone()
    base_64_photo = base64.b64encode(requests.get(photo_url).content)
    cursor.execute("UPDATE User SET photo = '{}' WHERE user_id = '{}'".format(
        base_64_photo, user_id))
    return ("success")


def ban_user(token, ban_user_id):
    user = helper.get_user_from_token(token)
    user_id = user['user_id']
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    check = cursor.execute('''
        SELECT ban_user_id FROM Banlist WHERE user_id = ? AND ban_user_id = ?
    ''', (user_id, ban_user_id,)).fetchone()
    print(check)
    if check is not None:
        return {'400': 'user already banned'}
    cursor.execute('''
        INSERT INTO Banlist(user_id, ban_user_id) VALUES (?, ?)
    ''', (user_id, ban_user_id,))
    conn.commit()
    return {'result': 'success'}


################   helper functions   ################


def gen_token(user_id):
    '''
    Generates a token
    '''
    SECRET = 'afenjewIksdAMkldaSEVRETsknfjadsbfbuwh;/.ds301883yefsk;adf'
    token = jwt.encode({'u_id': user_id, 'time': time.time()},
                       SECRET, algorithm='HS256').decode('utf-8')
    return token


def check_email(email):
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(regex, email)):
        return True
    else:
        # return False
        return True


def auth_get_user_name(user_id):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    user_name = cursor.execute(
        '''
        SELECT name from User WHERE user_id = ?
        ''', (user_id,)
    ).fetchone()
    return {'user_name': user_name[0]}


def get_user_banned(token):
    user = helper.get_user_from_token(token)
    if user is None:
        return {'400': 'No such user'}
    user_id = user['user_id']
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    user_ids = cursor.execute('''
        SELECT ban_user_id FROM Banlist WHERE user_id = ?
        ''', (user_id,)
    ).fetchall()
    result = []
    for id in user_ids:
        result.append(id[0])
    return {'banned id': result}


def delete_banned_user(token, removed_user_id):
    user = helper.get_user_from_token(token)
    if user is None:
        return {'400': 'No such user'}
    user_id = user['user_id']
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM Banlist WHERE user_id = ? AND ban_user_id = ?
        ''', (user_id, removed_user_id))
    conn.commit()
    return {'result': 'success'}


def send_code(email):
    conn = sqlite3.Connection(db_file)
    cursor = conn.cursor()
    res = cursor.execute(
        '''
        SELECT email FROM User WHERE email  = ?
        ''', (email,)).fetchone()
    if res is None:
        return {'400': 'Email does not exist.'}
    global reset_code
    reset_code = str(random.randint(1000, 9999))

    subject = 'check out'
    body = """ 
    reset ur password
    """ + reset_code

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email
    em['Subject'] = subject

    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465,  context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email, em.as_string())
    return {'200': 'code successfully sent'}


def check_code(code):
    global reset_code
    if code == reset_code:
        return True
    else:
        return False


def reset_psw(email, code, new_psw):
    print(reset_code)
    if len(new_psw) < 6 or len(new_psw) > 20:
        # raise InputError('Password must be 6-20 characters inclusive')
        return {'400': "Password must be 6-20 characters inclusive"}
    if not check_code(code):
        return {'400': 'incorrect code, please try again'}
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        sql_1 = '''
            UPDATE User SET password=? where email = ?
        '''
        data = (new_psw, email,)
        cursor.execute(sql_1, data)
        conn.commit()
    except sqlite3.Error as error:
        print("Fail to register check in database", error)

    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")
            return {'200': 'successfully changed.'}
