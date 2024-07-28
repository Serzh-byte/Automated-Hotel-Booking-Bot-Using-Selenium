import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from booking.booking import Booking
from booking.booking_filtration import BookingFiltration

options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)

try:
    with Booking(teardown=True) as bot: 
        bot.land_first_page()
        bot.place_to_go('Bangkok')
        
        bot.close_button()
        bot.place_to_go_clicked()
        
        bot.calendar(check_in='2023-04-09', check_out='2023-04-22')
        bot.guest_block_click()
        bot.adult_add(2)
        bot.done_click()
        bot.search_button()

        # Initialize filtration
        filtration = BookingFiltration(driver=bot)
        filtration.star_filtration(star_values=[4, 5])
        filtration.apply_price_range(min_price=1000, max_price=30000)
        filtration.apply_meal_option('Breakfast included')

        # Fetch and print prices
        bot.prices()

except Exception as e:
    print(f"An error occurred: {e}")
