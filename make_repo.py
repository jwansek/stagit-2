import subprocess
import configparser
import datetime
import tempfile
import shutil
import jinja2
import os

repo_name = input("Input repository name: ").replace(" ", "_")
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

private = input("Would you like the repository to appear on the web version git.eda.gay? <y/n>: ").lower() == "n"

accessstr = "git@git.eda.gay:" + str(repo_path)
if input("Would you like the repository to remain bare? Useful for making mirrors of Github repos. <y/n>: ").lower() != "y": 
    with tempfile.TemporaryDirectory() as tempdir:
        subprocess.run(["git", "clone", accessstr, tempdir])
        os.chdir(tempdir)
   
        with open("README.md", "w") as f:
            f.write("# %s\n\n%s\n" % (repo_name, description))

        gitignore_templates_dir = "/home/eden/gitignore/"
        templates = sorted([f[:-10] for f in os.listdir(gitignore_templates_dir) if f.endswith(".gitignore")])
        templates.insert(0, "[None]")
        for i, template in enumerate(templates, 1):
            print("%3d: %-23s" % (i, template), end = "")
            if i % 4 == 0:
                print("")

        selected_index = int(input("\nSelect .gitignore template: "))
        if selected_index != 0:
            shutil.copy(os.path.join(gitignore_templates_dir, templates[selected_index - 1]) + ".gitignore", ".gitignore", follow_symlinks = True)

        licenses_templates_dir = "/home/eden/license-templates/templates/"
        templates = sorted([f[:-4] for f in os.listdir(licenses_templates_dir) if not f.endswith("-header.txt")])
        templates.insert(0, "[None]")
        for i, template in enumerate(templates, 1):
            print("%2d: %-22s" % (i, template), end = "")
            if i % 4 == 0:
                print("")
        
        selected_index = int(input("\nSelect license template: "))
        if selected_index != 0:
            with open(os.path.join(licenses_templates_dir, templates[selected_index - 1]) + ".txt", "r") as f:
                jinja_template = jinja2.Template(f.read())

            with open("LICENSE", "w") as f:
                f.write(jinja_template.render(**{
                    "year": str(datetime.datetime.today().year),
                    "organization": author,
                    "project": repo_name
                }))

        subprocess.run(["git", "add", "-A"])
        subprocess.run(["git", "commit", "-m", "Initialized repository"])
        subprocess.run(["git", "push", "origin", "master"])

# user input in an executed string? YIKES
#   to run this you have to have ssh access anyway soo....
#       still bad form though tbh
if not private:
    subprocess.run(["ssh", "git@192.168.1.92", "cd /media/git/html/ && mkdir %s && cd %s && stagit ../../%s.git/" % (repo_name, repo_name, repo_name)])

    with open(os.path.join(repo_path, "hooks", "post-receive"), "w") as f:
        f.write("#!/bin/sh\n\n")
        f.write("ssh git@192.168.1.92 'cd /media/git/html/%s && stagit ../../%s.git/'\n" % (repo_name, repo_name))
        f.write("python3 /home/git/remake_index.py\n") 
else:
    with open("/home/git/git/private_repos.txt", "a") as f:
        f.write("%s.git\n" % repo_name)

os.chdir(cwd)

import remake_index

subprocess.run(["ln", "-s", repo_path, repo_name])
subprocess.run(["ln", "-s", repo_path, repo_name + ".git"])

gitconf = configparser.ConfigParser()
gitconf.read("/srv/git/github.conf")

print("""
Repository created. You can now clone or add remote:
    git remote add other %s
                         %s
    git clone %s
And add github mirror (insecure method, keys are stored locally):
    git remote add github https://%s:%s@github.com/%s/%s
    """ % (accessstr, "git@eda.gay:" + repo_name, accessstr, gitconf.get("github", "user"), gitconf.get("github", "key"), gitconf.get("github", "user"),repo_name ))
