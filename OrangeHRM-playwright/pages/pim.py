import re

class PIMPage:
    def __init__(self, page):
        self.page = page
        self.pim_menu = page.get_by_role("link", name="PIM")
        self.add_button = page.get_by_role("button", name="Add")
        self.first_name_input = page.get_by_placeholder("First Name")
        self.middle_name_input = page.get_by_placeholder("Middle Name")
        self.last_name_input = page.get_by_placeholder("Last Name")
        self.employee_id_input = page.locator(".oxd-input-group", has_text="Employee Id").get_by_role("textbox")
        self.save_button = page.get_by_role("button", name="Save")
        self.success_toast = page.locator(".oxd-toast")
        self.search_id_input = page.locator(".oxd-input-group", has_text="Employee Id").get_by_role("textbox")
        self.search_button = page.get_by_role("button", name="Search")
        self.table_row = page.locator(".oxd-table-card")
        self.other_id = page.locator("form").filter(has_text="Other Id").get_by_role("textbox")
        self.drivers_license = page.locator("form").filter(has_text="Driver's License Number").get_by_role("textbox")
        self.nationality_dropdown = page.locator(".oxd-select-wrapper").first
        self.marital_status_dropdown = page.locator(".oxd-select-wrapper").nth(1)
        self.gender_male = page.get_by_label("Male")
        self.gender_female = page.get_by_label("Female")
        self.save_personal_details = page.locator("button:has-text('Save')").first

    def fill_personal_details(self, emp_data):
        self.page.locator(".oxd-input-group", has_text="Other Id").get_by_role("textbox").fill(emp_data.get('other_id', ''))
        self.page.locator(".oxd-input-group", has_text="Driver's License Number").get_by_role("textbox").fill(emp_data.get('drivers_license', ''))
        self.page.locator(".oxd-input-group", has_text="Nationality").locator(".oxd-select-text").click()
        self.page.get_by_role("option", name=emp_data.get('nationality', 'Indian')).click()
        self.page.locator(".oxd-input-group", has_text="Marital Status").locator(".oxd-select-text").click()
        self.page.get_by_role("option", name=emp_data.get('marital_status', 'Single')).click()
        gender = emp_data.get('gender', 'Male')
        self.page.get_by_role("radio", name=gender, exact=True).check(force=True)
        self.page.locator("button:has-text('Save')").first.click()

    def search_employee_by_id(self, emp_id):
        id_input = self.page.get_by_role("textbox").nth(1)
        id_input.clear()
        id_input.fill(emp_id)
        self.page.get_by_role("button", name="Search").click()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(1000) 

    def get_table_row_text(self):
        row = self.page.locator(".oxd-table-card").first
        row.wait_for(state="visible", timeout=5000)
        return row.inner_text()

    def navigate_to_pim(self):
        self.page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewEmployeeList")
        self.search_button.wait_for(state="visible")

    def add_employee(self, emp_data):
        self.first_name_input.fill(emp_data.get('first_name', 'DefaultFirst'))
        self.middle_name_input.fill(emp_data.get('middle_name', ''))
        self.last_name_input.fill(emp_data.get('last_name', 'DefaultLast'))
        if emp_data.get('employee_id'):
            self.employee_id_input.click()
            self.page.keyboard.press("Control+A")
            self.page.keyboard.press("Backspace")
        self.employee_id_input.fill(emp_data['employee_id'])
        self.save_button.scroll_into_view_if_needed()
        self.save_button.click()

    def search_employee_by_id(self, employee_id):
        self.navigate_to_pim()
        self.search_id_input.fill("")
        self.search_id_input.fill(employee_id)
        self.search_button.click()
        self.page.wait_for_load_state("networkidle")

    def get_table_row_text(self):
        return self.table_row.first.text_content()