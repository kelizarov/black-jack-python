class InputHandler:

    def __init__(self):
        self.cmd = {"", "", ""}
        self.history = []

    def parse_command(self, line):
        if line:
            self.cmd = [t(s) for t, s in zip((str, str, str), line.rstrip().split())]
            return self.cmd

    def add_command(self, line):
        self.history.append(line)

    def execute_command(self, line, cmd_list):
        cmd = self.parse_command(line)
        if not cmd or cmd[0] not in cmd_list:
            print(">>> Unrecognized command")
            return
        self.add_command(line)
        for key, value in cmd_list.items():
            if key == cmd[0]:
                if len(cmd) == 3:
                    value(cmd[1], cmd[2])
                elif len(cmd) == 2:
                    value(cmd[1])
                else:
                    value()
                return

    def get_last_cmd(self):
        return self.history[-1]

    def get_cmd(self):
        return self.cmd

    def get_history(self):
        return self.history

    def dump_history(self):
        for cmd in self.history:
            print(">", cmd)