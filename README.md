# StudConnect 📡

**StudConnect** — это современное веб-приложение, предназначенное для эффективной коммуникации между преподавателями, студентами и административным персоналом университета. Платформа обеспечивает удобное взаимодействие, обмен важной информацией и поддерживает образовательный процесс.

---

## 🚀 Основной функционал

- **Регистрация и аутентификация**
  - Пользователи могут создавать аккаунты и входить в систему.
  - Поддержка различных ролей: студенты, преподаватели, администрация.

- **Профили пользователей**
  - Возможность редактировать личные данные и контактную информацию.

- **Общение и обмен сообщениями**
  - Отправка личных сообщений между пользователями.
  - Рассылки для важных объявлений.

- **Административные инструменты**
  - Управление пользователями и ролями.
  - Управление правами доступа.

- **Удобный и адаптивный интерфейс**
  - Работа на любых устройствах: ПК, планшетах, смартфонах.

---

## 📥 Установка и запуск проекта

### 1. Клонирование репозитория

```bash
git clone https://github.com/slippyslime/studconnect.git
cd studconnect
```



### 2. Создание и запуск контейнеров

Убедитесь, что у вас установлены Docker и Docker Compose. Затем выполните:

```bash
docker-compose up --build
```


Это соберет образы и запустит контейнеры для веб-приложения и базы данных.
В среднем билд занимает 5 минут, на слабых устройствах возможно ожидание до 10 минут.

### 3. Применение миграций

В новом терминале выполните миграции базы данных:

```bash
docker-compose exec web python manage.py migrate
```



### 4. Доступ к приложению

После успешного запуска приложение будет доступно по адресу: [http://localhost:8000](http://localhost:8000)
