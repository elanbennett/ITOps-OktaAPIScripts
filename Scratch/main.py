# =======================================================================
# Version 1.0
# -----------------------------------------------------------------------
# Last changed by: Elan Bennett
# -----------------------------------------------------------------------
# 0.0.1 Changes:
# Creating classes and workflow
# 1.0 Changes:
# Completed testing and addition of bulk group deletion processes.
# =======================================================================

# == Imports == #
from Functions import okta_functions_old

if __name__ == '__main__':
    # Standard Functions
    # user = functions.getUser('00u1fnbyowaGo2y5u357')

    # group = functions.getGroupUsers('00g1zzib9nd3S0v9c357')  # FileCloud Group ID

    # === GET GROUP SNAPSHOT === #
    # functions.getGroups()

    # === REMOVE ALL GROUPS FROM DEPROVISIONED USERS === #
    # d_users = functions.getDeactivatedUsers()
    # for user in d_users:
    #     functions.userRemoveAllGroups(user)
    #
    # functions.getGroupsInList(d_users)

    # === SINGLE USER/GROUP TEST === #
    # Removes last group in list for Andy
    # user = functions.getUser('andy.mykrantz@canoo.com')
    # if user is not None:
    #     users_groups = functions.getUsersGroups(user.profile.login)
    #     # for group in users_groups:
    #     #     print(group.profile.name, "|", group.id)
    #     functions.userRemoveGroup(users_groups[-1], user)  # SYNTAX: (GROUP, USER)

    # === TARGETED GROUP BULK TEST === #
    # user = functions.getUser('david.dai@canoo.com')
    # # user2 = functions.getUser('marco-da@canoo.com')
    # # user3 = functions.getUser('marco.isabella@canoo.com')
    # user_list = [user]  # , user2, user3]
    #
    # for user in user_list:
    #    if user is not None:
    #        functions.userRemoveAllGroups(user)

    # === App Username Testing === #
    # functions.getAppUserName( "0oadi1ahitpQBDxIG357", "00ub24t287GYb08Jf357") ## Jira Native, Thony Pinada
    jira_nativeAppID = "0oadi1ahitpQBDxIG357"
    okta_functions_old.getAppUsers(jira_nativeAppID)
    # functions.getUserSchema("00ub24t287GYb08Jf357")