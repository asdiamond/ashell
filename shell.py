import os, re, sys


def child(raw_cmd):
    cmd = tok(raw_cmd)
    # simple single command shell
    fname = cmd[0]
    args = cmd[1:]
    print(args)

    for directory in re.split(":", os.environ['PATH']):  # walk the path
        program = f"{directory}/{fname}"
        try:
            os.execve(program, args, os.environ)
        except FileNotFoundError:  # continue walking the path
            pass
        # if you've gotten here every execve has failed
    print(f"command not found {fname}")


def main():
    print("Welcome to ashell.")

    while True:
        raw_cmd = input("user@machine:dir$ ")
        if raw_cmd.strip() is "q":
            print("Goodbye")
            sys.exit(0)

        ret_code = os.fork()
        if ret_code < 0:
            print("fork failed.")
        elif ret_code == 0:
            child(raw_cmd)
        else:  # fork is ok
            child_pid = os.wait()
            print(f"Child terminted with exit code{child_pid}")


def tok(val):
    return re.findall('\w+', val)


if __name__ == '__main__':
    main()
