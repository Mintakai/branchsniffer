import re
import sys
from tkinter import filedialog
from tkinter import *
from pygit2 import Repository, GitError
from pygit2 import *
import os

def get_repo_path() -> str:
    "Get the repository path from user input or exit if canceled"
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

def get_branch_name() -> str:
    "Get the current active shorthand branch name as a string"
    try:
        repo = Repository(REPO_PATH)
    except (GitError):
        return False
    head = repo.head
    return head.shorthand

def update_repo():
    "Continuously check for the branch name, updating main_text in main_window accordingly along with the background color"
    branch_name = get_branch_name()
    main_text.configure(text=f"Currently selected branch: {branch_name}")
    main_text.configure(bg="red") if determine_master(branch_name) else main_text.configure(bg="green")
    main_window.after(1000, update_repo)

def determine_master(branch_name: str) -> bool:
    "Determine if the active branch is master/main or not"
    return True if (re.search(r'\bmaster\b', branch_name) or re.search(r'\bmain\b', branch_name)) else False

branch_name = get_branch_name()

main_text = Label(main_window, text=f"Currently selected branch: {branch_name}")
main_text.configure(font=("Segoe UI", 18), bg="grey")
main_text.pack()

update_repo()

main_window.mainloop()