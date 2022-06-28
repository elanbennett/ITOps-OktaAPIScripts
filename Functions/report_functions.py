from Functions.oktaservice import okta_client as client # Connect to Okta API
from Functions import okta_functions as afunc
import os
import asyncio
import nest_asyncio
from datetime import date
import csv
nest_asyncio.apply()
today = date.today().strftime("%m%d%Y")


# List user group data given a Group ID
async def listGroupUsers(group_id):
    group, resp, err = await client.get_group(group_id)  # Get group using ID
    members, resp, err = await client.list_group_users(group_id)  # Get group members using group object
    user_list = []  # User list to be exported
    # Get users and append to list, then get next page
    while True:
        for user in members:
            line = [user.profile.first_name, user.profile.last_name, user.profile.login, user.id, group.profile.name,
                    group.id, today]  # Data for csv
            user_list.append(line)
            print(line)
        # Get next page if there is one
        if resp.has_next():
            members, err = await resp.next()
        else:
            break
    print(group.profile.name, "- Members:", len(user_list))
    return user_list


# List user group data based on a defined list of users
async def getGroupsInList(users):
    print("Getting groups for list of users...")
    data = []
    for user in users:
        users_groups = await afunc.getUsersGroups(user.id)
        for group in users_groups:
            line = [user.profile.first_name, user.profile.last_name, user.profile.login, user.id, group.profile.name,
                    group.id, today]  # Data for csv
            data.append(line)
    return data


# Report that returns the user type of all users
async def listAllUsersTypes():
    users, resp, err = await client.list_users()
    data = []  # data to be exported
    user_types = {
        "abc": "Contractor",
        "def": "External",
        "ghi": "Intern",
        "jkl": "Service",
        "mno": "User"
    }
    while True:
        for user in users:
            if user.type.id in user_types.keys():
                type = user_types[user.type.id]
            else:
                type = "None"
            line = [user.profile.first_name, user.profile.last_name, user.profile.login, type]  # Data for csv
            print(line)
            data.append(line)
        # Get next page if there is one
        if resp.has_next():
            users, err = await resp.next()
        else:
            break
    return data


# Get list of all groups and then return group membership for each group
def getSnapshotByGroups():
    data = []
    # Get all Groups
    groups = afunc.run_async(afunc.getAllGroups())

    # Pass to get group members
    for group in groups:
        users = afunc.run_async(afunc.getGroupUsers(group.id))
        data.extend(users)
    return data


# Get list of all users and then return group membership for each user
def getSnapshotByUsers():
    data = []
    group_list = afunc.getAllUsersAllGroups()
    for pair in group_list:
        user = pair["user"]
        group = pair["group"]
        line = [user.profile.first_name, user.profile.last_name, user.profile.login, user.id, group.profile.name,
                group.id, today]  # Data for csv
        data.append(line)
    return data


# Write data out to file as a CSV
def write_out(data, path, title):
    print("Writing out data...")
    if not os.path.exists(path):
        print("Out path doesn't exist. Creating directory...")
        os.mkdir(path)
    f = open(path + title, 'w', newline='')  #
    writer = csv.writer(f, delimiter=',')
    writer.writerows(data)
    f.close()
    print("Writing complete. Report located at:", path, ",", title)
