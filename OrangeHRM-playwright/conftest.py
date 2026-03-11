import pytest, json, os
from pages.loginpage import LoginPage
from pages.admin import AdminPage
from pytest_html import extras

@pytest.fixture()
def login_page(page):
    return LoginPage(page)

@pytest.fixture(scope="session")
def admin_creds():
    with open('data/auth.json', 'r') as f:
        return json.load(f)

# @pytest.fixture(scope="module")
# def shared_admin_session(browser, admin_creds):
#     context = browser.new_context()
#     page = context.new_page()
#     lp = LoginPage(page)
#     ap = AdminPage(page)
#     lp.navigate()
#     lp.login(admin_creds["admin_user"], admin_creds["admin_password"])
#     real_name = ap.get_any_existing_employee_name()
#     yield page, real_name
#     context.close()

# conftest.py
@pytest.fixture(scope="module")
def shared_page(browser):
    context = browser.new_context()
    page = context.new_page()
    from pages.loginpage import LoginPage
    lp = LoginPage(page)
    lp.navigate()
    lp.login(admin_creds["admin_user"], admin_creds["admin_password"]) 
    yield page 
    from pages.logout import Logout
    Logout(page).perform_logout()
    context.close()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        if "shared_admin_session" in item.funcargs:
            page, _ = item.funcargs["shared_admin_session"]
            if not os.path.exists("test-results"):
                os.makedirs("test-results")
            screenshot_path = f"test-results/failure_{item.name}.png"
            page.screenshot(path=screenshot_path)
            if hasattr(report, "extra"):
                report.extra.append(extras.image(os.path.abspath(screenshot_path)))
                
# def pytest_collection_modifyitems(items):
#     desired_order = ["test_loginpage", "test_dashboard_side", "test_admin", "test_logout", "test_pim"]
#     items.sort(key=lambda item: next((i for i, name in enumerate(desired_order) if name in item.nodeid), len(desired_order)))

# conftest.py

def pytest_html_results_table_row(report, cells):
    if hasattr(report, 'nodeid'):
        clean_name = report.nodeid.split("::")[-1]
        try:
            cells[1] = clean_name 
        except Exception:
            if hasattr(cells[1], 'replace_contents'):
                cells[1].replace_contents(clean_name)

def pytest_metadata(metadata):
    for key in ["Python", "Platform", "Packages", "Plugins", "JAVA_HOME"]:
        metadata.pop(key, None)

