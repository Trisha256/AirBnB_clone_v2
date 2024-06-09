#!/usr/bin/python3
"""
a Fabric script (based on the file 3-deploy_web_static.py)
that deletes out-of-date archives, using the function do_clean:
"""


from fabric.api import *
from datetime import datetime
from os.path import exists
import os.path


env.hosts = ['35.237.166.125', '54.167.61.201']  # <IP web-01>, <IP web-02>


def do_pack():
    """ Generates a .tgz archive from the contents of the web_static folder """
    local("sudo mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = "versions/web_static_{}.tgz".format(date)
    result = local("sudo tar -cvzf {} web_static".format(filename))
    if result.succeeded:
        return filename
    else:
        return None


def do_deploy(archive_path):
    """ Distributes an archive to the web servers """
    if not os.path.exists(archive_path):
        return False

    filename = archive_path.split('/')[-1]
    no_ext = "/data/web_static/releases/{}".format(filename.split('.')[0])
    tmp = "/tmp/{}".format(filename)

    try:
        put(archive_path, "/tmp")
        run("mkdir -p {}/".format(no_ext))
        run("tar -xzf {} -C {}/".format(tmp, no_ext))
        run("rm {}".format(tmp))
        run("mv {}/web_static/* {}/".format(no_ext, no_ext))
        run("rm -rf {}/web_static".format(no_ext))
        run("rm -rf /data/web_static/current")
        run("ln -s {}/ /data/web_static/current".format(no_ext))
        return True
    except Exception:
        return False


def deploy():
    """ Creates and distributes an archive to the web servers """
    new_archive_path = do_pack()
    if not os.path.exists(new_archive_path):
        return False
    result = do_deploy(new_archive_path)
    return result


def do_clean(number=0):
    """ Deletes out-of-date archives """
    number = int(number)
    if number < 0:
        return False
    if number == 0 or number == 1:
        number = 1
    else:
        number += 1

    with lcd("versions"):
        local("ls -t | tail -n +{} | xargs rm -rf".format(number))

    with cd("/data/web_static/releases"):
        run("ls -t | tail -n +{} | xargs rm -rf".format(number))

    with lcd("versions"):
        archives_count = int(local("ls -1 | wc -l", capture=True))
        to_delete = archives_count - number
        if to_delete > 0:
            local("ls -t | tail -n {} | xargs rm -rf".format(to_delete))

    with cd("/data/web_static/releases"):
        archives_count = int(run("ls -1 | wc -l"))
        to_delete = archives_count - number
        if to_delete > 0:
            run("ls -t | tail -n {} | xargs rm -rf".format(to_delete))


# Call the do_clean function with the desired number of archives to keep
do_clean(2)
