# Лабораторные работы в рамках лекционного курса "Введение в распределенные технологии 2022/2023"

## Список лабораторных работ
* Лабораторная работа №1 "Установка Docker и Minikube, мой первый манифест."
* Лабораторная работа №2 "Развертывание веб сервиса в Minikube, доступ к веб интерфейсу сервиса. Мониторинг сервиса."
* Лабораторная работа №3 "Сертификаты и "секреты" в Minikube, безопасное хранение данных."
* Лабораторная работа №4 "Сети связи в Minikube, CNI и CoreDNS."

## Путеводитель по репозиторию
В **директории** каждой лабораторной работы есть **отчет (report) в формате .md**.

Отчет содержит:
* краткий ликбез по теме
* ход работы и замечания
* ошибки, с которыми я столкнулся в ходе выполнения работы, и их решение
* полезные ссылки

Заметки по Docker и Kubernetes:
* `lectures.md` -  с лекций
* `docker_k8s_notes.md` - с онлайн-курса

`exam.md` - ответы на все вопросы экзамена  
`init_rep.py` - скрипт для инициализации репозитория

## Подготовительная работа
Перед тем, как приступать к выполнению лабораторных работ, изучите язык разметки **Markdown**, чтобы красиво оформлять отчеты, систему контроля версий **Git**, а также скачайте какую-нибудь среду разработку (**IDE**).

В качестве IDE удобно использовать **Visual Studio Code**, в котором есть расширения для работы с Markdown, Git и Docker.

Полезные ссылки:
1. Шпаргалка по [Markdown](https://github.com/sandino/Markdown-Cheatsheet)
2. Работа с Markdown в [VSCode](https://code.visualstudio.com/docs/languages/markdown)
3. Расширение для работы с cистемой контроля версий [Git](https://code.visualstudio.com/docs/sourcecontrol/overview) в VSCode
4. [Горячие клавиши](https://skillbox.ru/media/base/goryachie_klavishi_v_vscode/) в VSCode

## Техническая статья на Medium
### [Да что такое этот ваш containerd? Как работает контейнеризация? Связь с Docker и Kubernetes](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/containerd_medium_paper/conainerd_medium_paper.md)

![what_is_containerd](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/containerd_medium_paper/images/what_is_containerd.png 'What is containerd?')

Статья расположена в директории `containerd_medium_paper`, а также опубликована на [Medium](https://medium.com/@anatoliibriushinin/what-is-containerd-bf36c39875c5).

