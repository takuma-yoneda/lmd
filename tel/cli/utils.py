#!/usr/bin/env python3
import subprocess

def rsync(source_dir, target_dir, options=''):
    import shutil
    # make sure rsync is installed
    if shutil.which("rsync") is None:
        raise RuntimeError("rsync binary is not found.")
    # ---
    print(f"Syncing code...")
    source_dir = str(source_dir).rstrip('/') + '/'
    target_dir = str(target_dir).rstrip('/') + '/'

    cmd = f"rsync --archive --compress {options} {source_dir} {target_dir}"
    print('running command', cmd)
    run_cmd(cmd, shell=True)
    print("Sync finished!")


def run_cmd(cmd, get_output=False, shell=False):

    if shell and isinstance(cmd, (list, tuple)):
        cmd = " ".join([str(s) for s in cmd])

    if get_output:
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=shell)
        proc.wait()
        if proc.returncode != 0:
            msg = "The command {} returned exit code {}".format(cmd, proc.returncode)
            raise RuntimeError(msg)
        out = proc.stdout.read().decode("utf-8").rstrip()
        print(out)
        return out
    else:
        res = subprocess.run(cmd, shell=shell)
        return res.returncode
