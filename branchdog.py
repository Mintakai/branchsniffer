import re
import sys
from tkinter import filedialog
from tkinter import *
from pygit2 import Repository, GitError
from pygit2 import *
import os

# Get the repository path from user input or exit if canceled
def get_repo_path() -> str:
    while (True):
        repo_path = filedialog.askdirectory(initialdir=os.path.normpath("C:\\"), title="Please select a repository to watch!")
        if (discover_repository(repo_path)):
            break
        elif (repo_path == ''):
            sys.exit()
    return repo_path

REPO_PATH = get_repo_path()
title = REPO_PATH.split('/')

main_window = Tk()
main_window.title(f"Repo: {title[-1]}")
main_window.attributes('-topmost', True)

# Get the current active shorthand branch name as a string
def get_branch_name() -> str:
    try:
        repo = Repository(REPO_PATH)
    except (GitError):
        return False
    head = repo.head
    return head.shorthand

# Continuously check for the branch name, updating main_text in main_window accordingly along with the background color
def update_repo():
    branch_name = get_branch_name()
    main_text.configure(text=f"Currently selected branch: {branch_name}")
    main_text.configure(bg="red") if determine_master(branch_name) else main_text.configure(bg="green")
    main_window.after(1000, update_repo)

# Determine if the active branch is master/main or not
def determine_master(branch_name: str) -> bool:
    return True if (re.search(r'\bmaster\b', branch_name) or re.search(r'\bmain\b', branch_name)) else False

branch_name = get_branch_name()

main_text = Label(main_window, text=f"Currently selected branch: {branch_name}")
main_text.configure(font=("Segoe UI", 18), bg="grey")
main_text.pack()

update_repo()

main_window.mainloop()