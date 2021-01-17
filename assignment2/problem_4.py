class Group(object):
    def __init__(self, _name):
        self.name = _name
        self.groups = []
        self.users = set()

    def add_group(self, group):
        self.groups.append(group)

    def add_user(self, user):
        self.users.add(user)

    def get_groups(self):
        return self.groups

    def get_users(self):
        return self.users

    def get_name(self):
        return self.name

def is_user_in_group(user, group: Group):
    """
    Return True if user is in the group, False otherwise.

    Args:
      user(str): user name/id
      group(class:Group): group to check user membership against
    """
    if user in group.get_users():
        return True
    
    for group in group.get_groups():
        user_found = is_user_in_group(user, group)
        if user_found:
            return True

    return False

"""
We will create a sample hierarchy for testing the is_user_in_group function.
We will have 4 employees who are at the bottom of the hierarchy - e1, e2, e3 and e4
We will have 2 managers - m1 is the manager for e1 and e2, m2 is the manager for e3 and e4
We will have 1 ceo - ceo1 is above m1 and m2

Ceo is an employee and a manager as well. A manager is an employee as well. Just employees are
neither managers nor the ceo.
"""

# Create the groups
emp_grp = Group("employee")
mgr_grp = Group("manager")
ceo_grp = Group("ceo")

#Establish the hierarchy for the groups
emp_grp.add_group(mgr_grp) #Because managers are also employees
mgr_grp.add_group(ceo_grp) #Because Ceo is also a manager

#Create the users
e1="e1"
e2="e2"
e3="e3"
e4="e4"
m1="m1"
m2="m2"
ceo="ceo"

#Add users to their respective groups
emp_grp.add_user(e1)
emp_grp.add_user(e2)
emp_grp.add_user(e3)
emp_grp.add_user(e4)

mgr_grp.add_user(m1)
mgr_grp.add_user(m2)

ceo_grp.add_user(ceo)

assert is_user_in_group(ceo, emp_grp) == True # Because everybody is an employee, which includes the ceo
assert is_user_in_group(e1, ceo_grp) == False # Because not all employees are ceos
assert is_user_in_group(ceo, mgr_grp) == True # Because ceo is also a manager
assert is_user_in_group(m2, emp_grp) == True # Because everybody is an employee, which includes all the managers

stranger = "stranger"
assert is_user_in_group(stranger, emp_grp) == False # Because strangers don't belong to any group