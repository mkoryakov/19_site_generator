# Encyclopedia

Cкрипт, который конвертирует статьи из формата _markdown_ в _html_ и делает из них небольшой статический сайт. Сайт будет помещён в каталог `encyclopedia`. Результат работы скрипта доступен по [адресу](https://mkoryakov.github.io/19_site_generator/encyclopedia/).

# Установка зависимостей скрипта
    $ pip install -r requirements.txt

# Запуск скрипта
Скрипт содержит необязательный параметр config, в котором указывается путь к конфигурационному файлу статического сайта. Если параметр не задан, будет использовано значение по умолчанию - **config.json**.

    $ python md_to_html.py --config config.json

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
