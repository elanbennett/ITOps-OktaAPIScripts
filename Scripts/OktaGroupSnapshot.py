# =======================================================================
# Version 1.0
# -----------------------------------------------------------------------
# Last changed by: Elan Bennett
# -----------------------------------------------------------------------
# 1.0 Changes:
# - Added Pagination to functions: getAllUsersAllGroups, getGroupUsers
# - Added function write_out()
# - Added function getAllGroups()
# - Added function getSnapShot()
# =======================================================================

# == Imports == #
from Functions import report_functions as rf
import time
from datetime import date
today = date.today().strftime("%m%d%Y")

if __name__ == '__main__':
    # === SET VARIABLES === #
    st = time.time()
    path = "/Users/elan/OneDrive - canoo/Projects/PycharmProjects/ITOpsScripts/reports/"

    # === GET GROUP USERS === #
    # data = functions.getGroupUsers('00g1zzib9nd3S0v9c357')  # FileCloud Group ID
    # report_title = "Group User List_" + today + ".csv"
    # functions.write_out(data, path, report_title)

    # === GET GROUP SNAPSHOT === #
    # data = functions.getAllUsersAllGroups()
    data = rf.getSnapshotByGroups()
    report_title = "Okta Group Snapshot_" + today + ".csv"  # Set title
    rf.write_out(data, path, report_title)

    # === TESTING === #
    # data = functions.getAllGroups()
    # GP_Users_AppID = "00g2szp903t5MZval357"
    # GP_Users = functions.getGroupUsers(GP_Users_AppID)
    # print(len(GP_Users))

    # === TRACK FUNCTION RUN TIME === #
    print("----%.2f----"%(time.time()-st))













