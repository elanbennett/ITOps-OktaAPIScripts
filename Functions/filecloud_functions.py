import requests

## Filecloud headers.
Headers = {'Accept': 'application/json'}

## Filecloud creds
Creds = {'adminuser': 'admin', 'adminpassword': 'Files@can00!'}

##Filecloud server API endpoints
ServerURL = 'https://files.canoo.com/'
GuestLoginEndPont = 'core/loginguest'
AdminLoginEndPoint = 'admin/adminlogin'


## Specify user path inside Filecloud.
FilecloudPath = "/elan"  # To be defined

## Upload API params.
UploadApiParams = {'appname': 'explorer', 'path': FilecloudPath, 'offset': 0}



def FCAdminLogin():
    s = requests.Session()
    s.headers.update(Headers)
    LoginCall = s.post(ServerURL + AdminLoginEndPoint, data=Creds, headers=Headers).json()
    if LoginCall['command'][0]['result'] == 1:  # Checks successful login
        print("Admin login successful")
        return s
    else:
        print("Admin login failed")
        return False


def FCGetUser(session, username):
    print("Getting details for user:", username)
    try:
        user_query = {'username': username}
        UserCall = session.post(ServerURL + 'admin/getuser', params=user_query)
        UserCall.raise_for_status()
    except requests.exceptions.HTTPError as error:
        print(error)
    user = UserCall.json()
    if user['user'][0]:
        print("User found")
        for obj in UserCall.json()['user']:
            print(obj)
    else:
        print("User not found")


def FCCheckUserExists(session, username):
    print("Finding user:", username)
    try:
        user_query = {'username': username}
        UserCall = session.post(ServerURL + 'admin/getuser', params=user_query)
        UserCall.raise_for_status()
    except requests.exceptions.HTTPError as error:
        print(error)
    user = UserCall.json()
    return user['user'][0]


def FCDeleteUser(session, profile):
    print("Attemting to delete user:", profile)
    try:
        delete_query = {'profile': profile}
        DeleteCall = session.post(ServerURL + 'admin/deleteuser', params=delete_query)
        DeleteCall.raise_for_status()
    except requests.exceptions.HTTPError as error:
        print(error)
    if DeleteCall.status_code == 200:
        print("User deleted successfully")
    else:
        print("Error deleting user")
