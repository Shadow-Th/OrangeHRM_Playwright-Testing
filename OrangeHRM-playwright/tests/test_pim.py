# import pytest
# import json
# from playwright.sync_api import expect
# from pages.pim import PIMPage
# from pages.loginpage import LoginPage
# from pages.logout import Logout
# import re

# def load_employee_data():
#     with open('data/employees.json', 'r') as f:
#         return json.load(f)

# @pytest.mark.parametrize("emp_data", load_employee_data())
# def test_add_and_verify_employee(shared_admin_session, emp_data):
#     page, _ = shared_admin_session
#     pim_pg = PIMPage(page)
#     page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/pim/addEmployee")
#     pim_pg.add_employee(emp_data)
#     expect(pim_pg.success_toast).to_be_visible()
#     pim_pg.search_employee_by_id(emp_data['employee_id'])
#     row_text = pim_pg.get_table_row_text()
#     assert emp_data['first_name'] in row_text
#     assert emp_data['last_name'] in row_text

# def test_logout(page, record_property, admin_creds):
#     login = LoginPage(page)
#     logout_pg = Logout(page) 
#     login.navigate()
#     login.login(admin_creds["admin_user"], admin_creds["admin_password"])
#     logged_out_user = logout_pg.perform_logout()
#     record_property("logged_out_user", logged_out_user)
#     expect(page).to_have_url(re.compile(r".*auth/login"))

import pytest
import re, json
from playwright.sync_api import expect
from pages.pim import PIMPage
from pages.loginpage import LoginPage
from pages.logout import Logout
from pages.dashboard import DashboardPage

def load_employee_data():
    with open('data/employees.json', 'r') as f:
        return json.load(f)

def test_pim_continuous(page, admin_creds, faker):
    login = LoginPage(page)
    login.navigate()
    login.login(admin_creds["admin_user"], admin_creds["admin_password"])
    pim_pg = PIMPage(page)
    employees = load_employee_data()
    for emp_data in employees:
            page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/pim/addEmployee")
            emp_data['employee_id'] = str(faker.random_int(100000, 999999))
            pim_pg.add_employee(emp_data)
            expect(pim_pg.success_toast).to_be_visible(timeout=10000)
            page.wait_for_url("**/viewPersonalDetails/**", timeout=20000, wait_until="networkidle")
            page.wait_for_timeout(1000) 
            try:
                pim_pg.fill_personal_details(emp_data)
                expect(pim_pg.success_toast).to_be_visible(timeout=10000)
                pim_pg.success_toast.wait_for(state="hidden")
                page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/pim/viewEmployeeList")
                pim_pg.search_employee_by_id(emp_data['employee_id'])
                row_content = pim_pg.get_table_row_text()
                print(f"Search result found: {row_content}")
                assert emp_data['first_name'] in row_content, f"Expected {emp_data['first_name']} but found {row_content}"
                row_text = pim_pg.get_table_row_text()
                assert emp_data['first_name'] in row_text
                assert emp_data['last_name'] in row_text
                print(f"Verified Employee: {emp_data['first_name']} {emp_data['last_name']}")
            except Exception as e:
                page.screenshot(path=f"details_fail_{emp_data['employee_id']}.png")
                print(f"Failed to fill extra details for {emp_data['employee_id']}")
                raise e
    logout_pg = Logout(page)
    logout_pg.perform_logout()
    expect(page).to_have_url(re.compile(r".*auth/login"))

