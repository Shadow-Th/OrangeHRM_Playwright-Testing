from playwright.sync_api import expect
class DashboardPage:
    def __init__(self, page):
        self.page = page
        self.dashboard_header = page.get_by_role("heading", name="Dashboard")
        self.sidebar_container = page.locator(".oxd-sidepanel")
        self.sidebar_toggle = page.locator(".oxd-main-menu-button")
        self.widgets = page.locator(".orangehrm-quick-launch-card")
        self.menu_items_list = [ "Admin", "PIM", "Leave", "Time", "Recruitment", "My Info", "Performance", "Dashboard", "Directory", "Maintenance", "Claim", "Buzz"]

    def verify_all_item_leftpanel(self):
        for item_name in self.menu_items_list:
            item = self.sidebar_container.get_by_role("link", name=item_name)
            expect(item).to_be_visible(timeout=10000)

    def get_widget_count(self):
        return self.widgets.count()

    def toggle_sidebar(self):
        self.sidebar_toggle.click()