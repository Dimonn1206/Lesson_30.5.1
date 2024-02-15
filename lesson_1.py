import pytest
from selenium import webdriver      #подключение библиотеки
from  webdriver_manager.chrome import ChromeDriverManager       #импорт вебдрайвера Chrome
from  selenium.webdriver.chrome.service import Service      #нужен для открытия браузера и выполнения тестов
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait         #нужен для использования явных ожиданий
from selenium.webdriver.support import expected_conditions as EC        #сокращает название элемнета 'expected_conditions'

service = Service(executable_path=ChromeDriverManager().install())
chrome_options = webdriver.ChromeOptions
# chrome_options.add_argument("--window-size=1920, 1080")

@pytest.fixture(autouse=True)
def driver():
    driver = webdriver.Chrome(service=service)

    #Добавляем неявное ожидание для загруки карточек питомцев
    driver.implicitly_wait(5)
    driver.get('https://petfriends.skillfactory.ru/login')

    #Важно установить большое разрешение экрана, иначе путь в dom дереме может измениться
    driver.set_window_size(1920, 1080)
    yield driver

    driver.quit()

def test_show_all_pets(driver):
    driver.find_element('id', 'email').send_keys('dimon.viktorov70@gmail.com') #Вводим email
    driver.find_element('id', 'pass').send_keys('52944012') #Вводим пароль
    #Нажимаем на кнопку входа

    element = (By.CSS_SELECTOR, 'button[type="submit"]')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(element)).click()
    # driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    #Провеверяем, что мы оказались на главной странице

    assert driver.find_element(By.TAG_NAME, 'h1').text == "PetFriends"

    images = driver.find_elements(By.XPATH, '//img[@class="card-img-top"]')
    names = driver.find_elements(By.XPATH,'//h5[@class="card-   title"]')
    descriptions = driver.find_elements(By.XPATH,'//p[@class="card-text"]')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ""
        assert names[i].text != ""
        assert descriptions[i].text != ""
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(", ")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0


    """Выполнение задания 30.3.1"""

    #Проверяем, что пристутствуют все питомцы
    xpath_for_element = ('xpath', '//a[@href="/my_pets"]')      #Сохраняем xpath в переменную

    # Добавляем ожидание для загрузки страницы и кликаем на кнопку 'Мои питомцы'
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located(xpath_for_element)).click()
    # driver.get("https://petfriends.skillfactory.ru/my_pets")

    amount = driver.find_elements(By.XPATH, "//table//tbody/tr")
    assert len(amount) == 2     #Количетсво моих питомцев: 2

    #Проверяем, что у половины моих питомцев есть фото

    images_my_pets = driver.find_elements(By.XPATH, '//table//tbody/tr//img[@src]')
    assert ((len(images_my_pets))/2) != ""

    #Проверяем, что у всех питомцев есть имя, возраст и порода
    names_my_pets = driver.find_elements(By.XPATH, '//table//tbody//td[1]')     #Выводим имена
    animal_type = driver.find_elements(By.XPATH,'//table//tbody//td[2]')        #Выводим породу
    age = driver.find_elements(By.XPATH,'//table//tbody//td[3]')        #Выводим возраст

    #Выполнянем проверку наличия данных питомцев
    for i in range(len(names_my_pets)):
        assert names_my_pets[i].text != ""
        # print('Имя:', names_my_pets[i].text)

        assert animal_type[i].text != ""
        # print('Порода:', animal_type[i].text)

        assert age[i].text != ""
        # print('Возраст:', age[i].text)

    #Проверяем, что у питомцев разные имена
    names_my_pets = driver.find_elements(By.XPATH, '//table//tbody//td[1]')
    # создать пустой список
    names_list = []

    # выполнить цикл for по элементам
    for name in names_my_pets:
        # добавить элемент в список
        names_list += [name.text]

    set_names = set(names_list)
    if len(names_list) == len(set_names):
        print('Все питомцы уникалльные')
    else:
        print('Есть одинаковые')