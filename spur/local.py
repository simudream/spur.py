import os
import subprocess
import shutil

from spur.tempdir import create_temporary_dir
from spur.files import FileOperations
    
class LocalShell(object):
    def upload_dir(self, source, dest, ignore=None):
        shutil.copytree(source, dest, ignore=shutil.ignore_patterns(*ignore))

    def upload_file(self, source, dest):
        shutil.copyfile(source, dest)
    
    def open(self, name, mode):
        return open(name, mode)
    
    def write_file(self, remote_path, contents):
        subprocess.check_call(["mkdir", "-p", os.path.dirname(remote_path)])
        open(remote_path, "w").write(contents)

    def spawn(self, *args, **kwargs):
        subprocess.Popen(**self._subprocess_args(*args, **kwargs))
        
    def run(self, *args, **kwargs):
        output = subprocess.check_output(**self._subprocess_args(*args, **kwargs))
        return ExecutionResult(output)
        
    def temporary_dir(self):
        return create_temporary_dir()
    
    @property
    def files(self):
        return FileOperations(self)
    
    def _subprocess_args(self, command, cwd=None, update_env=None, new_process_group=False):
        kwargs = {"args": command, "cwd": cwd}
        if update_env is not None:
            new_env = os.environ.copy()
            new_env.update(update_env)
            kwargs["env"] = new_env
        if new_process_group:
            kwargs["preexec_fn"] = os.setpgrp
        return kwargs

class ExecutionResult(object):
    def __init__(self, output):
        self.output = output
