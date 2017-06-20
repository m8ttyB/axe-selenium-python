# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import selenium
import time

class Axe:

    def __init__(self, selenium, script_url):
        self.selenium = selenium
        self.script_url = script_url
        self.inject(selenium, script_url)

    def inject(self, selenium, script_url):
        """
        Recursively inject aXe into all iframes and the top level document.

        :param script_url: location of the axe-core script.
        :type script_url: string
        """
        selenium.execute_script(open(script_url).read())

    def execute(self, selenium):
        command = 'return axe.run().then(function(result){return result;});'
        response = selenium.execute_script(command)
        return response

    def report(self, violations):
        """
        Return readable report of accessibility violations found.

        :param violations: Dictionary of violations.
        :type violations: dict
        :return report: Readable report of violations.
        :rtype: string
        """
        global string
        string = ''
        string += 'Found ' + str(len(violations)) + ' accessibility violations:'
        for i, item in enumerate(violations):
            string += '\n' + str(i + 1) + ') ' + violations[item]['help']
            if violations[item]['helpUrl'] is not None:
                string += ': ' + violations[item]['helpUrl'] + '\n\n'

            nodes = violations[item]['nodes']
            for j, node in enumerate(nodes):
                for target in node['target']:
                    string += target + '\t'

                string += '\n\n' + node['failureSummary'] + '\n\n'
                string += 'Impact: ' + node['impact'] + '\n'

        return string

    def write_results(self, name, output):
        """
        Write JSON to file with the specified name.

        :param name: Name of file to be written to.
        :param output: JSON object.
        """
        file = open(name, 'w+')
        file.write(json.dumps(output, indent=4))
        file.close
