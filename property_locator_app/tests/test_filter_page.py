import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

def test_property_filter_flow(pla_login):
    driver = pla_login
    wait = WebDriverWait(driver, 45)

    filter_btn = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(., 'Filters')]")
    ))
    driver.execute_script("arguments[0].click();", filter_btn)
    print("Filter modal opened")


    saved_filter_trigger = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[contains(., 'Select Saved Filter')]")
    ))
    saved_filter_trigger.click()
    
    property_option = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@role='option' or @role='menuitem']//span[text()='property']")
    ))
    property_option.click()


    bed_select_element = wait.until(EC.presence_of_element_located((By.XPATH, "//select[contains(., '1 Bed')]")))
    bed_select = Select(bed_select_element)
    bed_select.select_by_value("ONE_BED")
    print("Selected 1 Bed")

    bath_select_element = wait.until(EC.presence_of_element_located((By.XPATH, "//select[contains(., '1 Bath')]")))
    bath_select = Select(bath_select_element)
    bath_select.select_by_value("ONE_BATH")
    print("Selected 1 Bath")

    apply_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-cy='filters-modal-submit']")))
    driver.execute_script("arguments[0].click();", apply_btn)
    print("Filters applied")

    try:
        count_element = wait.until(EC.visibility_of_element_located((By.ID, "property-count")))
        print(f"Verification Success: {count_element.text}")
        assert "properties found" in count_element.text
    except Exception as e:
        pytest.fail(f"Filter verification failed. Error: {e}")