from fabric.api import local
from datetime import datetime
from os import path


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder
    """
    current_time = datetime.now()
    archive_name = "web_static_{}{}{}{}{}{}.tgz".format(
        current_time.year,
        current_time.month,
        current_time.day,
        current_time.hour,
        current_time.minute,
        current_time.second
    )

    if not path.isdir("versions"):
        local("mkdir -p versions")

    archive_path = "versions/{}".format(archive_name)

    tar_command = "tar -cvzf {} web_static".format(archive_path)
    if local(tar_command).failed:
        return None

    return archive_path