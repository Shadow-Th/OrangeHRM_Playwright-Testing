import re
from playwright.sync_api import expect

class AdminPage:
    def __init__(self, page):
        self.page = page
        self.admin_menu = page.get_by_role("link", name="Admin")
        self.add_button = page.get_by_role("button", name="Add")
        self.user_role_dropdown = page.locator(".oxd-input-group", has_text="User Role").locator(".oxd-select-text")
        self.status_dropdown = page.locator(".oxd-input-group", has_text="Status").locator(".oxd-select-text")
        self.employee_name_input = page.get_by_placeholder("Type for hints...")
        self.username_field = page.locator(".oxd-input-group", has_text="Username").get_by_role("textbox")
        self.password_field = page.locator(".oxd-input-group", has_text=re.compile(r"^Password$")).get_by_role("textbox")
        self.confirm_password_field = page.locator(".oxd-input-group", has_text=re.compile(r"^Confirm Password$")).get_by_role("textbox")
        self.save_button = page.get_by_role("button", name="Save")
        self.success_toast = page.locator(".oxd-toast")

    def navigate_to_admin(self):
        self.admin_menu.click()
        self.page.wait_for_url("**/admin/viewSystemUsers")

    def get_any_existing_employee_name(self):
        self.navigate_to_admin()
        self.page.wait_for_selector(".oxd-table-card")
        name = self.page.locator(".oxd-table-card").first.locator(".oxd-table-cell").nth(3).text_content()
        return name.strip()

    def add_user(self, user_data):
        self.user_role_dropdown.click()
        self.page.get_by_role("option", name=user_data['user_role']).click()
        search_term = user_data['employee_name'][:3]
        self.employee_name_input.click()
        self.employee_name_input.fill("")
        self.employee_name_input.press_sequentially(search_term, delay=300)
        suggestion_box = self.page.locator(".oxd-autocomplete-dropdown")
        try:
            suggestion_box.wait_for(state="visible", timeout=10000)
            suggestion_box.get_by_text(user_data['employee_name']).first.click()
        except:
            self.employee_name_input.press("ArrowDown")
            self.page.wait_for_timeout(1000)
            suggestion_box.locator(".oxd-autocomplete-option").first.click()
        self.status_dropdown.click()
        self.page.get_by_role("option", name=user_data['status']).click()
        self.username_field.fill(user_data['username']) 
        self.password_field.fill(user_data['password'])
        self.confirm_password_field.fill(user_data['confirm_password'])
        self.save_button.click()

    def get_field_errors(self):
        return self.page.locator(".oxd-input-group__message").all_text_contents()