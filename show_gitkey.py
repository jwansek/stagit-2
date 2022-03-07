import configparser

gitconf = configparser.ConfigParser()
gitconf.read("/srv/git/github.conf")

print("git remote add github https://%s:%s@github.com/%s/" % (gitconf.get("github", "user"), gitconf.get("github", "key"), gitconf.get("github", "user")))
