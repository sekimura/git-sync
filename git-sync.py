#!/usr/bin/env python

import os
import sys
import signal
import urlparse
import subprocess


def _run_shell(cmd, timeout=30):
    """ running a shell to excecute commands passed in """
    try:
        signal.signal(signal.SIGALRM, signal.SIG_IGN)
        signal.alarm(timeout)
        output = subprocess.check_output(
            cmd,
            shell=True,
            stderr=subprocess.STDOUT,
        )
        if output:
            print 'OUTPUT: %s' % output
    except subprocess.CalledProcessError, e:
        sys.stderr.write("ERROR: %s\n" % str(e))
    finally:
        signal.signal(signal.SIGALRM, signal.SIG_DFL)
        signal.alarm(0)


def sync(url, basedir, path=None):
    """ sync git repository to local """
    u = urlparse.urlparse(url)

    if path is None:
        repo = "%s%s" % (u.netloc, u.path)
        path = os.path.join(basedir, repo)

    cmd = "git clone -q --mirror %s %s 2>&1" % (url, path)
    if os.path.exists(path):
        cmd = ("(cd %s; git fetch -q --tags -f origin "
               "'refs/heads/*:refs/heads/*') 2>&1" % (path,))
    _run_shell(cmd)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--basedir', required=True)
    parser.add_argument('urls', metavar='repo-url', nargs='*')
    args = parser.parse_args()

    if len(args.urls) == 1 and args.urls[0] == '-':
        for url in sys.stdin:
            url = url.rstrip()
            sync(url, args.basedir)
    else:
        for url in args.urls:
            sync(url, args.basedir)
