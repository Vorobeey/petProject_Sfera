""" Программа используется для автоматизации работы редактора-дизайнера
производственной фирмы "СФЕРА" Санкт-Петербург по изготовлению ритуальной
продукции. Она забирает с личного кабинета дизайнера все необходимые
данные и изображдения для последующей обработки. А также в папки загруженных
заказов копирует необходимые .psd файлы и .jpeg фоны."""

import json
import os
from datetime import date
import requests
import re
import shutil


# Забираем с сайта json, в котором хранятся все данные заказов и ссылки на изображения
def parsing_sfera():
    session = requests.Session()
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/'
                      '537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/'
                      '537.36 OPR/86.0.4363.70'
    }
    data = {
        # Логин и пароль были спрятаны при выкладывании на github
        'login': '*****',
        'password': '*****'
    }
    link = 'https://sferazakaz.ru/fl/login'
    # Не удалять неиспользуемую response, иначе не будет работать post
    response = session.post(link, data=data, headers=header).text

    link = 'https://sferazakaz.ru/udata//panel/loadFreelancerOrders/.json'
    response = session.get(link, headers=header).text

    try:
        os.mkdir(f'D:\\test\\{date.today()}')
    except FileExistsError:
        pass

    with open(f'D:\\test\\{date.today()}\\orders.json', 'w', encoding='utf-8') as file:
        file.write(response)


parsing_sfera()


