# =======================================================================
# Version 1.0
# -----------------------------------------------------------------------
# Last changed by: Elan Bennett
# -----------------------------------------------------------------------
# 1.0 Changes:
# =======================================================================

# == Imports == #
import sys, os, time
sys.path.append(os.getcwd())
from Functions import report_functions as rf, okta_functions as of
from datetime import date
today = date.today().strftime("%m%d%Y")

if __name__ == '__main__':

    # === SET VARIABLES === #
    st = time.time()

    # === INIT LOG FILE === #
    if not os.path.exists('/localpath/logs/'):
        os.mkdir('/localpath/logs/')
    title = 'OktaBulkUserGroupUpdate_' + today
    output_txt = open(os.path.expanduser('../logs/' + title + ".txt"), "a")
    text = "Attempting to bulk add users to groups. \n"
    output_txt.write(text)

    # === BULK ADDING USERS TO GROUPS === #
    # Users - list of emails
    target_users = ["testuser1@acme.com", "testuser2@acme.com"]
    users = []
    # Groups - list of group names
    target_groups = ["testgroup1", "testgroup2"]

    # == Create a master dictionary of groups as Name/ID pairs as a reference == #
    group_library = {}
    # - List all groups from Okta
    list_groups = of.run_async(of.getAllGroups())
    # - Append name/id pairs to dictionary
    for group in list_groups:
        group_library[group.profile.name] = group.id

    # == Iterate by user and add user to any missing groups == #
    for login in target_users:
        # - Get user obj
        user_obj = of.run_async(of.getUser(login))
        if user_obj:
            output_txt.write("Updating group permissions for " + user_obj.profile.login + "\n")
        else:
            output_txt.write("User for " + login + " not found. Skipping..")
            continue

        # - Get user's groups from Okta
        user_groups = of.run_async(of.getUsersGroups(user_obj.id))

        # - Extract group IDs from user's groups as a list for reference
        user_group_ids = []
        for group in user_groups:
            user_group_ids.append(group.id)

        # - Iterate through target groups and add user to any that are missing
        for group in target_groups:
            # -- Get Group obj
            group_id = group_library[group]
            group_obj = of.run_async(of.getGroup(group_id))

            # -- Check if user is already in group
            if group_id in user_group_ids:
                text = user_obj.profile.login + " is already a member of " + group + ". Skipping.\n"
                output_txt.write(text)
                continue
            # -- If user is not in group, try adding user to group
            else:
                text = "Attempting to add " + user_obj.profile.login + " to " + group + "... "
                output_txt.write(text)
                err = of.run_async(of.userAddGroup(group_obj, user_obj))   # Note: userAddGroup takes group obj and user obj as input
                if err is None:
                    text = "Successfully added.\n"
                    output_txt.write(text)
                else:
                    text = "Error: " + err
                    output_txt.write(text)


    # ======================================================== #

    # == CLOSE LOG FILE ==#
    output_txt.close()
    # === TRACK FUNCTION RUN TIME === #
    print("----%.2f----"%(time.time()-st))

