from oktaservice import okta_client as client  # Connect to Okta API
import os
import asyncio
import nest_asyncio
from datetime import date
import csv
nest_asyncio.apply()
today = date.today().strftime("%m%d%Y")


def getUser(uid):
    async def getUser(uid):
        user, resp, err = await client.get_user(uid)
        if user is None:
            print("User not found")
        else:
            print(user.profile.first_name, user.profile.last_name, "|", user.status)
        return user
    loop = asyncio.get_event_loop()
    user = loop.run_until_complete(getUser(uid))
    return user


# Get all users
def getAllUsers():
    async def getAllUsers():
        users, resp, err = await client.list_users()
        return users
    loop = asyncio.get_event_loop()
    all_users = loop.run_until_complete(getAllUsers())
    return all_users


# List all users types in your Org
def getAllUserTypes():
    async def getAllUserTypes():
        types, resp, err = await client.list_user_types()
        for item in types:
            print(item.display_name, ":", item.id)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getAllUserTypes())


# List all groups in Okta
def getAllGroups():
    async def getAllGroups():
        groups, resp, err = await client.list_groups()
        data = []  # List of groups
        counter = 0  # Number of groups
        while True:
            for group in groups:
                data.append(group)
                print(group.profile.name)
                counter += 1
            if resp.has_next():  # Pagination
                groups, err = await resp.next()
            else:
                break
        print("Number of groups: ", counter)
        return data
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(getAllGroups())
    return data


def getUsersGroups(uid):
    async def getUsersGroups():
        users_groups, resp, err = await client.list_user_groups(uid)
        return users_groups
    loop = asyncio.get_event_loop()
    users_groups = loop.run_until_complete(getUsersGroups())
    return users_groups


# List group membership of for all users
def getAllUsersAllGroups():
    async def getAllUsersAllGroups():
        users, resp, err = await client.list_users()
        data = []  # data to be exported
        while True:
            for user in users:
                users_groups, resp, err = await client.list_user_groups(user.id)
                for group in users_groups:
                    line = [group.profile.name, user.profile.first_name, user.profile.last_name, user.profile.login, today]  # Data for csv
                    print(line)
                    data.append(line)
            # Get next page if there is one
            if resp.has_next():
                users, err = await resp.next()
            else:
                break
        return data
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(getAllUsersAllGroups())
    return data


# Report that returns the user type of all users
def getAllUsersTypes():
    async def getAllUsersTypes():
        users, resp, err = await client.list_users()
        data = []  # data to be exported
        user_types = {
            "oty3ggscsu5eeMNAK357": "Contractor",
            "oty3ggs8w3wwpom8H357": "External",
            "oty3ggre21K20cIdq357": "Intern",
            "oty5lxu0qy0SnQNXh357": "Service",
            "otypj558oQU4274DR356": "User"
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
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(getAllUsersTypes())
    return data


# Get user type of individual user
def getUserType(id):
    async def getUserType():
        type, resp, err = await client.get_user_type(id)
        print(type)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getUserType())


# Get all users given a group ID
def getGroupUsers(group_id):
    async def getGroupUsers():
        group, resp, err = await client.get_group(group_id)  # Get group using ID
        members, resp, err = await client.list_group_users(group_id)  # Get group members using group object
        records = 0  # Track number of members
        user_list = []  # User list to be exported

        # Get users and append to list, then get next page
        while True:
            for user in members:
                line = [group.profile.name, user.profile.first_name, user.profile.last_name, user.profile.login, today]  # Data for csv
                user_list.append(line)
                print(line)
                records += 1

            # Get next page if there is one
            if resp.has_next():
                members, err = await resp.next()
            else:
                break
        print(group.profile.name, "- Members:", records)
        return user_list
    loop = asyncio.get_event_loop()
    user_list = loop.run_until_complete(getGroupUsers())  # save function output
    return user_list  # return function output


def getGroupsInList(users):
    async def getGroupsInList():
        for user in users:
            users_groups, resp, err = await client.list_user_groups(user.id)
            for group in users_groups:
                print(today, ",", group.profile.name, ",", user.profile.first_name, ",", user.profile.last_name)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(getGroupsInList())


def getDeactivatedUsers():
    async def getDeactivatedUsers():
        total = 0
        d_users = []
        query_parameters = {'limit': '200', 'filter': 'status eq "DEPROVISIONED"'}
        users, resp, err = await client.list_users(query_parameters)
        # Iterate through all of the rest of the pages
        while True:
            print(len(users))
            for user in users:
                # if user.status.value == 'DEPROVISIONED': # -- Redundant Check
                print(user.profile.first_name, user.profile.last_name, "|", user.status)
                d_users.append(user)
                total += 1
            if resp.has_next():
                users, err = await resp.next()
            else:
                break

        print("\n", "Total count:", total)
        return d_users
    loop = asyncio.get_event_loop()
    d_users = loop.run_until_complete(getDeactivatedUsers())
    return d_users


def userRemoveGroup(group, user):
    async def userRemoveGroup():
        resp, err = await client.remove_user_from_group(group.id, user.id)
        print(resp)
        if err is None:
            print("Successfully removed", user.profile.login, "from group", group.profile.name)
        else:
            print(err)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(userRemoveGroup())


def userRemoveAllGroups(user):
    async def userRemoveAllGroups():
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
    loop = asyncio.get_event_loop()
    loop.run_until_complete(userRemoveAllGroups())


def getAppUserName(appid, userid):  # Using to check username of App User
    async def getAppUserName():
        appuser, resp, err = await client.get_application_user(appid, userid)
        try:
            username = appuser.credentials.user_name
            print(username)
        except:
            username = None
            print(username)
        return username
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getAppUserName())


def getAppUsers(appid):
    async def getAppUsers():
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
    loop = asyncio.get_event_loop()
    userIDs = loop.run_until_complete(getAppUsers())
    return userIDs


# https://developer.okta.com/docs/reference/api/apps/#update-application-credentials-for-assigned-user
def updateAppUserCreds(appid, uid, user_name):
    async def updateAppUserCreds():
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
    loop = asyncio.get_event_loop()
    loop.run_until_complete(updateAppUserCreds())


# https://developer.okta.com/docs/reference/api/apps/#update-application-credentials-for-assigned-user
def updateAppUserProfile(appid, uid, user_name):
    async def updateAppUserProfile():
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
    loop = asyncio.get_event_loop()
    loop.run_until_complete(updateAppUserProfile())


def getUserSchema(userid):
    async def getUserSchema():
        schema, resp, err = await client.get_user_schema()
        print(schema)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getUserSchema())


def getSnapshot():
    data = []
    # Get all Groups
    groups = getAllGroups()

    # Pass to get group members
    for group in groups:
        users = getGroupUsers(group.id)
        data.extend(users)
    return data


def write_out(data, path, title):
    f = open(path + title, 'w', newline='')  #
    writer = csv.writer(f, delimiter=',')
    writer.writerows(data)
    f.close()
