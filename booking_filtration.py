from selenium import webdriver
import booking.constants as const
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class BookingFiltration:
    def __init__(self, driver: WebDriver):
        """
        Initializes a new instance of the BookingFiltration class.

        Args:
        driver (WebDriver): The Selenium WebDriver instance.
        """
        self.driver = driver

    def star_filtration(self, star_values: list):
        """
        Applies star rating filtration to the search results.

        Args:
        star_values (list): List of star values to filter by (e.g., [3, 4, 5]).
        """
        try:
            column = self.driver.find_element(By.ID, 'filter_group_class_:R14q:')
            star_map = {
                1: ':R1f94q:', 2: ':R2f94q:', 3: ':R3f94q:',
                4: ':R4f94q:', 5: ':R5f94q:'
            }

            for star_value in star_values:
                if star_value in star_map:
                    star_element = column.find_element(By.ID, star_map[star_value])
                    star_element.click()
                else:
                    print(f"Star value {star_value} is not valid.")
        except Exception as e:
            print(f"Error applying star filtration: {e}")

    def apply_price_range(self, min_price: int, max_price: int):
        """
        Applies price range filtration to the search results.

        Args:
        min_price (int): Minimum price value for filtration.
        max_price (int): Maximum price value for filtration.
        """
        try:
            price_filter_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-filters-group='pri']")
            price_filter_button.click()
            min_price_input = self.driver.find_element(By.NAME, "pri=1")
            max_price_input = self.driver.find_element(By.NAME, "pri=2")
            min_price_input.clear()
            max_price_input.clear()
            min_price_input.send_keys(str(min_price))
            max_price_input.send_keys(str(max_price))
            apply_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-testid='filters-form-submit']")
            apply_button.click()
        except Exception as e:
            print(f"Error applying price range: {e}")

    def apply_meal_option(self, meal_option: str):
        """
        Applies meal option filtration to the search results.

        Args:
        meal_option (str): The meal option to filter by (e.g., "Breakfast included").
        """
        try:
            meal_filter_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-filters-group='mealplan']")
            meal_filter_button.click()
            meal_options = self.driver.find_elements(By.CSS_SELECTOR, "label[data-testid='mealplan-label']")
            for option in meal_options:
                if meal_option in option.text:
                    option.click()
                    break
            apply_button = self.driver.find_element(By.CSS_SELECTOR, "button[data-testid='filters-form-submit']")
            apply_button.click()
        except Exception as e:
            print(f"Error applying meal option: {e}")
