from fabric.api import env, local, put, run
from datetime import datetime
from os import path

env.hosts = ['32.231.168.90', '3.233.54.196']

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

def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    Args:
        archive_path: Path to the local archive to be uploaded
    """
    if not path.exists(archive_path):
        return False

    compressed_file = archive_path.split("/")[-1]
    file_name = compressed_file.split(".")[0]
    upload_path = "/tmp/{}".format(compressed_file)

    if put(archive_path, upload_path).failed:
        return False

    current_release = '/data/web_static/releases/{}'.format(file_name)

    run("mkdir -p {}".format(current_release))
    run("tar -xzf {} -C {}".format(upload_path, current_release))
    run("rm {}".format(upload_path))
    run("mv {}/web_static/* {}/".format(current_release, current_release))
    run("rm -rf {}/web_static".format(current_release))
    run("rm -rf /data/web_static/current")
    run("ln -s {} /data/web_static/current".format(current_release))

    return True

def deploy():
    """
    Creates and distributes an archive to web servers
    """
    archive_path = do_pack()
    if archive_path is None:
        return False

    return do_deploy(archive_path)