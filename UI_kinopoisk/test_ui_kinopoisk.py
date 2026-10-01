import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Локаторы для теста 1 и общие
SEARCH_INPUT = (By.CSS_SELECTOR, '[placeholder="Фильмы, сериалы, персоны"]')
POSSIBILITY_HEADER = (By.XPATH, "//h2[contains(text(), 'Возможно, вы искали')]")

# Локаторы для теста 2 (Карточка фильма)
MOVIE_LINK_IN_SEARCH = (By.XPATH, '//span[text()="Дневник памяти"]')
MOVIE_INFO_BLOCK = (
    By.XPATH, "//div[contains(@class, 'basicInfoSection')]")
MOVIE_PAGE_TITLE = (By.CSS_SELECTOR, "h1") # Корневой тег h1 для проверки названия фильма

# Локаторы для теста 3 (Карточка персоны)
NOLAN_LINK_IN_SEARCH = (
    By.CSS_SELECTOR, "a[href='/name/41477/'][data-tid='46191fe3']")
PERSON_INFO_TABLE = (
    By.CSS_SELECTOR, "[data-tid='5ca8e1a8'], .styles_table__KGj5u")
PERSON_PAGE_TITLE = (
    By.CSS_SELECTOR, "h1") # Тег h1 для проверки имени персоны

# Локаторы для теста 4 (Фильтрация и меню)
MENU_MOVIES_TAB = (
    By.XPATH, "//a[contains(@class, 'styles_root') and .//span[text()='Фильмы']]")
GENRE_FILTER_BUTTON = (
    By.XPATH, "//a[@data-test-id='next-link' and normalize-space()='Жанры']")
COMEDY_OPTION = (
    By.XPATH, "//span[contains(@class, 'styles_name') and normalize-space()='Комедии']")
FILM_CARD = (
    By.CSS_SELECTOR, "[data-tid='film-card'], [class*='styles_root__']")
CURRENT_GENRE_TITLE = (
    By.CSS_SELECTOR, "h1") # Тег h1 на странице результатов фильтрации

# Локаторы для теста 5 (Внутренняя навигация карточки фильма)
TRAILERS_TAB_LINK = (By.XPATH, "//a[@data-tid='kp-ui.navigation-tabs-item.item' and text()='Трейлеры']")
TRAILERS_PAGE_HEADER = (By.CSS_SELECTOR, "h1") # Главный заголовок на открывшейся странице с трейлерами


# ФИКСТУРА
@pytest.fixture
def wait_driver():
    options = Options()
    # Оптимизация скорости: отключаем загрузку картинок, чтобы страницы открывались мгновенно
    options.add_experimental_option(
        "prefs", {"profile.managed_default_content_settings.images": 2})

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    # Шаг 1: Открываем главную страницу Кинопоиска
    driver.get("https://www.kinopoisk.ru/")

    # Настройка явного ожидания (максимум 10 секунд)
    wait = WebDriverWait(driver, 10)

    # Передаем объекты драйвера и ожидания в сам тест в виде кортежа
    yield driver, wait

    # Закрываем сессию браузера
    driver.quit()


# Тест 1: Поиск фильма по названию
def test_search_movie_by_title(wait_driver):
    driver, wait = wait_driver

    # Шаг 2: Находим поисковую строку
    search_input = wait.until(EC.element_to_be_clickable(SEARCH_INPUT))

    # Вводим название фильма
    movie_title = "Дневник памяти (2004)"
    search_input.send_keys(movie_title)

    # Шаг 3: Отправляем форму (кликаем по кнопке)
    search_input.submit()

    # Находим заголовок блока истории результатов
    possibility_header = wait.until(
        EC.visibility_of_element_located(POSSIBILITY_HEADER))

    assert possibility_header.text.lower() == "возможно, вы искали"


