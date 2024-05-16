#!/usr/bin/python3
""" a Fabric script (based on the file 1-pack_web_static.py) that distributes..
    ..an archive to your web servers, using the function do_deploy: """


from fabric.api import *
from datetime import datetime
from os.path import exists


env.hosts = ['35.237.166.125', '54.167.61.201']  # <IP web-01>, <IP web-02>
# ^ All remote commands must be executed on your both web servers
# (using env.hosts = ['<IP web-01>', 'IP web-02'] variable in your script)


def do_deploy(archive_path):
    """ distributes an archive to my web servers
    """
    if exists(archive_path) is False:
        return False  # Returns False if the file at archive_path doesnt exist
    filename = archive_path.split('/')[-1]
    # so now filename is <web_static_2021041409349.tgz>
    no_tgz = '/data/web_static/releases/' + "{}".format(filename.split('.')[0])
    # curr = '/data/web_static/current'
    tmp = "/tmp/" + filename

    try:
        put(archive_path, "/tmp/")
        # ^ Upload the archive to the /tmp/ directory of the web server
        run("mkdir -p {}/".format(no_tgz))
        # Uncompress the archive to the folder /data/web_static/releases/
        # <archive filename without extension> on the web server
        run("tar -xzf {} -C {}/".format(tmp, no_tgz))
        run("rm {}".format(tmp))
        run("mv {}/web_static/* {}/".format(no_tgz, no_tgz))
        run("rm -rf {}/web_static".format(no_tgz))
        # ^ Delete the archive from the web server
        run("rm -rf /data/web_static/current")
        # Delete the symbolic link /data/web_static/current from the web server
        run("ln -s {}/ /data/web_static/current".format(no_tgz))
        # Create a new the symbolic link /data/web_static/current on the
        # web server, linked to the new version of your code
        # (/data/web_static/releases/<archive filename without extension>)
        return True
    except:
        return False
"""
Fabric script that distributes an archive to your web servers, using the do_deploy function
"""
from fabric.api import env, put, run
from os import path

env.hosts = ["34.231.110.206", "3.239.57.196"]


def do_deploy(archive_path):
    """
    It distributes archives to web servers
    """
    if not path.exists(archive_path):
        return False
    compressedFile = archive_path.split("/")[-1]
    fileName = compressedFile.split(".")[0]
    upload_path = "/tmp/{}".format(compressedFile)
    if put(archive_path, upload_path).failed:
        return False
    current_release = '/data/web_static/releases/{}'.format(fileName)
    if run("rm -rf {}".format(current_release)).failed:
        return False
    if run("mkdir -p {}".format(current_release)).failed:
        return False
    uncompress = "tar -xzf /tmp/{} -C {}".format(
        compressedFile, current_release
    )
    if run(uncompress).failed:
        return False
    delete_archive = "rm -f /tmp/{}".format(compressedFile)
    if run(delete_archive).failed:
        return False
    if run("rm -rf /data/web_static/current").failed:
        return False
    relink = "ln -s {} /data/web_static/current".format(current_release)
    if run(relink).failed:
        return False
    return True