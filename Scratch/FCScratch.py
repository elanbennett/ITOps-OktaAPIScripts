from Functions import filecloud_functions as ff

if __name__ == '__main__':
    # == Admin Login == #
    session = ff.FCAdminLogin()

    # == Retrieve User Details == #
    username = 'elan'
    UserCall = ff.FCGetUser(session, username)

    # == Delete User == #
    # if UserCall.status_code == 200:
    #     f.FCDeleteUser(session, username)
    # else:
    #     print("User not found")