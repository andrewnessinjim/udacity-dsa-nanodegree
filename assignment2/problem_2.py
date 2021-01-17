import os

def find_files(suffix, path):
    files_with_suffix = []

    for item in os.listdir(path):
        relative_path = os.path.join(path,item)
        if os.path.isfile(relative_path) and relative_path.endswith("."+suffix):
            files_with_suffix.append(relative_path)
        elif os.path.isdir(relative_path):
            subfiles_with_suffix = find_files(suffix, relative_path)
            files_with_suffix.extend(subfiles_with_suffix)

    return files_with_suffix

"""
Test case 1: There are four .c files in the entire hierarchy at different levels of nesting. All these four files must be returned by the function:
1. problem_2_testdir\subdir1\a.c
2. problem_2_testdir\subdir3\subsubdir1\b.c
3. problem_2_testdir\subdir5\a.c
4. problem_2_testdir\t1.c
"""
c_files = find_files("c", "problem_2_testdir")
assert len(c_files) == 4
for file in c_files:
    assert file.endswith(".c")


"""
Test case 2: There are no files that ends with cpp. So the function should not return any files
"""
cpp_files = find_files("cpp", "problem_2_testdir")
assert len(cpp_files) == 0

"""
Test case 3: There is two files that has no filename, but only extention. They are ".gitkeep" files. They should be returned by the function
"""
gitkeep_files = find_files("gitkeep", "problem_2_testdir")
assert len(gitkeep_files) == 2
for file in gitkeep_files:
    assert file.endswith(".gitkeep")