# Тест 2: Просмотр карточки фильма
def test_view_movie_card(wait_driver):
    driver, wait = wait_driver

    # Предусловие: Поиск фильма «Дневник памяти (2004)»
    search_input = wait.until(EC.element_to_be_clickable(SEARCH_INPUT))
    movie_title = "Дневник памяти (2004)"
    search_input.send_keys(movie_title)
    search_input.submit()

    # Шаг 1: Клик по названию фильма в результатах поиска
    movie_link = wait.until(
        EC.element_to_be_clickable(MOVIE_LINK_IN_SEARCH))
    movie_link.click()

    # Ожидаемый результат: Открывается карточка фильма с информацией
    wait.until(EC.visibility_of_element_located(MOVIE_INFO_BLOCK))
    movie_title_element = wait.until(
        EC.visibility_of_element_located(MOVIE_PAGE_TITLE))

    assert movie_title_element.text == "Дневник памяти (2004)"


# Тест 3: Просмотр карточки персоны через результаты поиска (Без авторизации)
def test_view_person_profile_from_search(wait_driver):
    driver, wait = wait_driver

    # Шаг 1: Вводим поисковый запрос и отправляем его
    search_input = wait.until(EC.element_to_be_clickable(SEARCH_INPUT))
    search_input.send_keys("Кристофер Нолан")
    search_input.submit()

    # Шаг 2: Кликаем по постеру Кристофера Нолана
    nolan_link = wait.until(
        EC.element_to_be_clickable(NOLAN_LINK_IN_SEARCH))
    nolan_link.click()

    # Ожидаемый результат: Открылась карточка персоны.
    # На странице корректно отображается информация о ней
    wait.until(EC.visibility_of_element_located(PERSON_INFO_TABLE))
    person_title_element = wait.until(
        EC.visibility_of_element_located(PERSON_PAGE_TITLE))

    assert person_title_element.text == "Кристофер Нолан"

# Тест 4: Фильтрация фильмов через навигацию по меню сайта (Без авторизации)
def test_filter_movies_by_navigating_menu(wait_driver):
    driver, wait = wait_driver

    # Шаг 1: Находим и кликаем на вкладку «Фильмы» в боковом меню
    movies_menu_item = wait.until(
        EC.presence_of_element_located(MENU_MOVIES_TAB))
    driver.execute_script("arguments[0].click();", movies_menu_item)

    # Шаг 2: Кликаем по вкладке-фильтру «Жанры» на открывшейся странице списков
    genre_button = wait.until(
        EC.element_to_be_clickable(GENRE_FILTER_BUTTON))
    genre_button.click()

    # Шаг 3: Выбираем из списка вариантов «Комедии»
    comedy_select = wait.until(
        EC.element_to_be_clickable(COMEDY_OPTION))
    comedy_select.click()

    # Ожидаемый результат:
    # Ждем, что в адресе страницы появилось слово 'comedy'
    wait.until(EC.url_contains('comedy'))

    assert 'comedy' in driver.current_url


# Тест 5: Переключение на вкладку «Трейлеры» в карточке фильма (Без авторизации)
def test_navigate_to_movie_trailers(wait_driver):
    driver, wait = wait_driver

    # Предусловие: Находим фильм «Дневник памяти (2004)» через поиск
    search_input = wait.until(EC.element_to_be_clickable(SEARCH_INPUT))
    search_input.send_keys("Дневник памяти (2004)")
    search_input.submit()

    # Переходим на саму карточку фильма
    movie_link = wait.until(
        EC.element_to_be_clickable(MOVIE_LINK_IN_SEARCH))
    movie_link.click()

    # Ждем, пока карточка полностью загрузится
    wait.until(EC.visibility_of_element_located(MOVIE_INFO_BLOCK))

    # Шаг 1: Находим и кликаем на вкладку «Трейлеры» в меню фильма
    trailers_tab = wait.until(EC.element_to_be_clickable(TRAILERS_TAB_LINK))
    trailers_tab.click()

    # Ожидаемый результат:
    # Страница обновилась и отображает заголовок подраздела с трейлерами
    trailers_header = wait.until(
        EC.visibility_of_element_located(TRAILERS_PAGE_HEADER))

    assert trailers_header.text == "Трейлеры"
