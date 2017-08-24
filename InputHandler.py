import datetime


class InputHandler:

    def __init__(self, is_debug=True):
        self.exec = {"", "", ""}
        self.is_debug = is_debug
        self.commands = []
        self.history = []

    def parse_command(self, line):
        if line:
            self.exec = [t(s) for t, s in zip((str, str, str), line.rstrip().split())]
            return self.exec

    def add_command(self, line):
        if self.is_debug:
            self.commands.append([datetime.datetime.now(), line])

    def add_log(self, line):
        if self.is_debug:
            self.history.append([datetime.datetime.now(), line])

    def execute_command(self, line, cmd_list):
        cmd = self.parse_command(line)
        output = ""
        if not cmd or cmd[0] not in cmd_list:
            output = ">>> Unrecognized command"
        else:
            self.add_command(line)
            for key, value in cmd_list.items():
                if key == cmd[0]:
                    if len(cmd) == 3:
                        output = value(cmd[1], cmd[2])
                    elif len(cmd) == 2:
                        output = value(cmd[1])
                    else:
                        output = value()
                    break
            if not output:
                output = ">>> Error executing command"
            self.add_log(output)
        if self.is_debug:
            print(output)

    def get_last_cmd(self):
        return self.history[-1]

    def get_cmd(self):
        return self.cmd

    def get_history(self):
        return self.history

    def dump_history(self):
        for cmd in self.history:
            print(">", cmd)