import pytest
import user_data
from selenium import webdriver


@pytest.fixture(scope='function', params=['chrome', 'firefox'])
def driver(request):
    if request.param == 'chrome':
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=chrome_options)
    elif request.param == 'firefox':
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument("--width=1920")
        firefox_options.add_argument("--height=1080")
        driver = webdriver.Firefox(options=firefox_options)
    else:
        raise ValueError("Unsupported browser")
    yield driver
    driver.quit()


@pytest.fixture(scope='function')
def user():
    user = user_data.register_new_user_and_return_user_data()
    yield user
    user_data.delete_user(user['json']['accessToken'])
