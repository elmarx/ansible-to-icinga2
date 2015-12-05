import unittest
from textwrap import dedent

from filter_plugins import to_icinga2


class ToIcinga2ExpressionTest(unittest.TestCase):
    def _p(self, t):
        return dedent(t).strip()

    def test_string_value(self):
        self.assertEqual("vars.os = \"Linux\"", to_icinga2.to_icinga2_expression(dict(os="Linux")))

    def test_multiple_string_values(self):
        expected = """
        vars.os_family = "RedHat"
        vars.os = "Linux"
        """
        self.assertEqual(self._p(expected), to_icinga2.to_icinga2_expression(dict(os="Linux", os_family="RedHat")))

    def test_with_list(self):
        expected = """
        vars.notification["mail"] = {
            groups = [ "icingaadmins" ]
        }
        """

        self.assertEqual(self._p(expected), to_icinga2.to_icinga2_expression({
            "notification": {
                "mail": {
                    "groups": ["icingaadmins"]
                }
            }
        }))

    def test_empty_dict(self):
        expected = """
        vars.disks["disk"] = {

        }
        """
        self.assertEqual(self._p(expected), to_icinga2.to_icinga2_expression({
            "disks": {"disk": {}}
        }))

    def test_nested_dict(self):
        expected = dedent("""\
        vars.http_vhosts["Default page"] = {
            http_string = "the string"
            http_uri = "/"
        }""")

        configuration = {
            "http_vhosts": {
                "Default page": {
                    "http_string": "the string",
                    "http_uri": "/"
                }
            }
        }

        self.assertEqual(expected, to_icinga2.to_icinga2_expression(configuration))


if __name__ == '__main__':
    unittest.main()
