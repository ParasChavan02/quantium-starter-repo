import threading
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from app import app

# ChromeDriver path
CHROMEDRIVER_PATH = r"C:\Windows\chromedriver-win64\chromedriver.exe"


# Run Dash app
def run_app():
    app.run(debug=False, port=8050)


# Create Chrome driver
def get_driver():

    service = Service(CHROMEDRIVER_PATH)

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")

    driver = webdriver.Chrome(
        service=service,
        options=options
    )

    return driver


# Start app server
server_thread = threading.Thread(target=run_app)
server_thread.daemon = True
server_thread.start()

# Give server time to start
time.sleep(5)


def test_header_present():

    driver = get_driver()

    driver.get("http://127.0.0.1:8050")

    header = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "header"))
    )

    assert header.text == "Soul Foods Sales Visualizer"

    driver.quit()


def test_graph_present():

    driver = get_driver()

    driver.get("http://127.0.0.1:8050")

    graph = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "sales-chart"))
    )

    assert graph is not None

    driver.quit()


def test_region_picker_present():

    driver = get_driver()

    driver.get("http://127.0.0.1:8050")

    radio = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "region-picker"))
    )

    assert radio is not None

    driver.quit()