# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import pytest
import time
from selenium.webdriver.common.keys import Keys
from axe_selenium_python import Axe


class TestAxeConfig:

    @pytest.mark.nondestructive
    @pytest.mark.xfail
    def test_mozillians_full(self, selenium):
        """Run axe against mozillians.org and assert no violations found."""

        script_url = 'src/axe.min.js'
        selenium.get('https://mozillians.org')

        axe = Axe(selenium, script_url)
        response = axe.execute(selenium)

        # convert array to dictionary
        violations = dict((k['id'], k) for k in response['violations'])

        # write result to file
        axe.write_results('mozillians_full.json', violations)
        # assert response exists
        assert len(violations) == 0, violations

    @pytest.mark.nondestructive
    @pytest.mark.xfail
    def test_mozillians_context(self, selenium):
        """Run axe against a specific element of mozillians.org."""

        script_url = 'src/axe.min.js'
        selenium.get('https://mozillians.org')
        axe = Axe(selenium, script_url)
        response = axe.execute(selenium, '#language')

        # convert array to dictionary
        violations = dict((k['id'], k) for k in response['violations'])

        # write result to file
        axe.write_results('mozillians_context.json', violations)
        # assert response exists
        assert len(violations) == 0, violations

    @pytest.mark.nondestructive
    @pytest.mark.xfail
    def test_mozillians_search_full(self, selenium):
        """
        Perform search using keystrokes, and run axe on results page.
        """
        script_url = 'src/axe.min.js'
        selenium.get('https://mozillians.org')

        html = selenium.switch_to.active_element
        elem = html['value']
        elem.send_keys(Keys.TAB)
        elem.send_keys('mbrandt')
        elem.send_keys(Keys.ENTER)

        # wait for page load
        time.sleep(2)
        axe = Axe(selenium, script_url)
        response = axe.execute(selenium)

        # convert array to dictionary
        violations = dict((k['id'], k) for k in response['violations'])

        # write result to file
        axe.write_results('mozillians_search_full.json', violations)
        # assert response exists
        assert len(violations) == 0, violations

    @pytest.mark.nondestructive
    @pytest.mark.xfail
    def test_mozillians_search_context(self, selenium):
        """
        Perform search using keystrokes, and run axe on single element of page.
        """
        script_url = 'src/axe.min.js'
        axe = Axe(selenium, script_url)
        selenium.get('https://mozillians.org')

        html = selenium.switch_to.active_element
        elem = html['value']
        elem.send_keys(Keys.TAB)
        elem.send_keys('mbrandt')
        elem.send_keys(Keys.ENTER)

        # wait for page load
        time.sleep(1)

        axe = Axe(selenium, script_url)

        response = axe.execute(selenium, '#main > p.alert > a')

        # convert array to dictionary
        violations = dict((k['id'], k) for k in response['violations'])

        # write result to file
        axe.write_results('mozillians_search_context.json', violations)
        # assert response exists
        assert len(violations) == 0, violations
