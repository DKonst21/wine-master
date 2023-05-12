import datetime
import pandas
import argparse

from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from collections import defaultdict


def get_correct_year_name(winery_age):
    last_two_digit = winery_age % 100
    last_digit = winery_age % 10
    if last_digit == 1 and last_two_digit != 11:
        return 'год'
    elif last_digit in [2, 3, 4] and last_two_digit not in [12, 13, 14]:
        return 'года'
    else:
        return 'лет'


def get_winery_age(year_of_create):
    now = datetime.datetime.now()
    year_now = now.year
    winery_age = year_now - year_of_create
    return winery_age


def get_wine_catalog(wine_cards_filepath):
    excel_data_df = pandas.read_excel(wine_cards_filepath, sheet_name='Лист1', na_values='nan', keep_default_na=False)
    wines = excel_data_df.to_dict(orient='records')
    grouped_wine_cards = defaultdict(list)
    for wine in wines:
        grouped_wine_cards[wine['Категория']].append(wine)
    return grouped_wine_cards


def get_dir_path():
    parser = argparse.ArgumentParser(description='Запуск Сайта-магазина')
    parser.add_argument('-d', '--dir', help='Укажите путь к файлу с продукцией, по умолчанию wine_catalog.xlsx',
                        default='wine_catalog.xlsx')
    args = parser.parse_args()
    return args.dir


if __name__ == '__main__':

    year_of_opening = 1920
    winery_age = get_winery_age(year_of_opening)
    correct_year_name = get_correct_year_name(winery_age)
    wines_catalog = get_wine_catalog(get_dir_path())
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    rendered_page = template.render(
        wines_catalog=wines_catalog,
        winery_age=winery_age,
        correct_year_name=correct_year_name,
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
