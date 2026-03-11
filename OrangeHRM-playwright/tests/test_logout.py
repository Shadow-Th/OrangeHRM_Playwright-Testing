from playwright.sync_api import expect
import re, pytest
from tests.test_loginpage import test_successful_login
from pages.logout import Logout
from conftest import admin_creds

@pytest.mark.skip()
def test_logout_works(page, record_property, admin_creds):
    test_successful_login(page, admin_creds)
    logout_pg = Logout(page) 
    logged_out_user = logout_pg.perform_logout()
    record_property("logged_out_user", logged_out_user)
    expect(page).to_have_url(re.compile(r".*auth/login"))