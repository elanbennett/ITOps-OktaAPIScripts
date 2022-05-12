from Functions import filecloud_functions as ff, okta_functions as of, report_functions as rf
import time
from datetime import date
today = date.today().strftime("%m%d%Y")

if __name__ == '__main__':
    st = time.time()
    path = "/Users/elan/OneDrive - canoo/Projects/PycharmProjects/ITOpsScripts/reports/"

    # == FC Admin Login == #
    fc_session = ff.FCAdminLogin()

    # === CHECK FC for DEPROVISIONED Users === #
    # Pull list of deprovisioned users for Okta, then check if any of them have a FileCloud account
    data = []
    d_users = of.run_async(of.getDeactivatedUsers())
    for user in d_users:
        username = user.profile.login.split('@')[0]
        UserCall = ff.FCCheckUserExists(fc_session, username)
        if UserCall:
            print("ACCOUNT FOUND |", username)
            line = (username, "true")
        else:
            print("No account")
            line = (username, "false")
        data.append(line)

    report_title = "FileCloud User Cleanup_" + today + ".csv"  # Set title
    rf.write_out(data, path, report_title)

    # == Delete User == #
    # if UserCall.status_code == 200:
    #     f.FCDeleteUser(session, username)
    # else:
    #     print("User not found")

    # === TRACK FUNCTION RUN TIME === #
    print("Function run time:")
    print("----%.2f----"%(time.time()-st))