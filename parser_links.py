# -*- coding: UTF-8 -*-
from urllib.parse import urlencode, urlparse
from bs4 import BeautifulSoup
import requests
import csv
import lxml

DOMAIN = 'domain.com'
HOST = 'https://' + DOMAIN
FORBIDDEN_PREFIXES = ['#', 'tel:', 'mailto:']
FORBIDDEN_SUFFIX = ['.jpg', '.png']
FILENAME = "site_links.csv"
links = set()  # множество всех ссылок


def add_all_links_recursive(url, maxdepth=10):
    print(url[len(HOST):])
    # извлекает все ссылки из указанного `url`
    # и рекурсивно обрабатывает их
    # глубина рекурсии не более `maxdepth`

    # список ссылок, от которых в конце мы рекурсивно запустимся
    links_to_handle_recursive = []

    # получаем html код страницы
    request = requests.get(url)
    # парсим его с помощью BeautifulSoup
    soup = BeautifulSoup(request.content, 'lxml')
    # рассматриваем все теги <a>
    for tag_a in soup.find_all('a', href=True):
        # получаем ссылку, соответствующую тегу
        link = tag_a.get('href')
        if link is None:
            continue
        # если ссылка не начинается с одного из запрещённых префиксов
        if all(not link.startswith(prefix) for prefix in FORBIDDEN_PREFIXES):
            # если ссылка не заканчивается с одного из запрещённых суффиксов
            if all(not link.endswith(suffix) for suffix in FORBIDDEN_SUFFIX):
                # проверяем, является ли ссылка относительной
                # например, `/oplata` --- это относительная ссылка
                # `http://101-rosa.ru/oplata` --- это абсолютная ссылка
                if link.startswith('/') and not link.startswith('//'):
                    if link.startswith('//'):
                        continue
                    # преобразуем относительную ссылку в абсолютную
                    link = HOST + link
                    # проверяем, что ссылка ведёт на нужный домен
                    # и что мы ещё не обрабатывали такую ссылку
                    if urlparse(link).netloc == DOMAIN and link not in links:
                        links.add(link)
                        links_to_handle_recursive.append(link)

                    with open(FILENAME, "w+") as file:
                        for l in links:
                            n = l[15:]
                            file.write(n)
                            file.write('\n')

    if maxdepth > 0:
        for link in links_to_handle_recursive:
            add_all_links_recursive(link, maxdepth=maxdepth - 1)


def main():
    add_all_links_recursive(HOST + '/')
    for link in links:
        print(link)


if __name__ == '__main__':
    main()
