from selenium import webdriver
import booking.constants as const
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Booking(webdriver.Chrome):
    def __init__(self, driver_path=r"C:/SeleniumDrivers", teardown=False, wait_time=15):
        """
        Initializes a new instance of the Booking class.
        
        Args:
        driver_path (str): Path to the Selenium ChromeDriver.
        teardown (bool): Whether to quit the driver on exit.
        wait_time (int): Implicit wait time for Selenium.
        """
        self.driver_path = driver_path
        self.teardown = teardown
        os.environ['PATH'] += self.driver_path
        super(Booking, self).__init__()
        self.implicitly_wait(wait_time)
        self.maximize_window()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Quits the driver if teardown is True.
        """
        if self.teardown:
            self.quit()

    def land_first_page(self):
        """
        Navigates to the booking.com homepage.
        """
        self.get(const.BASE_URL)

    def place_to_go(self, place_to_go):
        """
        Inputs the destination in the search field.
        
        Args:
        place_to_go (str): Destination to search for.
        """
        try:
            search_field = self.find_element(By.ID, ':Ra9:')
            search_field.clear()
            search_field.send_keys(place_to_go)
        except Exception as e:
            print(f"Error entering place to go: {e}")

    def place_to_go_clicked(self):
        """
        Clicks the destination from the autocomplete suggestions.
        """
        try:
            element = self.find_element(By.CLASS_NAME, 'cd1e09fdfe')
            element.click()
        except Exception as e:
            print(f"Error clicking place to go: {e}")

    def close_button(self):
        """
        Closes the sign-in info popup.
        """
        try:
            dismiss_button = self.find_element(By.CSS_SELECTOR, "button[aria-label='Dismiss sign-in info.']")
            dismiss_button.click()
        except Exception as e:
            print(f"Error closing sign-in info: {e}")

    def calendar(self, check_in, check_out):
        """
        Selects check-in and check-out dates.
        
        Args:
        check_in (str): Check-in date in 'yyyy-mm-dd' format.
        check_out (str): Check-out date in 'yyyy-mm-dd' format.
        """
        try:
            check_in_element = self.find_element(By.CSS_SELECTOR, f'[data-date="{check_in}"]')
            check_in_element.click()
            check_out_element = self.find_element(By.CSS_SELECTOR, f'[data-date="{check_out}"]')
            check_out_element.click()
        except Exception as e:
            print(f"Error selecting dates: {e}")

    def guest_block_click(self):
        """
        Clicks the guest block to open the guest options.
        """
        try:
            guest_block_element = self.find_element(By.CLASS_NAME, 'd67edddcf0')
            guest_block_element.click()
        except Exception as e:
            print(f"Error clicking guest block: {e}")

    def adult_add(self, times):
        """
        Increases the number of adults.
        
        Args:
        times (int): Number of times to click the add button.
        """
        try:
            add_element = self.find_element(By.XPATH, "//button[@class='fc63351294 a822bdf511 e3c025e003 fa565176a8 f7db01295e c334e6f658 e1b7cfea84 d64a4ea64d']")
            for _ in range(times):
                add_element.click()
        except Exception as e:
            print(f"Error adding adults: {e}")

    def done_click(self):
        """
        Clicks the done button after selecting guests.
        """
        try:
            done_element = self.find_element(By.XPATH, "//button[@class='fc63351294 a822bdf511 e2b4ffd73d f7db01295e c938084447 a9a04704ee d285d0ebe9']/span[text()='Done']")
            done_element.click()
        except Exception as e:
            print(f"Error clicking done: {e}")

    def search_button(self):
        """
        Clicks the search button.
        """
        try:
            search_element = self.find_element(By.XPATH, "//button[@class='fc63351294 a822bdf511 d4b6b7a9e7 cfb238afa1 c938084447 f4605622ad aa11d0d5cd' and @type='submit']/span[text()='Search']")
            search_element.click()
        except Exception as e:
            print(f"Error clicking search button: {e}")

    def apply_filtrations(self):
        """
        Applies filters to the search results.
        """
        try:
            column = self.find_element(By.ID, 'filter_group_class_:R14q:')
            five_star = column.find_element(By.ID, ':Rlf94q:')
            five_star.click()
        except Exception as e:
            print(f"Error applying filters: {e}")

    def budget(self):
        """
        Applies budget filter to the search results.
        """
        try:
            column1 = self.find_element(By.ID, 'filter_group_pri_:Rcq:')
            budget = column1.find_element(By.ID, ':rfm:')
            budget.click()
        except Exception as e:
            print(f"Error applying budget filter: {e}")

    def next_button_click(self):
        """
        Clicks the next button to load more results and returns the prices.
        
        Returns:
        list: List of prices from the current page.
        """
        try:
            next_button = self.find_element(By.CSS_SELECTOR, "button.fc63351294[type='button']")
            next_button.click()
            values = WebDriverWait(self, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid='price-and-discounted-price']"))
            )
            prices = []
            for price in values:
                price_text = price.text.replace('THB', '').replace(',', '').strip()
                price_value = int(price_text)
                if price_value <= 30000:
                    prices.append(price_value)
            return prices
        except Exception as e:
            print(f"Error clicking next button: {e}")
            return []

    def prices(self):
        """
        Retrieves and prints all prices that meet the criteria.
        """
        all_prices = []
        while True:
            prices = self.next_button_click()
            if not prices:
                break
            all_prices.extend(prices)

        print(all_prices)

        if self.teardown:
            self.quit()

    def perform_search(self, destination, check_in, check_out, adults, apply_filters=True):
        """
        Performs a complete search on Booking.com with the specified parameters.
        
        Args:
        destination (str): Destination to search for.
        check_in (str): Check-in date in 'yyyy-mm-dd' format.
        check_out (str): Check-out date in 'yyyy-mm-dd' format.
        adults (int): Number of adults.
        apply_filters (bool): Whether to apply filters to the search results.
        """
        self.land_first_page()
        self.place_to_go(destination)
        self.place_to_go_clicked()
        self.close_button()
        self.calendar(check_in, check_out)
        self.guest_block_click()
        self.adult_add(adults - 2)  # Assuming 2 adults by default
        self.done_click()
        self.search_button()

        if apply_filters:
            self.apply_filtrations()
            self.budget()

        self.prices()
