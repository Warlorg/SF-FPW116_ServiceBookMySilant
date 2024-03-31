# SF-FPW116_ServiceBookMySilant
Diploma project "Service e-book" on Django 
# Проект электронной сервисной книжки компании "Силант" - "Мой Силант"

<h4>Сервис предназначен для ведения технического состояния техники, о проведенных ремонтах и техническом обслуживании</h4>

<h2>Функционал сервиса</h2>

<h3>Роли</h3>

| **Роль**        | **Доступ к данным машин**                   | **Доступ к списку машин**                        |
|-----------------|---------------------------------------------|--------------------------------------------------|
| Клиент          | Имеет доступ к данным определённых машин    | У каждой машины есть только один клиент          |
| Сервисная орг.  | Доступ к данным определённых машин          | У каждой машины только одна сервисная организация|
| Менеджер        | Доступ ко всем данным машин                 | Доступ ко всем машинам и редактированию данных   |

<h2>Преднастроенные роли</h2>
<hr>
        Супер-юзер - полный доступ <br>
            логин: Admin <br>
            пароль: admin <br>
<hr>
        Клиент - ограниченный доступ согласно роли <br> 
            логин: user (Пользователь ИП Трудников С.В.) <br>
            пароль: silant123 <br>
<hr>
        Сервисная организация - ограниченный доступ согласно роли <br> 
            логин: service01 (Пользователь ООО ФНС <br>
            пароль: silant123 <br>
<hr>
        Менеджер - ограниченный доступ согласно роли <br> 
            логин: manager <br>
            пароль: silant123 <br>
<hr>

![Не авторизованный пользователь]
<br>
<details>
<summary>Нажмите, что бы посмотреть дополнительную информацию</summary>

*Не зарегистрированные пользователи могут просматривать только список машин с ограниченным выводом информации (доступ только к полям пп.1-10)*
Сортировка данных в полях производиться по умолчанию по дате  

Пользователь без авторизации может получить ограниченную информацию о комплектации машины, введя её заводской номер.Данному типу пользователя доступно поле для ввода заводского номера машины и кнопка поиск. Кнопкой поиск можно отсортировать по заводскому номеру машины

![Не авторизованный пользователь]
</details>

**Самостоятельная регистрация отключена**

*Авторизация проводиться по логину/паролю, которые назначаются администратором системы. Пользователь не может самостоятельно поменять логин и/или пароль.*
Для этого согда `ACCOUNT_ADAPTER` который управляеться `ACCOUNT_ALLOW_SIGNUPS` и взависимости от ``False`` или ``True`` можно запретить или разрешить регистрацию
<br>

<h3>API</h3>

API доступно по по ссылке:<pre><code> `http://127.0.0.0:8000/api/` </code></pre> 

<h2>Запуск проекта</h2>

<div style='background-color:#163E6C'>

**Склонируйте репозиторий командой:** <pre><code> `git clone https://github.com/Warlorg/SF-FPW116_ServiceBookMySilant.git` </code></pre> 

**Создайте виртуальное окружение:** <pre><code>`python -m venv`</code></pre> 

**Установите все зависимости:** <pre><code>`pip install -r .\requirements.txt`</code></pre> 

**Запуск сервера:** <pre><code>`python manage.py runserver`</code></pre> 
</div>
