from playwright.sync_api import Page
class Logout:
    def __init__ (self, page):
        self.page = page
        self.user_dropdown = page.locator(".oxd-userdropdown-name")
        self.logout_button = page.get_by_role("menuitem", name="Logout")

    def perform_logout(self):
        self.user_dropdown.wait_for(state="visible")
        username = self.user_dropdown.text_content()
        self.user_dropdown.click()
        self.logout_button.wait_for(state="visible", timeout=5000)
        self.logout_button.click(force=True)
        return username.strip() if username else "No usernaem"
