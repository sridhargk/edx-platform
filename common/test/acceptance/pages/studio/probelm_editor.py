"""
Studio Problem Editor
"""
from common.test.acceptance.pages.studio.xblock_editor import XBlockEditorView
from common.test.acceptance.pages.common.utils import click_css
from selenium.webdriver.support.ui import Select


class ProblemXBlockEditorView(XBlockEditorView):
    """
    Represents the rendered view of an Problem editor.
    """

    editor_mode_css = '.edit-xblock-modal .editor-modes .editor-button'
    settings_mode = '.settings-button'
    settings_ordered = ["Blank Common Problem", "", "", "", "Never", "Finished", "False", "0"]

    def open_settings(self):
        """
        Clicks on the settings button
        """
        self._click_button(self.settings_mode)

    @property
    def setting_keys(self):
        """
        Returns the list of all the keys
        """
        all_keys = self.q(css='.label.setting-label').text
        # We do not require the key for 'Component Location ID'
        all_keys.pop()
        return all_keys

    def set_field_val(self, field_display_name, field_value):
        """
        If editing, set the value of a field.
        """
        selector = '.xblock-studio_view li.field label:contains("{}") + input'.format(field_display_name)
        script = "$(arguments[0]).val(arguments[1]).change();"
        self.browser.execute_script(script, selector, field_value)

    @property
    def default_dropdown_values(self):
        """
        Gets default values from the dropdowns
        Returns:
            dropdown_values (list): A list of all the default dropdown values
        """
        dropdown_values = []
        elements = self.browser.find_elements_by_css_selector('select[class="input setting-input"][name]')
        for element in elements:
            dropdown_default_selection = Select(element)
            value = dropdown_default_selection.first_selected_option.text
            dropdown_values.append(value)
        return dropdown_values

    @property
    def default_field_values(self):
        """
        Gets default field values
        Returns:
            list: A list of all the default field values
        """
        return self.q(css='.input.setting-input[value]').attrs('value')

    @property
    def ordered_setting_values(self):
        """
        Arrange the setting values in exact order taken from the page
        Returns:
            ordered_values (list): A list of all the setting values in ordered form
        """
        unordered_values = self.default_field_values + self.default_dropdown_values
        ordered_values = sorted(unordered_values, key=lambda x: self.settings_ordered.index(x))
        return ordered_values

    @property
    def settings(self):
        """
        Place all the keys and values in tuples list
        Returns:
            list: A list of all the key and values in tuples
        """
        return zip(self.setting_keys, self.ordered_setting_values)

    def is_latex_comiler_present(self):
        """
        Checks for the presence of latex compiler settings presence
        Returns:
            bool: True if present
        """
        return self.q(css='.launch-latex-compiler').present

    def _click_button(self, button_name):
        """
        Click on a button as specified by `button_name`

        Arguments:
            button_name (str): button name
        """
        self.q(css=button_name).first.click()
        self.wait_for_ajax()

    def save(self):
        """
        Clicks save button.
        """
        click_css(self, '.action-save')
