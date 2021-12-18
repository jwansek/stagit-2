import subprocess
import os

initdir = os.path.join("/", "home", "git", "git")
remote_git = os.path.join("/", "media", "git")

dirs = []
for dir_ in os.listdir(initdir):
    full_dir = os.path.join(initdir, dir_)
    if os.path.isdir(full_dir) and str(full_dir).endswith(".git"):
        dirs.append(str(os.path.join(remote_git, dir_)))

cmd = "stagit-index %s > %s" % (" ".join(dirs), str(os.path.join(remote_git, "html", "index.html")))

#print(cmd)
subprocess.run(["ssh", "git@192.168.1.92", cmd])
print("Rebuilt HTML index...")
