from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

import re


def init_browser():
    """
    Создаем окно браузера
    """
    browser = webdriver.Chrome()
    browser.wait = WebDriverWait(browser, 5)
    return browser


def search_words(words: str, link: str):
    """
    Парсер заходит на стартовую страницу,
    вбивает в поиск "words"
    """
    browser = init_browser()

    browser.get('http://yandex.ru')
    yandex_search_input = browser.find_element_by_id('text')
    yandex_search_input.send_keys(words)
    yandex_search_input.submit()

    count = [0]

    def parsing_result():
        """
        Поиск ссылок на странице выдачи результатов,
        извлечение urls,
        печать результата
        """
        search_result = browser.find_elements_by_xpath('//*[@id="search-result"]/li/div/div[1]/div[1]/a[1]')

        for result in search_result:
            parse_href_from_result = result.get_attribute("href")
            parse_url = re.findall(r'https://[\da-z\.-]+\.[a-z\.]{2,6}', parse_href_from_result)
            for url in parse_url:
                count[0] += 1
                if url == link:
                    print(words, '-', count[0])
        return count

    def next_page(n):
        """
        Переход на n-ю страницу
        """
        search_button = browser.find_element_by_xpath(f'//a[text()="{n}"]')
        search_button.click()

    def runner():
        """
        Запуск парсинга страницы,
        переход на следующую страницу
        """
        parsing_result()
        next_page(2)
        parsing_result()
        next_page(3)
        parsing_result()

    runner()
