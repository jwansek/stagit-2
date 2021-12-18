import subprocess
import os

repo_name = input("Input repository name: ")
repo_path = os.path.join("/", "srv", "git", repo_name + ".git")

if os.path.exists(repo_path):
    print("ERROR: A repository with that name already exists. Please try another")
    exit()

os.mkdir(repo_path)
cwd = os.getcwd()

os.chdir(repo_path)
subprocess.run(["git", "init", "--bare"])

description = input("Input repository description: ")
with open(os.path.join(repo_path, "description"), "w") as f:
    f.write(description)

author = input("Input repository author: ")
with open(os.path.join(repo_path, "author"), "w") as f:
    f.write(author)

with open(os.path.join(repo_path, "url"), "w") as f:
    f.write("git@eda.gay:" + repo_name)

# user input in an executed string? YIKES
#   to run this you have to have ssh access anyway soo....
#       still bad form though tbh
subprocess.run(["ssh", "git@192.168.1.92", "cd /media/git/html/ && mkdir %s && cd %s && stagit ../../%s.git/" % (repo_name, repo_name, repo_name)])

with open(os.path.join(repo_path, "hooks", "post-receive"), "w") as f:
    f.write("#!/bin/sh\n\n")
    f.write("ssh git@192.168.1.92 'cd /media/git/html/%s && stagit ../../%s.git/'\n" % (repo_name, repo_name))
    f.write("python3 /home/git/remake_index.py\n") 

os.chdir(cwd)

import remake_index

accessstr = "git@git.eda.gay:" + str(repo_path)

subprocess.run(["ln", "-s", repo_path, repo_name])
subprocess.run(["ln", "-s", repo_path, repo_name + ".git"])

print("""
Repository created. You can now clone or add remote:
    git remote add other %s
                         %s
    git clone %s
    """ % (accessstr, "git@eda.gay:" + repo_name, accessstr))
