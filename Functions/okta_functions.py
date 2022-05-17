from Functions.oktaservice import okta_client as client
import os
import asyncio
import nest_asyncio
from datetime import date
import csv
nest_asyncio.apply()
today = date.today().strftime("%m%d%Y")


# Define an async loop with a function and run until complete
def run_async(function):
    loop = asyncio.get_event_loop()
    output = loop.run_until_complete(function)
    return output

## ========================== ##
#        BASIC FUNCTIONS       #
## ========================== ##

# Get user data given a User ID
async def getUser(uid):
    print("Getting user data for", uid)
    user, resp, err = await client.get_user(uid)
    if user is None:
        print("User not found")
    else:
        print(user.profile.first_name, user.profile.last_name, "|", user.status)
    return user


# Get list of all users
async def getAllUsers():
    print("Getting list of all users...")
    all_users = []
    users, resp, err = await client.list_users()
    while True:
        all_users.extend(users)
        if resp.has_next():  # Pagination
            users, err = await resp.next()
        else:
            break
    print("Total users returned:", len(all_users))
    return all_users


# Get list of all custom user types
async def getAllUserTypes():
    print("Getting list of all custom user types...")
    types, resp, err = await client.list_user_types()
    for item in types:
        print(item.display_name, ":", item.id)
    return types


# Get list of all groups
async def getAllGroups():
    print("Getting list of all groups...")
    all_groups = []  # List of groups
    groups, resp, err = await client.list_groups()
    while True:
        all_groups.extend(groups)
        if resp.has_next():  # Pagination
            groups, err = await resp.next()
        else:
            break
    for group in all_groups:
        print(group.profile.name)
    print("Number of groups: ", len(all_groups))
    return all_groups


# Get group membership given a User ID
async def getUsersGroups(uid):
    print("Getting group membership for user", uid)
    groups, resp, err = await client.list_user_groups(uid)
    for group in groups:
        print(group.profile.name)
    return groups


# Get group membership for all users in a list of {user, group} dicts
async def getAllUsersAllGroups():
    print("Getting group membership for all users...")
    users, resp, err = await client.list_users()
    list = []
    while True:
        for user in users:
            users_groups = await getUsersGroups(user.id)
            for group in users_groups:
                group_pair = {"user": user, "group": group}
                print(group_pair)
                list.append(group_pair)
        # Get next page if there is one
        if resp.has_next():
            users, err = await resp.next()
        else:
            break
    return list


# Get user type of individual user
async def getUserType(uid):
    type, resp, err = await client.get_user_type(uid)
    print(uid, type)
    return type


# Get user schema given User ID
async def getUserSchema(uid):
    schema, resp, err = await client.get_user_schema(uid)
    print(schema)
    return schema


# Get list of users given a group ID
async def getGroupUsers(group_id):
    print("Getting list of user in group:", group_id)
    group, resp, err = await client.get_group(group_id)  # Get group using ID
    members, resp, err = await client.list_group_users(group_id)  # Get group members using group object
    user_list = []  # User list to be exported
    # Get users and append to list, then get next page
    while True:
        user_list.extend(members)
        # Get next page if there is one
        if resp.has_next():
            members, err = await resp.next()
        else:
            break
    print(group.profile.name, "has", len(user_list), "members.")
    return user_list


# Gets groups based on a defined list of users in a list of {user, group} dicts
async def getGroupsInList(users):
    print("Getting groups for list of users...")
    list = []
    for user in users:
        users_groups = await getUsersGroups(user.id)
        for group in users_groups:
            group_pair = {"user": user, "group": group}
            print(group_pair)
            list.append(group_pair)
    return list


# Get list of users given a status
# TODO: TEST FUNCTION
async def getUsersByStatus(status):
    print("Getting users that match status:", status, "...")
    s_users = []
    # Set query parameters for API call
    query_parameters = {'filter': 'status eq ' + status}
    users, resp, err = await client.list_users(query_parameters)
    while True:
        s_users.extend(users)
        for user in users:
            print(user.profile.first_name, user.profile.last_name, "|", user.status)
        if resp.has_next():
            users, err = await resp.next()
        else:
            break
    print("\n", "Total", status, "users:", len(s_users))
    return s_users