def downloads_orders():
    link = 'https://sferazakaz.ru'
    path = 'D:\\Sfera\\Шаблоны шрифты'

    # Замена английской буквы 'x' на русскую.
    # Необходимо, так как в архиве СФЕРА размеры изделий указаны с разными буквами.
    def rename_x(path):
        try:
            os.rename(f'{path}\\Керамика Фарфор\\овалы портреты\\6x9',
                      f'{path}\\Керамика Фарфор\\овалы портреты\\6х9')
            os.rename(f'{path}\\Керамика Фарфор\\овалы портреты\\7x9',
                      f'{path}\\Керамика Фарфор\\овалы портреты\\7х9')
            os.rename(f'{path}\\Керамика Фарфор\\овалы портреты\\7x10',
                      f'{path}\\Керамика Фарфор\\овалы портреты\\7х10')
            os.rename(f'{path}\\Керамика Фарфор\\овалы портреты\\10x15',
                      f'{path}\\Керамика Фарфор\\овалы портреты\\10х15')
            os.rename(f'{path}\\Керамика Фарфор\\овалы портреты\\11x15',
                      f'{path}\\Керамика Фарфор\\овалы портреты\\11х15')
            os.rename(f'{path}\\Керамика Фарфор\\портреты прям\\10x15',
                      f'{path}\\Керамика Фарфор\\портреты прям\\10х15')
            os.rename(f'{path}\\Металл\\Портреты овалы металл\\9x12',
                      f'{path}\\Металл\\Портреты овалы металл\\9х12')
            os.rename(f'{path}\\Металл\\Портреты овалы металл\\13x18',
                      f'{path}\\Металл\\Портреты овалы металл\\13х18')
        except FileNotFoundError:
            pass

    rename_x(path)

    with open(f'D:\\test\\{date.today()}\\orders.json', 'r', encoding='utf-8') as file:
        src = json.load(file)

    block_orders = src['orders']
    number_order = []
    count_order = 0
    count_photo = 1

    for i in list(zip(block_orders)):
        number_order.append(''.join(i))
        count_order += 1

    print(
        f'Всего на сегодня заказов: {count_order}\n'
        f'Начинается загрузка файлов...'
    )

    for num in number_order:

        # Из json достаем ссылки на оригинальные фотографии и обработанные нейросетью фотографии.
        # В json ссылки хранятся хаотично и неупорядоченно, поэтому проверяются все доступные места.
        try:
            sours_photo = block_orders[num]["images"]["hashes"]["0"]
        except Exception:
            sours_photo = block_orders[num]["re_image_1"]["path"]

        try:
            original_photo = f'{block_orders[num]["images"]["iml_images"][sours_photo]["input_url"]}'
            processed_photo = f'{block_orders[num]["images"]["iml_images"][sours_photo]["output_url"]}'
        except Exception:
            original_photo = f'{link}{sours_photo[1::]}'
            processed_photo = None

        if 'order_images' not in original_photo:
            try:
                original_photo = f'{block_orders[num]["images"]["filePaths"]["0"]}'
                processed_photo = None
            except Exception:
                original_photo = f'{link}{sours_photo}'
                processed_photo = None

        sfera_number = block_orders[num]["sfera_number"]

        try:
            os.mkdir(f'D:\\test\\{date.today()}\\{sfera_number}')
        except FileExistsError:
            pass

        order_name = f'{block_orders[num]["order_name"]}'
        description = f'{block_orders[num]["description"]}'
        last_name_1 = f'{block_orders[num]["last_name_1"]}'
        first_name_1 = f'{block_orders[num]["first_name_1"]}'
        dates_1 = f'{block_orders[num]["dates_1"]}'
        description_layout = f'{block_orders[num]["flmsg"]}'

        with open(f'D:\\test\\{date.today()}\\{sfera_number}\\Детали заказа {sfera_number}.txt', 'w',
                  encoding='utf-8') as file:
            file.write(f'{order_name}\n{description}\n{last_name_1}\n{first_name_1}\n{dates_1}\n{description_layout}')

        text = order_name.replace(',', '').replace(')', '').replace('(', '').replace(':', '')
        color = text.split()[1].capitalize()

        # В архиве СФЕРА с заготовками psd и jpg директории названы не совсем стандартно.
        # Переименовывать их сам не стал, так как сторонним дизайнерам тоже может пригодиться программа,
        # а свои архивы они качали с сайта СФЕРА с точно такими же названиями директорий.
        material = text.split()[2].capitalize()

        material_path = 'Металл'
        if material == 'Керамика':
            material_path = 'Керамика Фарфор'
        if material == 'Керамогранит':
            material = 'Керамика'
            material_path = 'Керамика Фарфор'

        size = ''.join(re.findall(r'\d+\w\d+', text))   # Поиск текста из строки в виде "13х18"
        number_psd = re.findall(r'\d\d', text)[0]   # Поиск текста из строки в виде "25"
        background = 'Без замены фона'
        if 'фон' in text:
            background = re.findall(r'\d\d', text)[-1]

        view = ''
        if 'овал' in text:
            view = 'Овал'
        elif 'прямоугольник' in text:
            view = 'Прямоугольник'

        psd_path = ''
        if material_path == 'Керамика Фарфор' and view == 'Овал':
            psd_path = 'овалы портреты'
        elif material_path == 'Керамика Фарфор' and view == 'Прямоугольник':
            psd_path = 'портреты прям'
        if material_path == 'Металл' and view == 'Овал':
            psd_path = 'Портреты овалы металл'
        elif material_path == 'Металл' and view == 'Прямоугольник':
            psd_path = 'Портреты прямоугольники металл'

        hole = ''
        if 'отверстий' in text:
            hole = 'Без отверстий'
        elif 'отверстия вертикально' in text:
            hole = 'Вертикальные отверстия'
        elif 'отверстия горизонтально' in text:
            hole = 'Горизонтальные отверстия'

        retouching = ''
        if 'ретуши' in text:
            retouching = 'Без ретуши'
        elif 'сложная' in text:
            retouching = 'Сложная ретушь'

        direction = ''
        if 'вертикально' in text:
            direction = 'Вертикально'
        elif 'горизонтально' in text:
            direction = 'Горизонтально'

        with open(f'D:\\test\\{date.today()}\\{sfera_number}\\'
                  f'Детали заказа {sfera_number}.txt', 'w', encoding='utf-8') as file:
            file.write(
                f'Материал: {material}\n'
                f'Вид: {view}\n'
                f'Размер: {size}\n'
                f'Направление: {direction}\n'
                f'Окантовка: {number_psd}\n'
                f'Примечание: >>>>> {description} <<<<<\n'
                f'Примечание макета: >>>>> {description_layout} <<<<<\n'
                f'Фон: {background}\n'
                f'Цвет: {color}\n'
                f'Ретушь: {retouching}\n'
                f'Отверстия: {hole}\n'
                f'Фамилия: >>>>> {last_name_1} <<<<<\n'
                f'Имя Отчество: >>>>> {first_name_1} <<<<<\n'
                f'Даты: >>>>> {dates_1} <<<<<'
            )

            path_psd = f'{path}\\{material_path}\\{psd_path}\\{size}'
            scan = os.scandir(path_psd)
            list_psd = []
            for item in scan:
                list_psd.append(item)
            str_list_psd = str(list_psd).split("'")
            for psd in str_list_psd:
                if number_psd in psd:
                    name_psd = psd

            shutil.copy(
                f"{path_psd}\\{name_psd}",
                f"D:\\test\\{date.today()}\\{sfera_number}\\{sfera_number}.psd"
            )

        try:
            shutil.copy(
                f"{path}\\Фоны\\{background}.jpg",
                f"D:\\test\\{date.today()}\\{sfera_number}\\{background}.jpg"
            )
        except FileNotFoundError:
            pass

        original_photo_bytes = requests.get(original_photo).content

        with open(f'D:\\test\\{date.today()}\\{sfera_number}\\{sfera_number}.jpg', 'wb') as file:
            file.write(original_photo_bytes)

        if processed_photo is not None:
            processed_photo_bytes = requests.get(processed_photo).content
            with open(f'D:\\test\\{date.today()}\\{sfera_number}\\{sfera_number}+.jpg', 'wb') as file:
                file.write(processed_photo_bytes)

        print(f'Заказов загружено: {count_photo}. Осталось загрузить: {count_order - 1}')
        count_photo += 1
        count_order -= 1
        if count_order == 0:
            print('Все заказы загружены. Хорошей работы!')


downloads_orders()

print(input('Нажмите Enter для завершения работы программы'))