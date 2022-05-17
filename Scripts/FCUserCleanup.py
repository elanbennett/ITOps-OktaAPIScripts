from Functions import filecloud_functions as ff, okta_functions as of, report_functions as rf
import time
from datetime import date
today = date.today().strftime("%m%d%Y")

if __name__ == '__main__':
    st = time.time()

    # == FC Admin Login == #
    fc_session = ff.FCAdminLogin()

    # === CHECK FC for DEPROVISIONED Users === #
    # Pull list of deprovisioned users for Okta, then check if any of them have a FileCloud account
    data = []
    log = []
    d_users = of.run_async(of.getDeactivatedUsers())
    for user in d_users:
        username = user.profile.login.split('@')[0]  # Extract username from okta email
        UserExists = ff.FCCheckUserExists(fc_session, username)  # Search for account in FileCloud by username
        if UserExists:
            print("FILECLOUD ACCOUNT FOUND |", username)
            line = (username, "true")
            ff.FCCheckStorageUsage(fc_session, username)
            # == Delete User == #
            # f.FCDeleteUser(fc_session, username)
            # log.append(("Successfully deleted FileCloud account for", username))
        else:
            # print("No account")
            line = (username, "false")
        data.append(line)

    path = "/Users/elan/OneDrive - canoo/Projects/PycharmProjects/ITOpsScripts/reports/"
    report_title = "FileCloud User Cleanup_" + today + ".csv"  # Set title
    rf.write_out(data, path, report_title)



    # === TRACK FUNCTION RUN TIME === #
    print("Function run time:")
    print("----%.2f----"%(time.time()-st))