# =======================================================================
# Version 1.0
# -----------------------------------------------------------------------
# Last changed by: Elan Bennett
# -----------------------------------------------------------------------
# 1.0 Changes:
# Completed testing and addition of bulk group deletion processes.
# =======================================================================

# == Imports == #
from Functions import okta_functions_old
import time
from datetime import date
today = date.today().strftime("%m%d%Y")

if __name__ == '__main__':
    st = time.time()
    # === REMOVE ALL GROUPS FROM DEPROVISIONED USERS === #
    d_users = okta_functions_old.getDeactivatedUsers()
    for user in d_users:
        okta_functions_old.userRemoveAllGroups(user)

    # functions.getGroupsInList(d_users)  # Checks groups for listed users, to confirm groups were removed correctly

    # === TRACK FUNCTION RUN TIME === #
    print("----%.2f----"%(time.time()-st))