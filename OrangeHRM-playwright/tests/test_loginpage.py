from playwright.sync_api import expect
import re, pytest
from pages.loginpage import LoginPage
from conftest import admin_creds

@pytest.mark.skipif(reason = "if called by another it is imported")
def test_successful_login(page, admin_creds):
    login_page = LoginPage(page)
    if "dashboard" not in page.url:
        login_page.navigate()
        login_page.login(admin_creds["admin_user"], admin_creds["admin_password"])
        expect(page).to_have_url(re.compile(r".*dashboard/index"), timeout=30000)





        
