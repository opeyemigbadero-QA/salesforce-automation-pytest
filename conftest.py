import pytest
import pytest_html  # <--- THIS WAS MISSING
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

@pytest.fixture(scope="function")
def driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Extends the Pytest-HTML report to include screenshots on failure.
    """
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call" or report.when == "setup":
        xfail = hasattr(report, "wasxfail")
        if (report.failed and not xfail) or (report.skipped and xfail):
            # Check if 'driver' fixture was used in the test
            driver_fixture = item.funcargs.get("driver")
            if driver_fixture:
                screenshot = driver_fixture.get_screenshot_as_base64()
                # Use the pytest_html module to embed the image
                html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % screenshot
                extra.append(pytest_html.extras.html(html))
        report.extra = extra