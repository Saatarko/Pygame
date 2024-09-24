# Этот проект - игра перестрелка.


# Описание:
Онлайн/локальная игра на 2 человек(перестрелка) сделана на pygame и socket.

# Технологии:

Языки программирования: Python v3.10,
Дополнительная библиотека: Pygame

# Общие действия для установки/теста игры:
1. Загрузить все файлы на ПК.
2. Установить виртуальное окружение с Python v3.10
3. Установить библиотеки. (в проекте использовался poetry)
   Для этого Вам нужно установить poetry - pip install poetry
   Затем для установки всех библиотек  -   poetry install
4. Для запуска раздельно (сервер в одно месте, клиент в другом) нужно разделять
для запуска сервера нужны:
 4.1 server.py
 4.2 models.py
для сборки/запуска клиента:
 4.3 main.py
 4.4.models.py
 4.5 network.py
models.py используется как в серверной части так и в клиентской

# Для локальной игры требуется (для тестирования):
1. В файле server.py надо раскоментировать s.bind(("localhost", 8000)) и
закоментировать строку s.bind(("0.0.0.0", 8000)). Точно также заменить данные в файле Network.py.
2. Затем запустить server.py и 2 main.py (для каждого игрока)

# Для удаленной игры требуется:
1. Если сервеную часть планируется запускать на сервере то нужно в server.py раскоментировать s.bind(("0.0.0.0", 8000)) и
закоментировать строку s.bind(("localhost", 8000)). 
2. Затем на сервере запустить server.py
3. В файле Network.py нужно вписать адрес сервера (на котором запущен server.py)
4. Затем можно или сделать предварительно exe файлы и дать их игрокам (как это сделать см. ниже). Или 
повторить действия из "Общие действия для установки/теста игры" для обоих игроков, и 
затем просто запускать main.py на клиентском ПК (нужный сервер в настроках Network.py нужен именно 
для клиентских версий)

# Для формирования exe файлов клиентской части программы

1. Нужно установить библиотеку pygameinstall
2. СОбрать билд. Для этого:

1. Установите PyInstaller: Убедитесь, что у вас установлен PyInstaller. Вы можете установить его с помощью pip:
pip install pyinstaller
2. Создайте .exe файл: Откройте командную строку (или терминал) и перейдите в директорию,
где находится ваш основной файл Pygame (main.py). Затем выполните следующую команду:

pyinstaller --onefile --windowed main.py --add-data "network.py;." --add-data "model.py;."

--onefile: создаёт один исполняемый файл.
--windowed: убирает консольное окно (если вы не хотите, чтобы оно отображалось).
--add-data "network.py;." и --add-data "model.py;." добавляют файлы в сборку.
Обратите внимание, что в Windows используется ; для разделения пути, а в других ОС — :.
3. Найдите .exe файл: После завершения сборки вы найдёте ваш .exe файл в папке dist внутри вашей рабочей директории.

# This project is a shootout game.

# Description:
Online/local game for 2 people (shootout) made on pygame and socket.

# Technologies:

Programming languages: Python v3.10,
Additional library: Pygame

# General steps for installing/testing the game:
1. Download all files to PC.
2. Install virtual environment with Python v3.10
3. Install libraries. (poetry was used in the project)
To do this, you need to install poetry - pip install poetry
Then to install all the libraries - poetry install
4. To run separately (server in one place, client in another) you need to separate
to run the server you need:
4.1 server.py
4.2 models.py
to build/run the client:
4.3 main.py
4.4.models.py
4.5 network.py
models.py is used both in the server and client parts

# For local play you need (for testing):
1. In the server.py file, you need to uncomment s.bind(("localhost", 8000)) and
comment out the line s.bind(("0.0.0.0", 8000)). Replace the data in the Network.py file in the same way.
2. Then run server.py and 2 main.py (for each player)

# For remote play you need:
1. If you plan to run the server part on the server, then you need to uncomment s.bind(("0.0.0.0", 8000)) in server.py and
comment out the line s.bind(("localhost", 8000)).

2. Then run server.py on the server
3. In the Network.py file you need to enter the server address (on which server.py is running)
4. Then you can either make .exe files in advance and give them to the players (see below for how to do this). Or
repeat the steps from "General steps for installing/testing the game" for both players, and
then simply run main.py on the client PC (the required server in the Network.py settings is needed specifically
for client versions)

# To generate .exe files for the client part of the program

1. You need to install the pygameinstall library
2. Build the build. To do this:

1. Install PyInstaller: Make sure you have PyInstaller installed. You can install it using pip:
pip install pyinstaller
2. Create an .exe file: Open a command prompt (or terminal) and go to the directory
where your main Pygame file (main.py) is located. Then run the following command:

pyinstaller --onefile --windowed main.py --add-data "network.py;." --add-data "model.py;."

--onefile: creates a single executable file.

--windowed: removes the console window (if you don't want it to be displayed).
--add-data "network.py;." and --add-data "model.py;." add files to the build.
Note that Windows uses ; to separate the path, while other OSes use :.
3. Find the .exe file: Once the build is complete, you will find your .exe file in the dist folder inside your working directory.