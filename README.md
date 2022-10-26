# Лабораторные работы в рамках лекционного курса "Введение в распределенные технологии 2022/2023"
## Список лабораторных работ

* Лабораторная работа №1 "Установка Docker и Minikube, мой первый манифест."
* Лабораторная работа №2 "Развертывание веб сервиса в Minikube, доступ к веб интерфейсу сервиса. Мониторинг сервиса."
* Лабораторная работа №3 "Сертификаты и "секреты" в Minikube, безопасное хранение данных."
* Лабораторная работа №4 "Сети связи в Minikube, CNI и CoreDNS."

## Подготовительная работа
1. Шпаргалка по [Markdown](https://github.com/sandino/Markdown-Cheatsheet)
2. Работа с Markdown в [VSCode](https://code.visualstudio.com/docs/languages/markdown)
3. Расширение для работы с cистемой контроля версий [Git](https://code.visualstudio.com/docs/sourcecontrol/overview) в VSCode

## Docker
Для знакомство с технологией можно посмотреть [Docker для Начинающих - Полный Курс](https://www.youtube.com/watch?v=n9uCgUzfeRQ) (продолжительность - 2 часа)

### Образы и контейнеры
* Образы (Images) - шаблоны для создания контейнеров, доступны только для чтения (они фиксированы, их невозможно изменить).

  В Docker существует целая цепочка наследования образов, которая позволяет запускать различные приложения в различных ОС.

* Контейнеры запускаются на основе (т.е. после прочтения) образа (например, образа Python или NodeJS). Именно в контейнере происходит работа приложения или сервиса.

Для многих технологий существуют Docker-образы, которые можно скачать с репозиториев на [Docker Hub](https://hub.docker.com/).

Например,
* [официальный Docker-образ Python](https://hub.docker.com/_/python)
* [официальный Docker-образ NodeJS](https://hub.docker.com/_/node)

Это готовые настройки, которые можно использовать для запуска своих контейнеров, где будут работать приложения.

    Если Docker не находит образ локально, он автоматически подтягивает его из сети.

### Основные команды
Выполняются через командную строку - cmd.  
`docker` - вывод документации  
`docker version` - версия Docker  
`docker images` -  
`docker run CONTAINER_ID` -  
`docker ps` -  
`docker ps --help` -   
`docker ps -a` - 
`docker run -it node`-  
`docker rm CONTAINER_ID` -  
`docker COMMAND --help` - параметр `--help` позволяет вывести документацию на команду

## Ошибки (в  хронологическом порядке)
1. Docker не запускался на Windows 10

> Docker daemon fails to start up on Windows or stops for some reason and when you try to run any commands:  
error during connect: Get http://%2F%2F.%2Fpipe%2Fdocker_engine/v1.30/info: open //./pipe/docker_engine: The system cannot find the file specified. In the default daemon configuration on Windows,
the docker client must be run elevated to connect. This error may also indicate that the docker daemon is not running.

* Решение  
Установка [пакета](https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi) обновления ядра Linux в WSL 2 для 64-разрядных компьютеров с [официальной страницы Microsoft](https://learn.microsoft.com/ru-ru/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package)


## Kubernetes 
1. [Основы Kubernetes](https://kubernetes.io/ru/docs/tutorials/kubernetes-basics/) на русском.
2. [Руководство по Minikube](https://kubernetes.io/ru/docs/tutorials/hello-minikube/) на русском.

## Полезные ссылки
1. Установка Docker с [официального сайта](https://www.docker.com/)  
2. Расширение для работы с [Docker](https://code.visualstudio.com/docs/containers/overview) в VSCode