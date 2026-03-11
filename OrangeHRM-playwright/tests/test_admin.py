# import pytest
# import json, re
# from playwright.sync_api import expect
# from pages.admin import AdminPage
# from pages.loginpage import LoginPage
# from pages.logout import Logout
# from pages.dashboard import DashboardPage
# from conftest import admin_creds

# def test_dashboard_sidebar_and_widgets(page, admin_creds):
#     login = LoginPage(page)
#     dashboard = DashboardPage(page)
#     login.navigate()
#     login.login(admin_creds["admin_user"], admin_creds["admin_password"])
#     dashboard.verify_all_item_leftpanel()
#     expect(dashboard.widgets).to_have_count(6)
#     dashboard.toggle_sidebar()
#     admin_label = page.locator(".oxd-main-menu-item--name", has_text="Admin")
#     dashboard.toggle_sidebar()
#     expect(admin_label).to_be_visible()

# def load_user_data():
#     with open('data/users.json', 'r') as f:
#         return json.load(f)

# @pytest.mark.parametrize("user_data", load_user_data())
# def test_add_users_parameterized(shared_admin_session, user_data, faker):
#     page, real_emp_name = shared_admin_session
#     admin_pg = AdminPage(page)
#     user_data['employee_name'] = real_emp_name
#     page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/admin/saveSystemUser")
#     admin_pg.add_user(user_data)
#     expect(admin_pg.success_toast).to_be_visible(timeout=10000)
#     admin_pg.success_toast.wait_for(state="hidden", timeout=10000)

# def test_add_user_field_validation(shared_admin_session):
#     page, _ = shared_admin_session
#     admin_pg = AdminPage(page)
#     page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/admin/saveSystemUser")
#     admin_pg.save_button.click()
#     errors = admin_pg.get_field_errors()
#     assert "Required" in errors
#     print("Validation Check Passed: Required field messages are visible.")

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
from pages.admin import AdminPage
from tests.test_loginpage import test_successful_login 
from tests.test_dashboard_side import test_dashboard_sidebar_and_widgets
from pages.logout import Logout
from conftest import admin_creds

def load_user_data():
    with open('data/users.json', 'r') as f:
        return json.load(f)

def test_admin_full_flow(page, admin_creds,faker):
    test_successful_login(page, admin_creds)
    test_dashboard_sidebar_and_widgets(page)
    admin_pg = AdminPage(page)
    users = load_user_data()
    for user_data in users:
        page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/admin/viewSystemUsers")
        real_emp_name = admin_pg.get_any_existing_employee_name() 
        page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/admin/saveSystemUser")
        user_data['employee_name'] = real_emp_name 
        user_data['username'] = f"{user_data['username']}_{faker.random_int(100, 999)}"
        admin_pg.add_user(user_data)
        expect(admin_pg.success_toast).to_be_visible(timeout=10000)
        admin_pg.success_toast.wait_for(state="hidden", timeout=10000)
        page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/admin/viewSystemUsers")
        admin_pg.search_user(user_data['username']) 
        row_text = admin_pg.get_table_row_text()
        assert user_data['username'] in row_text
        print(f"Verified: User {user_data['username']} is in the table.")
        page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/admin/saveSystemUser")
        admin_pg.save_button.click()
        errors = admin_pg.get_field_errors()
        assert "Required" in errors
        print("Validation Check Passed: Required field messages are visible.")
    logout_pg = Logout(page)
    logout_pg.perform_logout()
    expect(page).to_have_url(re.compile(r".*auth/login"))





