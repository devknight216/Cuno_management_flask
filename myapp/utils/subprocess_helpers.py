import subprocess, os

# arg `command` as a list of form ["executable", "arg1", "arg2", ...]
# arg `env` as a dictionary
def run_extra_env(exec, env):
    modified_env = os.environ.copy()
    for var in env:
        modified_env[var] = env[var]
    # return value has properties returncode (int), stdout (string), stderr (string)
    return subprocess.run(exec, env=modified_env, capture_output=True, check=False, text=True) 

def run_cunomgr(command, env):
    pass