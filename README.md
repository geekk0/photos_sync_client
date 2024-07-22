# photos_sync_client

![python version](https://img.shields.io/badge/python-3.12-brightgreen)
![languages](https://img.shields.io/github/languages/top/geekk0/photos_sync_client)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/3cc6c94a88dd41be9b84faf38e378752)](https://www.codacy.com/gh/geekk0/BRIO_assistant/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=geekk0/BRIO_assistant&amp;utm_campaign=Badge_Grade)
![last-commit](https://img.shields.io/github/last-commit/geekk0/photos_sync_client)
<br>Программа с графическим интерфейсом для автоматизации переноса файлов.

## Описание

Эта программа разработана для переноса фотографий, сделанных с Capture One, в папку назначения на сервере. Переносит имеющиеся в папке исходников ".jpg" файлы в папку назначения в порядке их создания. Отслеживает появление новых файлов в папке исходников и переносит, с использованием заданной задержки. Для удобства использования имеется вкладка настроек.

## Используемые библиотеки

tkinter
<br>PyQt5, qasync, asyncio, watchdog, loguru.
