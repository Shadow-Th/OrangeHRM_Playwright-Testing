from playwright.sync_api import expect
from pages.loginpage import LoginPage
from pages.dashboard import DashboardPage
from conftest import admin_creds
import pytest

@pytest.mark.skip()
def test_dashboard_sidebar_and_widgets(page, admin_creds):
    login = LoginPage(page)
    dashboard = DashboardPage(page)
    login.navigate()
    login.login(admin_creds["admin_user"], admin_creds["admin_password"])
    dashboard.verify_all_item_leftpanel()
    expect(dashboard.widgets).to_have_count(6)
    dashboard.toggle_sidebar()
    admin_label = page.locator(".oxd-main-menu-item--name", has_text="Admin")
    dashboard.toggle_sidebar()
    expect(admin_label).to_be_visible()


