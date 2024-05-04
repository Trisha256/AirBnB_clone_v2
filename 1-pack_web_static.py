#!/usr/bin/python3
"""
This fabric script generates a .tgz archive from the web_static folder of your AirBnB Clone repo, using the do_pack function
"""

from os import path
from datetime import datetime
from fabric.api import local


def do_pack():
    """
    This function generates an archive
    """
    date = datetime.now()
    archive = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        date.year, date.month, date.day,
        date.hour, date.minute, date.second
    )
    if not path.isdir("versions"):
        if local("mkdir versions").failed:
            return None
    cmd = "cd web_static && tar -cvzf ../{} . && cd -".format(archive)
    if local(cmd).succeeded:
        return archive
    return None
