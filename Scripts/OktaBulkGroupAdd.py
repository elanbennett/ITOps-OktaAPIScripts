# =======================================================================
# Version 1.0
# -----------------------------------------------------------------------
# Last changed by: Elan Bennett
# -----------------------------------------------------------------------
# 1.0 Changes:
# =======================================================================

# == Imports == #
from Functions import report_functions as rf, okta_functions as of
import time
import os
from datetime import date
today = date.today().strftime("%m%d%Y")

if __name__ == '__main__':

    # === SET VARIABLES === #
    st = time.time()

    # === INIT LOG FILE === #
    if not os.path.exists('../logs/'):
        os.mkdir('../logs/')
    title = 'OktaBulkUserGroupUpdate_' + today
    output_txt = open(os.path.expanduser('logs/' + title + ".txt"), "a")
    text = "Attempting to bulk add users to groups. \n"
    output_txt.write(text)

    # === BULK ADDING USERS TO GROUPS === #
    # Users - list of emails
    target_users = ["josephh@canoo.com", "kieran.ward@canoo.com", "zac@canoo.com", "Christopher.Lee@canoo.com", "Yash.Patel@canoo.com", "Anurag.Agarwal@canoo.com",
                "steven.montevideo@canoo.com", "giovanni@canoo.com", "Jorge.Morales@canoo.com", "Seok.Lee@canoo.com", "jinesh.shah@canoo.com", "jayson.glanville@canoo.com",
                "Gregory.Vitous@canoo.com", "christopher.reed@canoo.com", "adam.jones@canoo.com"]
    users = []
    # Groups - list of group names
    target_groups = ["team-adas", "team-brakes", "team-suspension", "team-steering", "team-closures",
                     "team-electrical-high-voltage", "team-electrical-low-voltage", "team-ecu", "team-vehicle-switches",
                     "team-vehicle-exteriors", "team-battery", "team-displays", "team-infotainment", "team-interior",
                     "team-powertrain-hardware", "team-restraints", "team-seats", "team-structures-skateboard",
                     "team-thermal-hardware", "team-structures-cabin", "team-lighting-switches",
                     "team-manufacturing-engineering", "team-production-control", "team-design-for-manufacturing",
                     "team-end-of-line-test", "team-supplier-quality", "team-triage"]


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
        text = "Updating group permissions for " + user_obj.profile.login + "\n"
        output_txt.write(text)

        # - Get user's groups from Okta
        user_groups = of.run_async(of.getUsersGroups(user_obj.id))

        # - Extract group IDs from user's groups as a list for reference
        user_group_ids = []
        for group in user_groups:
            user_group_ids.append(group.id)

        # - Iterate through target groups and add user to any that are missing
        for group in target_groups:
            group_id = group_library[group]
            # -- Check if user is already in group
            if group_id in user_group_ids:
                text = user_obj.profile.login + " is already a member of " + group.profile.name + ". Skipping.\n"
                output_txt.write(text)
                continue
            # -- If user is not in group, try adding user to group
            else:
                text = "Attempting to add " + user_obj.profile.login + " to " + group.profile.name + "... "
                output_txt.write(text)
                err = of.run_async(of.userAddGroup(group, user_obj))   # Note: userAddGroup takes group obj and user obj as input
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

