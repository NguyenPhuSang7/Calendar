import pytest

class TestCalendarAndUI:

    @pytest.mark.usefixtures("logged_in_session")
    def test_view_monthly_calendar(self, calendar_page):
        """TC-CAL-01: Verify calendar grid displays correctly and supports month navigation."""
        calendar_page.navigate()
        
        # Assert calendar layout grid is visible
        assert calendar_page.is_calendar_grid_visible(), "Calendar monthly grid failed to display"
        
        # Act: Get current month text, navigate next and check it updates
        initial_month = calendar_page.get_current_month_year()
        calendar_page.go_to_next_month()
        
        next_month = calendar_page.get_current_month_year()
        assert initial_month != next_month, "Calendar month header did not change after navigating to next month"
        
        # Act: Go back to previous month
        calendar_page.go_to_prev_month()
        back_to_initial = calendar_page.get_current_month_year()
        assert initial_month == back_to_initial, "Calendar did not revert to original month after clicking previous"

    @pytest.mark.usefixtures("logged_in_session")
    @pytest.mark.parametrize("viewport_width", [1440, 768, 390])
    def test_responsive_layout_validation(self, calendar_page, viewport_width):
        """TC-UI-01: Verify UI layouts adapt dynamically to desktop, tablet, and mobile dimensions."""
        calendar_page.navigate()
        
        # Act: Resize the browser window
        calendar_page.resize_window(width=viewport_width)
        
        # Assert elements fit and do not break constraints
        if viewport_width == 1440:
            # Desktop (1440px): sidebar should be visible, hamburger hidden
            assert not calendar_page.is_sidebar_hidden(), "Sidebar should be visible on desktop (1440px)"
            assert not calendar_page.is_hamburger_menu_visible(), "Mobile hamburger menu should be hidden on desktop"
            
        elif viewport_width in (768, 390):
            # Tablet/Mobile (viewport width <= 760px): sidebar should collapse, hamburger visible
            assert calendar_page.is_sidebar_hidden(), f"Sidebar should collapse on viewport: {viewport_width}px"
            assert calendar_page.is_hamburger_menu_visible(), f"Mobile hamburger trigger should be visible on viewport: {viewport_width}px"
            # Verify critical navigation elements do not overlap on mobile
            if viewport_width == 390:
                assert calendar_page.check_layout_overlap(), "UI elements overlapped on 390px mobile viewport"
