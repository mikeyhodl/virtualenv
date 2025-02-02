from __future__ import absolute_import, unicode_literals

from virtualenv.activation import BatchActivator
from virtualenv.info import PY2

if PY2:
    from pipes import quote
else:
    from shlex import quote


def test_batch(activation_tester_class, activation_tester, tmp_path, activation_python):
    version_script = tmp_path / "version.bat"
    version_script.write_text("ver")

    class Batch(activation_tester_class):
        def __init__(self, session):
            super(Batch, self).__init__(BatchActivator, session, None, "activate.bat", "bat")
            self._version_cmd = [str(version_script)]
            self._invoke_script = []
            self.deactivate = "call deactivate"
            self.activate_cmd = "call"
            self.pydoc_call = "call {}".format(self.pydoc_call)
            self.unix_line_ending = False

        def _get_test_lines(self, activate_script):
            # for BATCH utf-8 support need change the character code page to 650001
            return ["@echo off", "", "chcp 65001 1>NUL"] + super(Batch, self)._get_test_lines(activate_script)

        def quote(self, s):
            """double quotes needs to be single, and single need to be double"""
            return "".join(("'" if c == '"' else ('"' if c == "'" else c)) for c in quote(s))

        def print_prompt(self):
            return "echo %PROMPT%"

    activation_tester(Batch)
