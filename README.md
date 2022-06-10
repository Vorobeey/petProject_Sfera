# petProject_Sfera

>>> Аннотация

  Программа используется для автоматизации работы редактора-дизайнера
производственной фирмы "СФЕРА" Санкт-Петербург по изготовлению ритуальной
продукции. Она забирает с личного кабинета дизайнера все необходимые
данные и изображения для последующей обработки. А также в папки загруженных
заказов копирует необходимые .psd файлы и .jpeg фоны.

>>> Подробно

  Каждое утро рабочего дня дизайнеру необходимо самостоятельно логиниться в личный
кабинет на сайте, раскрывать каждый заказ по очереди, смотреть его детали, вручную
скачивать фотографии с сайта на рабочий компьютер и переименовывать их на номер заказа.

  После необходимо было найти нужный .psd файл заготовки с номером указанным в личном кабинете
заказа, а также .jpeg файл фона.

Скрипт упрощает работу дизайнера:
1. Создает в рабочей директории директорию с сегодняшней датой
2. Внутри создает директории с номером заказа
3. Внутри директории с номером заказа скачивает фотографии из заказа на сайте
4. Создает текстовый документ, в котором удобно записаны все необходимые данные для работы с заказом
5. Копирует из рабочего архива нужный .psd файл, отправляет в папку с заказом и переименовывает на номер заказа
6. Копирует из рабочего архива нужный .jpeg файл фона, отправляет в папку с заказом 

>>> Версии

  10.06.2022 - Первая рабочая версия проекта. Предназначена для использования одному дизайнеру. 
Внутри лежат его Логин и Пароль, а также личный путь рабочей директории и рабочего архива.
Для использования другим дизайнером необходимо внутри прописать его личные пути.
