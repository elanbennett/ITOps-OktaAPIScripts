# == Imports == #
from Functions import report_functions as rf, okta_functions as of
import time
from datetime import date
today = date.today().strftime("%m%d%Y")

if __name__ == '__main__':
    target_users = ["elan@canoo.com"]
    for login in target_users:
        user_obj = of.run_async(of.getUser(login))

        # Check if user in groups
        user_groups = of.run_async(of.getUsersGroups(user_obj.profile.login))
        print(user_groups)


