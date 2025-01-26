#!/bin/bash

# Имя виртуального окружения
VENV_NAME="venv"

# Проверяем, существует ли виртуальное окружение
if [ ! -d "$VENV_NAME" ]; then
    echo "[INFO] Создаём виртуальное окружение: $VENV_NAME"
    python3 -m venv $VENV_NAME
else
    echo "[INFO] Виртуальное окружение $VENV_NAME уже существует"
fi

# Активируем виртуальное окружение
if [ -d "$VENV_NAME/bin" ]; then
    source $VENV_NAME/bin/activate
elif [ -d "$VENV_NAME\\Scripts" ]; then
    source $VENV_NAME\\Scripts\\activate
else
    echo "[ERROR] Не удалось найти скрипт активации виртуального окружения"
    exit 1
fi

# Устанавливаем зависимости из requirements.txt
if [ -f "requirements.txt" ]; then
    echo "[INFO] Устанавливаем зависимости из requirements.txt"
    pip install -r requirements.txt
else
    echo "[WARNING] Файл requirements.txt не найден. Создайте его, чтобы добавить зависимости."
fi

# Сообщение об успешной настройке
echo "[INFO] Настройка завершена. Виртуальное окружение активировано."

