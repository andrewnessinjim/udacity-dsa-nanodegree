# Lookup if user belongs to a group
This document explains the requirements for the problem and design decisions behind the solution in `problem_4.py` file.

## Requirement
In Windows Active Directory, a group can consist of user(s) and group(s) themselves. We can construct this hierarchy as such. Write a function that provides an efficient look up of whether the user is in a group.

## Active Directory Simplified
In a real active directory, we would have a single reference for the entire directory and we can add users and groups using only that reference. For example, if we say `windows_active_directory` is the reference name, we would have code like this:
```
windows_active_directory.add_user_to_group(user, group)
windows_active_directory.is_user_in_group(user, group)
windows_active_directory.add_child_group(parent_group, child_group)
```

This would have needed a different kind of data structure and it would also prevent circular group relationships. But in this problem, we are assuming that we have reference to each group and there are no circular relationships. This means we already have the reference to the group in which we want to search and we focus on optimizing the lookup only.

## Time Complexity
Each group stores its users as a set, so the lookup time for checking if a user is directly under the given group is `O(1)`.

If the user is not present directly under the given group, then we iterate each of its sub groups. This is because the active directory is organized in a hierarchy. For example, let's consider 2 groups in an office - manager and employee. Every manager is also an employee, but an employee is not always a manager. So we make manager  a child group for employee group. Then, when we check if manager is an employee, the first lookup directly under employee group will be false, but checking the child group manager will return true. This means manager is an employee. But when we check if non-manager employee is a manager, it would result in a false because such an employee would not be present under manager group or any of manager's sub groups.

In the worst case, the user is not in any group (or in the bottom most group) and we start at the top of the hierarchy and hit every group when its organized in a linear fashion. If `n` is the number of groups, then the overall complexity is `O(n)` because looking up an user in a group takes constant time.

## Space Complexity
The algorithm to search does not require any space. It simply reads the provided group and user parameters. However, the data structures themselves need space. If there are `n` groups and `m` users, then the total space required will be `O(n + m)`. This is because each unique group and user exists only once in memory. Only their references are stored in the hierarchy, which might be more than once. Storing references does not contribute to space complexity.