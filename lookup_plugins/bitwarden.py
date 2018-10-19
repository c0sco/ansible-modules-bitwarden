#!/usr/bin/env python

# (c) 2018, Matt Stofko <matt@mjslabs.com>
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# This plugin can be run directly by specifying the field followed by a list of entries, e.g.
#     bitwarden.py password google.com wufoo.com
#
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    lookup: bitwarden
    author:
      -  Matt Stofko <matt@mjslabs.com>
    requirements:
      - bw (command line utility)
      - BW_SESSION environment var (from `bw login` or `bw unlock`)
    short_description: look up data from a bitwarden vault
    description:
      - use the bw command line utility to grab one or more items stored in a bitwarden vault
    options:
      _terms:
        description: name of item that contains the field to fetch
        required: True
      field:
        description: field to return from bitwarden
        default: 'password'
"""

EXAMPLES = """
- name: get 'username' from Bitwarden entry 'Google'
  debug:
    msg: "{{ lookup('bitwarden', 'Google', field='username') }}"
"""

RETURN = """
  _raw:
    description:
      - Items from Bitwarden vault
"""

from subprocess import Popen, PIPE, check_output
import os, sys

from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()


class Bitwarden(object):

    def __init__(self, path):
        self._cli_path = path
        try:
            check_output(self._cli_path)
        except OSError:
            raise AnsibleError("Command not found: {0}".format(self._cli_path))

    @property
    def cli_path(self):
        return self._cli_path

    @property
    def logged_in(self):
        return 'BW_SESSION' in os.environ

    def _run(self, args):
        p = Popen([self.cli_path] + args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        rc = p.wait()
        if rc != 0:
            display.debug("Received error when running '{0} {1}': {2}".format(self.cli_path, args, out))
            if out.startswith("Vault is locked."):
                raise AnsibleError("Error accessing Bitwarden vault. Run 'bw unlock' to unlock the vault.")
            elif out.startswith("You are not logged in."):
                raise AnsibleError("Error accessing Bitwarden vault. Run 'bw login' to login.")
            elif out.startswith("Failed to decrypt."):
                raise AnsibleError("Error accessing Bitwarden vault. Make sure BW_SESSION is set properly.")
            elif out.startswith("Not found."):
                raise AnsibleError("Error accessing Bitwarden vault. Specified item not found.")
            else:
                raise AnsibleError("Unknown failure in 'bw' command: {0}".format(out))
        return out.strip()

    def get_entry(self, key, field):
        return self._run(["get", field, key])


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        bw = Bitwarden(path=kwargs.get('path', 'bw'))

        if not bw.logged_in:
            raise AnsibleError("Not logged into Bitwarden: please run 'bw login', or 'bw unlock' and set the BW_SESSION environment variable first")

        field = kwargs.get('field', 'password')
        values = []
        for term in terms:
            values.append(bw.get_entry(term, field))
        return values


def main():
    if len(sys.argv) < 3:
        print("Usage: {0} <field> <name> [name name ...]".format(os.path.basename(__file__)))
        return -1

    print(LookupModule().run(sys.argv[2:], None, field=sys.argv[1]))

    return 0


if __name__ == "__main__":
    sys.exit(main())
