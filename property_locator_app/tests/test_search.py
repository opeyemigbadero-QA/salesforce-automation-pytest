import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_property_search_and_details(pla_login):
    driver = pla_login
    wait = WebDriverWait(driver, 45)
    search_query = "Amber"

   
    wait.until(lambda d: "properties" in d.current_url.lower())

   
    search_trigger = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@role='combobox' and contains(., 'Search...')]")
    ))
    driver.execute_script("arguments[0].click();", search_trigger)


    search_input = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[cmdk-input]")))
    search_input.send_keys(search_query)


    dropdown_option_xpath = "//div[@cmdk-item] //span[contains(text(), 'Amber Grove at Olley Creek')]"
    wait.until(EC.visibility_of_element_located((By.XPATH, dropdown_option_xpath)))
    
   
    search_input.send_keys(Keys.RETURN)
    print("Property selected from dropdown")

 
    modal_locator = (By.CSS_SELECTOR, "div[data-cy='listing-details-modal']#detailsPage")
    wait.until(EC.visibility_of_element_located(modal_locator))
    print("Listing details modal displayed")

   
    try:
       
        modal_title = driver.find_element(By.CSS_SELECTOR, "#detailsPage h5.text-lg")
        assert "Amber Grove at Olley Creek" in modal_title.text
        
       
        bed_count = driver.find_element(By.XPATH, "//img[contains(@src, 'bed-icon')]/following-sibling::div/span")
        assert "1-4" in bed_count.text
        
       
        bath_count = driver.find_element(By.XPATH, "//img[contains(@src, 'bath-icon')]/following-sibling::div/span")
        assert "1-2" in bath_count.text
        
        print(f"Verified {modal_title.text} with {bed_count.text} beds and {bath_count.text} baths.")

    except Exception as e:
        pytest.fail(f"Modal verification failed. Error: {e}")