from selenium.webdriver.common.by import By
import pytest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


login_url = 'http://petfriends.skillfactory.ru/login'
my_pets_url = 'https://petfriends.skillfactory.ru/my_pets'
driver = webdriver.Chrome(r'/home/panda/Documents/inga/selenium/chromedriver/chromedriver')

@pytest.fixture(scope='session', autouse=True)
def authorization():
    driver.get(login_url)
    # Вводим email
    driver.find_element(By.ID, 'email').send_keys('ingarudkevich@gmail.com')
    # Вводим пароль
    driver.find_element(By.ID, 'pass').send_keys('12345')
    # Нажимаем на кнопку входа в аккаунт
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    yield
    driver.quit()

def test_all_pets():

    images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    driver.implicitly_wait(5)
    names = driver.find_elements(By.CSS_SELECTOR,'.card-deck .card-title')
    driver.implicitly_wait(5)
    descriptions = driver.find_elements(By.CSS_SELECTOR,'.card-deck .card-text')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0

# Считаем количество питомцев
def my_pets():
    driver.get(my_pets_url)
    amount_pets = len(driver.find_elements(By.XPATH, '//tbody/tr'))
    return amount_pets


# Проверяем, что присутствуют все питомцы
def test_my_pets_amount():
    amount_pets = my_pets()
    user_statistics = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'div.\.col-sm-4.left'))).text
    split_summary = user_statistics.split()
    summary_amount = [int(split_summary[i + 1]) for i in range(len(split_summary)) if  split_summary[i]== "Питомцев:"]

    assert summary_amount[0] == amount_pets

# Проверяем, что половина питомцев с фото
def test_my_pets_photo():
    amount_pets = my_pets()
    images = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'th > img')))
    # images = driver.find_elements(By.CSS_SELECTOR, 'th > img')
    names = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'td:nth-child(2)')))
    # names = driver.find_elements(By.CSS_SELECTOR, 'td:nth-child(2)')
    pets_with_images = [names[i] for i in range(len(names)) if images[i].get_attribute('src') != '']
    assert len(pets_with_images) >= amount_pets // 2

# Проверяем, что у всех питомцев есть имя, возраст, порода
def test_my_pets_params():

    names = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'td:nth-child(2)')))
    greed = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR,'td:nth-child(3)')))
    age = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'td:nth-child(4)')))

    for i in range(len(names)):
        assert names[i].text != ''
        assert greed[i].text != ''
        assert age[i].text != ''

    # Проверяем, что у всех питомцев разные имена
def test_different_names():
    names = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'td:nth-child(2)')))
    amount_pets = my_pets()
    all_names = []
    for i in range(len(names)):
        all_names.append(names[i])
    assert len(set(all_names)) == amount_pets

# Проверяем, что в списке нет повторяющихся питомцев
def test_different_pets():
    names = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'td:nth-child(2)')))
    greed = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'td:nth-child(3)')))
    age = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'td:nth-child(4)')))

    pets_data = []
    for i in range(len(names)):
        pet = (names[i],age [i], greed[i])
        pets_data.append(pet)
    assert len(pets_data) == len(set(pets_data))









