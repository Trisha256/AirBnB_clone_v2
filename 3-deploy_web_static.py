#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers, using the do_deploy function
"""
from fabric.api import env, local, put, run
from os import path
from datetime import datetime

env.hosts = ["32.231.168.90", "3.233.54.196"]


def do_pack():
    """
    This function generates an archive file
    """
    dat = datetime.now()
    arc = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        dat.year, dat.month, dat.day,
        dat.hour, dat.minute, dat.second
    )
    if not path.isdir("versions"):
        if local("mkdir versions").failed:
            return None
    cmd = "cd web_static && tar -cvzf ../{} . && cd -".format(archive)
    if local(cmd).succeeded:
        return archive
    return None


def do_deploy(arc_path):
    """
    Distributes arc to web servers
    Args:
        archive_path: path to local archive to be uploaded
    """
    if not path.exists(arc_path):
        return False
    compressedFile = arc_path.split("/")[-1]
    fileName = compressedFile.split(".")[0]
    upload_path = "/tmp/{}".format(compressedFile)
    if put(archive_path, upload_path).failed:
        return False
    current_release = '/data/web_static/releases/{}'.format(fileName)
    if run("rm -rf {}".format(current_release)).failed:
        return False
    if run("mkdir {}".format(current_release)).failed:
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


def deploy():
    """
    it creates and distributes an archive to your web servers
    """
    arc_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(arc_path)