## ========================== ##
#       ADVANCED FUNCTIONS     #
## ========================== ##


# Get list of all users with Status: DEPROVISIONED
async def getDeactivatedUsers():
    print("Getting users that match status: DEPROVISIONED ...")
    d_users = []
    # Set query parameters for API call
    query_parameters = {'filter': 'status eq "DEPROVISIONED"'}
    users, resp, err = await client.list_users(query_parameters)
    while True:
        d_users.extend(users)
        for user in users:
            # if user.status.value == 'DEPROVISIONED': # -- Redundant Check
            print(user.profile.first_name, user.profile.last_name, "|", user.status)
        if resp.has_next():
            users, err = await resp.next()
        else:
            break
    print("\n", "Total DEPROVISIONED users:", len(d_users))
    return d_users


# Removes user from group given Group ID and User ID
async def userRemoveGroup(group, user):
    print("Attempting to remove", user.profile.login, "from group", group.profile.name)
    resp, err = await client.remove_user_from_group(group.id, user.id)
    print(resp)
    if err is None:
        print("Successfully removed", user.profile.login, "from group", group.profile.name)
    else:
        print(err)
    return(err)


async def userAddGroup(group, user):
    print("Attempting to add", user.profile.login, "to group", group.profile.name)
    resp, err = await client.add_user_to_group(group.id, user.id)
    if err is None:
        print("Successfully added", user.profile.login, "to group", group.profile.name)
    else:
        print(err)
    return(err)


async def userRemoveAllGroups(user):
    # == Create log file == #
    if not os.path.exists('../logs/'):
        os.mkdir('../logs/')
    title = 'userRemoveAllGroups_' + today
    output_txt = open(os.path.expanduser('logs/' + title + ".txt"), "a")
    text = "Attempting to remove groups for "+user.profile.first_name+" "+user.profile.last_name+" | "+user.status+"\n"
    output_txt.write(text)

    # == Get User Groups == #
    users_groups, resp, err = await client.list_user_groups(user.profile.login)

    # == Remove User from Groups ==#
    for group in users_groups:  # For each group in list
        resp, err = await client.remove_user_from_group(group.id, user.id)
        print(resp)
        if err is None:
            text = "Successfully removed "+user.profile.login+" from group "+group.profile.name+"\n"
            output_txt.write(text)
            print("Successfully removed", user.profile.login, "from group", group.profile.name)
        else:
            print(err)

    # == Close log file ==#
    output_txt.close()


# Using to check username of App User
async def getAppUserName(appid, userid):
    appuser, resp, err = await client.get_application_user(appid, userid)
    try:
        username = appuser.credentials.user_name
        print(username)
    except:
        username = None
        print(username)
    return username


async def getAppUsers(appid):
    query_parameters = {'limit': '200'}
    appusers, resp, err = await client.list_application_users(appid, query_parameters)
    userIDs = []
    while True:
        for user in appusers:
            if user.credentials is None:
                username = user.profile["email"]+" - No username"
            else:
                username = user.credentials.user_name
            userIDs.append(user.id)
            print(username)
        if resp.has_next():
            appusers, err = await resp.next()
        else:
            break
    return userIDs

#TODO: TEST FUNCTION
# https://developer.okta.com/docs/reference/api/apps/#update-application-credentials-for-assigned-user
async def updateAppUserCreds(appid, uid, user_name):
    # Specify user to be updated by embedding ids in request url
    url = '/api/v1/apps/'+appid+'/users/'+uid
    # Create request
    request, error = await client.get_request_executor().create_request(
        method='POST',
        url=url,
        body={
            "credentials": {
                "user_name": user_name
            }
        },
        headers={},
        oauth=False
    )
    print(request)
    print(error)


#TODO: TEST FUNCTION
# https://developer.okta.com/docs/reference/api/apps/#update-application-credentials-for-assigned-user
async def updateAppUserProfile(appid, uid, user_name):
    # Specify user to be updated by embedding ids in request url
    url = '/api/v1/apps/'+appid+'/users/'+uid
    # Create request
    request, error = await client.get_request_executor().create_request(
        method='POST',
        url=url,
        body={
            "profile": {
                "displayName": user_name
            }
        },
        headers={},
        oauth=False
    )
    print(request)
    print(error)




