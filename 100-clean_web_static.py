#!/usr/bin/python3
"""
This fabric script deletes out-of-date archives, using the do_clean function
"""
from fabric.api import cd, env, local, run
import os

env.hosts = ["33.244.168.90", "3.235.49.196"]


def do_clean(number=0):
    """
    it deletes out-of-date archives
    Args:
        number: is the number of the archives, including the recent
    """
    n = 1 if int(number) == 0 else int(number)
    files = [f for f in os.listdir('./versions')]
    files.sort(reverse=True)
    for f in files[n:]:
        local("rm -f versions/{}".format(f))
    remote = "/data/web_static/releases/"
    with cd(remote):
        tgz = run(
            "ls -tr | grep -E '^web_static_([0-9]{6,}){1}$'"
        ).split()
        tgz.sort(reverse=True)
        for d in tgz[n:]:
            run("rm -rf {}{}".format(remote, d))
