# Recursive search for files with given suffix

This document explains the requirements for the problem and design decisions behind the solution in `problem_2.py` file.

## Requirement
Given a directory, find all the files with a given suffix in that directory and all its nested directories . Nesting maybe up to any level.

## Algorithm
```
 1: ALGORITHM find_files(suffix, path)
 2:     files_with_suffix = empty list
 3:     files_and_directories = all files and directories in path
 4:     for each item in files_and_directories:
 5:        if item is a file and ends with suffix
 6:            add item to files_with_suffix list
 7:        else if item is a directory
 8:            subfiles_with_suffix = find_files(suffix, item) //Recursive call
 9:            add all files in subfiles_with_suffix to files_with_suffix
10:    return files_with_suffix
```

## Explanation And Time Complexity
We first iterate through all the items in the given directory. When we find a file with the given suffix, we add it to our `main output list`. When we find a directory, we recursively call the same algorithm on this subdirectory. The subdirectory now becomes the given directory in the recursive call. The output from this recursive call is merged with the `main output list` and returned as the final output.

Let's say each directory can have `n` items and the depth of nesting of directories can be up to `d` levels, in the worst case. All the items at the final level should still be files, otherwise the algorithm will never end. Also, this is not a valid scenario as every file system have a limit on the path length.

Now, each directory has `n` items. The first call will iterate `n` items. Since each of these are directories in the worst case, there would be `n` recursive calls. Similarly, each call will spawn another `n` recursive calls till the depth `d` is reached. For example, when `n=3` and `d=3`, the file system (and our recursive calls) would look like this:
```
inputdir
├───folder1
│   ├───folder11
│   │       file1.txt
│   │       file2.txt
│   │       file3.txt
│   │
│   ├───folder12
│   │       file1.txt
│   │       file2.txt
│   │       file3.txt
│   │
│   └───folder13
│           file1.txt
│           file2.txt
│           file3.txt
│
├───folder2
│   ├───folder21
│   │       file1.txt
│   │       file2.txt
│   │       file3.txt
│   │
│   ├───folder22
│   │       file1.txt
│   │       file2.txt
│   │       file3.txt
│   │
│   └───folder23
│           file1.txt
│           file2.txt
│           file3.txt
│
└───folder3
    ├───folder31
    │       file1.txt
    │       file2.txt
    │       file3.txt
    │
    ├───folder32
    │       file1.txt
    │       file2.txt
    │       file3.txt
    │
    └───folder33
            file1.txt
            file2.txt
            file3.txt
```

At first level, there are 3 calls (or `3^1` calls) - folder1, folder2, folder3. At second level, there are 9 calls (or `3^2` calls) - folder11, folder12, folder13, folder21, folder22, folder23, folder31, folder32, folder33. At third level, there are no recursive calls, but there are 27 files (or `3^3` files) to be iterated. Overall, this would be:
>  `(3^1) + (3^2) + (3^3)`. 

In general, we could say the time complexity is:
> `O ((n^1) + (n^2) + ...... + (n^d))`

Even though this tells us the number of method calls and iterations, it does not give us an accurate picture of the time complexity. The complexity according to this analysis is exponential growth, but we know we are checking each item only once. So its more accurate to consider `n` as the total number of files and directories in the entire hierarchy. And since we're visiting each item exactly once, its more appropriate to say the time complexity is `O(n)`.

## Space Complexity

If `n` is the total number of items in the entire hierarchy, `n1` is the number of files and `n2` is the number of directories, then `n = n1 + n2`. Each of the `n2` directories needs a recursive call, which needs a proportional amount of space on the call stack. Each of the `n1` files are also tracked in an array. So arrays and the call stack need `n1 + n2` space in total. So overall space complexity is `O(n)`.

## References
[Markdown Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)  
[Python `os.path` module](https://docs.python.org/3/library/os.path.html#module-os.path)