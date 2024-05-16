from fabric.api import env, put, run
from os import path

env.hosts = ['<IP web-01>', '<IP web-02>']  # Update with your web server IPs


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