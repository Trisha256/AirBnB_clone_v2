from fabric import task
from fabric.operations import run, sudo
from fabric.context_managers import cd, lcd
from datetime import datetime
import os

env.hosts = ['<IP web-01>', '<IP web-02>']
env.user = '<your-username>'
env.key_filename = '/path/to/your/private/key.pem'

@task
def do_clean(number=0):
    """Deletes out-of-date archives."""
    number = int(number)
    if number < 0:
        return

    with lcd("versions"):
        local("ls -t | tail -n +{} | xargs rm -rf".format(number + 1))

    with cd("/data/web_static/releases"):
        run("ls -t | tail -n +{} | xargs rm -rf".format(number + 1))

@task
def deploy():
    """Create and distribute the archive to the web servers."""
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)