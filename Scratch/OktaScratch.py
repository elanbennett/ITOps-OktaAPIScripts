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
from Functions import report_functions as rf, okta_functions as of
import time
from datetime import date
today = date.today().strftime("%m%d%Y")

if __name__ == '__main__':

    # === SET VARIABLES === #
    st = time.time()
    path = '/Users/elan/OneDrive - canoo/Resources/App Notes/Okta/Reports/'

    # === GET GROUP USERS === #
    # data = functions.getGroupUsers('00g1zzib9nd3S0v9c357')  # FileCloud Group ID
    # report_title = "Group User List_" + today + ".csv"
    # functions.write_out(data, path, report_title)

    # === GET GROUP SNAPSHOT === #
    # data = functions.getAllUsersAllGroups()
    # data = functions.getSnapshot()
    # report_title = "Okta Group Snapshot_" + today + ".csv"  # Set title
    # functions.write_out(data, path, report_title)

    # === GET USER TYPES SNAPSHOT === #
    # elan_id = "00u1fnbyowaGo2y5u357"
    # test_external_id = "00uhyskddoV1CxGFs357"
    # user_types = {
    #     "oty3ggscsu5eeMNAK357": "Contractor",
    #     "oty3ggs8w3wwpom8H357": "External",
    #     "oty3ggre21K20cIdq357": "Intern",
    #     "oty5lxu0qy0SnQNXh357": "Service",
    #     "otypj558oQU4274DR356": "User"
    # }
    # report_title = "Okta User Types Snapshot_" + today + ".csv"  # Set title
    # data = afunc.run_async(rf.listAllUsersTypes())
    # print(len(data))
    # rf.write_out(data, path, report_title)

    # === TESTING === #
    # data = functions.getAllGroups()
    # GP_Users_AppID = "00g2szp903t5MZval357"
    # GP_Users = functions.getGroupUsers(GP_Users_AppID)
    # print(len(GP_Users))
    # async_functions.run_async(async_functions.getUser(elan_id))
    # afunc.run_async(afunc.getAllUsers())

    # Nested ASYNCs
    # def getUserGroups2(uid):
    #     async def getUserGroups2():
    #         person = await functions.getUser(uid)
    #         print(person)


    # path = "/Users/elan/OneDrive - canoo/Projects/PycharmProjects/ITOpsScripts/reports/"
    # title = "Okta-ListGroupIDs_" + today + ".csv"  # Set title
    # rf.write_out(data, path, title)

    # === TRACK FUNCTION RUN TIME === #
    print("----%.2f----"%(time.time()-st))

