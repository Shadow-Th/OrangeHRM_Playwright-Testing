from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        page.get_by_role("textbox", name = "Username")
        self.username_field = page.get_by_placeholder("Username")
        self.password_field = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")

    def navigate(self):
        response = self.page.goto("https://opensource-demo.orangehrmlive.com/", wait_until="load")
        if response and response.status >= 500:
            print(f"Server is down (Status {response.status}). Waiting 10s for restart...")
            self.page.wait_for_timeout(10000)
            self.page.reload()

    def login(self, user, passw):
        self.username_field.wait_for(state="visible", timeout=30000)
        self.username_field.fill(user)
        self.password_field.fill(passw)
        with self.page.expect_navigation(wait_until="load"):
            self.login_button.click()
        self.page.wait_for_url("**/dashboard/index", timeout=30000)