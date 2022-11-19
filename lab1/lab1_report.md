
University: [ITMO University](https://itmo.ru/ru/)  
Faculty: [FICT](https://fict.itmo.ru)  
Course: [Introduction to distributed technologies](https://github.com/itmo-ict-faculty/introduction-to-distributed-technologies)  
Year: 2022/2023  
Group: K4111c  
Author: Briushinin Anatolii Alekseevich  
Lab: Lab1  
Date of create: 21.10.2022  
Date of finished: 10.11.2022

# Лабораторная работа №1 "Установка Docker и Minikube, мой первый манифест."

## Описание
Это первая лабораторная работа в которой вы сможете протестировать Docker, установить Minikube и развернуть свой первый "под".

## Цель работы
Ознакомиться с инструментами Minikube и Docker, развернуть свой первый "под".

---
## Ликбез

## Docker
### Суть технологии
**Docker** - технология для создания и управления **контейнерами**.

Мы оборачиваем какой-то код или приложение в контейнеры для того, чтобы он нам гарантировал одинаковое поведение в разных окружениях. Мы можем просто брать докер контейнеры и запускать их где угодно, где есть докер. Нам не важно, что это будет за ОС, его версия. Все поведение будет зафиксировано в контейнере.

### Образы и контейнеры
* **Образы (Images)** - шаблоны для создания контейнеров, доступны только для чтения (они фиксированы, их невозможно изменить).

  В Docker существует целая цепочка наследования образов, которая позволяет запускать различные приложения в различных ОС.

> Образы контейнеров Docker можно сравнить с пресс-формами для изготовления пластиковых изделий.

* **Контейнеры (Containers)** запускаются на основе (т.е. после прочтения) образа (например, образа Python или NodeJS). Именно в контейнере происходит работа приложения или сервиса.

> Контейнеры Docker - это вызванные к жизни образы Docker.

### Docker Hub
  Для многих технологий **существуют Docker-образы**, которые можно скачать с **реестра** образов, например [Docker Hub](https://hub.docker.com/).

  Например,
* [официальный Docker-образ Python](https://hub.docker.com/_/python)
* [официальный Docker-образ NodeJS](https://hub.docker.com/_/node)

  Это **готовые настройки**, которые можно использовать для запуска своих контейнеров, где будут работать приложения.

  Если Docker не находит образ локально, он **автоматически** подтягивает его из сети.

### Алгоритм создания контейнера
1. Пишем Dockerfile
2. Создаем образ из Dockerfile
3. Создаем контейнер из образа

> Dockerfile -> Image -> Container

### Dockerfile
Файл [Dockerfile](https://docs.docker.com/engine/reference/builder/) содержит набор **инструкций**, следуя которым Docker автоматически будет собирать образ контейнера. 

Этот файл содержит описание базового образа. В образ контейнера, поверх базового образа, можно добавлять дополнительные **слои**. 

```python
# Comment
INSTRUCTION arguments
```

Свой образ делается на основе базового, например для приложения, написанного на python, базовым будет образ python.

Итак, Dockerfile начинается с инструкции `FROM`, указывающей на **базовый слой**.

* `FROM python`

Так как образ read-only, нужно указать какие конкретно файлы будут использоваться, это делается инструкцией `COPY`.

* `COPY . .`

**Первая** `.` означает, смотрим все сущности, которые есть в корне проекта (там где лежит Dockerfile).
**Вторая** `.` означает, что положим файлы в корень контейнера.

Лучше копировать файлы в специальную директорию, тогда инструкция будет выглядеть:

* `COPY . /app`

Хорошей практикой будет сделать контекст, где все будет храниться, это делается с помощью инструкции `WORKDIR`. В этом случае в инструкции `COPY` вместо `/app` можно ставить `.`:

```
FROM python  
WORKDIR /app
COPY . .
```

Если для запуска наше приложение, требуется запустить, например, модуль pandas (мы используем дополнительные библиотеки), то используем инструкцию `RUN`. 

* `RUN pandas install`

Чтобы запустить наше приложение, надо прописать консольную команду с помощью инструкции `CMD`.

* `CMD ["python", "app.py"]`

Отличие интсрукции `RUN` от `CMD` в том, что `RUN` запускается один раз, когда мы собираем и строим сам образ, а `CMD` запускается каждый раз, когда мы запускаем образ (то есть при создании контейнера из образа).

Это экономит память.

На данный момент Dockerfile выглядит так:

```
FROM python  
WORKDIR /app
COPY . .
RUN pandas install
CMD ["python", "app.py"]
```

Хорошей практикой будет указать, какой порт запускает наше приложение с помощью инструкции `EXPOSE`.  

```
FROM python  
WORKDIR /app
COPY . .
RUN pandas install
EXPOSE 3000
CMD ["python", "app.py"]
```

Инструкция `ENV` позволяет объявлять переменные окружения внутри контейнеров Docker.

> Каждая инструкция в Dockerfile - это слой (видно по логам, [1/4]...[4/4] - этапы).

### Файл .dockerignore
С помощью файла **.dockerignore** можно ускорить сборку образа, указав Docker на то, какие директории можно **проигнорировать**.

Если вы знакомы с файлом **.gitignore**, структура этого файла, наверняка, покажется знакомой. В нём перечисляются директории, которые система сборки образа может проигнорировать. 

> Файл .dockerignore должен находиться в той же папке, что и файл Dockerfile. Теперь сборка образа будет занимать считанные секунды.

### Работа с командами Docker
Для взаимодействия с Docker используется **клиент Docker**, чтобы обратиться к клиенту используют ключевое слово `docker`. Затем клиент использует **API Docker** для отправки команд **демону Docker** - серверу Docker. Команды выполняются через командную строку - cmd.  

`docker` - вывод документации  
`docker version` - версия Docker  

### Команды для работы с образом
`docker build .` - создать образ из Dockerfile (`.` - текущая директория)  
`docker rmi image_id` - удалить образ  
`docker image prune` - удалить все образы  

`docker images` - список образов  

Хорошей практикой будет использовать следующие параметры при использовании команды `docker build` (при создании образа):

* `-t image_name` - задать имя образа  
* `-t image_name:tag` - задать имя образа с тегом (версией)

### Команды для работы с контейнером
`docker run image_id` - создать новый контейнер из образа  
`docker rm container_id` - удалить контейнер  
`docker container prune` - удалить все незапущенные контейнеры  

`docker start container_id` - запустить контейнер  
`docker stop container_id` - остановить запущенный контейнер

`docker ps` - список запущенных контейнеров  
`docker ps -a` - список всех контейнеров  

`docker logs container_id` - извлечь логи из контейнера  
`docker attach container_id` - зайти внутрь контейнера

Хорошей практикой будет использовать следующие **параметры** при использовании команды `docker run` (при создании контейнера):

* `-p 3000:3000` - управление портами, первым указывается номер порта хоста, то есть локального компьютера, а вторым - порт контейнера, на который должен быть перенаправлен запрос

> Перенаправление портов  
Система осуществляет перенаправление запросов с порта hostPort на порт containerPort. То есть обращение к порту 80 компьютера перенаправляется на порт 80 контейнера.

* `-d` - включить detach режим, чтобы не блокировалась консоль
* `--name container_name` - задать имя контейнеру
* `--rm` - удалить контейнер сразу после остановки

`docker run -d -p 3000:3000 --name new_cont --rm image_id`

`docker COMMAND --help` - параметр *--help* позволяет вывести документацию на команду  

--- 
## Kubernetes (K8S) 
### Суть технологии
**Kubernetes** - платформа, которая автоматизирует распределение и выполнение контейнеров приложений для запуска в **кластере** более эффективным образом.

  Задача Kubernetes заключается в координации кластера компьютеров, работающего как **одно целое**. Абстрактные объекты в Kubernetes позволяют развертывать контейнеризированные приложения в кластер, **не привязывая** их к отдельным машинам. 

### Схема кластера
Кластер Kubernetes состоит из двух типов ресурсов:
* Мастер - ведущий узел, который управляет кластером.
* Рабочие узлы - машины, на которых выполняются приложения.

**Узел** - это виртуальная машина или физический компьютер, который выполняет роль рабочего узла в кластере Kubernetes.

У каждого узла есть **Kubelet** - агент, управляющий узлом и взаимодействующий с ведущим узлом Kubernetes. Узел также имеет инструменты для выполнения контейнерных операций, например, **Docker** или rkt. Узлы взаимодействуют с ведущим узлом посредством **API Kubernetes**, который предлагает ведущий узел.

> Запрос -> API Server -> Kubelet -> Pod

### Pod
Pod - минимальная развертываемая единица в K8S, набор из одного и более контейнеров, имеющих общее пространство имен и тома общей файловой системы.

> Надо отметить, что контейнеры имеют собственные изолированные файловые системы, но они могут совместно использовать данные, пользуясь ресурсом K8S, который называется **Volume (том)**.

У каждого пода есть уникальный IP-адрес. Для описания пода пишут манифест (manifest file).

Kubernetes-кластер может быть развернут на **физических** или **виртуальных** машинах. Чтобы начать работать с Kubernetes, можно использовать **Minikube**. 

Итого:
1. Kubernetes позволяет приложениям абстрагироваться от инфраструктуры, давая нам простое API, к которому можно отправлять запросы.
2. Kubernetes способствует стандартизации работы с провайдерами облачных услуг (Cloud Service Provider, CSP).

--- 
## Minikube
### Суть технологии
**Minikube** - это упрощённая реализация Kubernetes, которая создает виртуальную машину на вашем локальном компьютере и разворачивает простой кластер с одним узлом. Minikube доступен для Linux, macOS и Windows.

---
## Ход работы и мои замечания

> Установить Docker на рабочий компьютер

В разделе "Полезные ссылки" есть полный курс по Docker на YouTube, **серия из 6 статей про Docker на Habr**, а также ссылки на скачивание программы Docker и расширения Docker для VSCode.

При работе с Docker столкнулся с ошибкой #1.

> Установить Minikube используя оригинальную инструкцию

В разделе "Полезные ссылки" есть руководства по Kubernetes (K8S) и Minikube.

При работе с Minikube столкнулся с ошибкой #2.

### Создание контейнера vault
Скачиваем образ vault командой `docker pull vault`.  
Проверяем, что появился образ vault - `docker images`.

![Образ vault](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab1/images/vault_image.png 'Образ vault')

Создаем контейнер на основе образа vault - `docker run -d --name vault vault`.  
Проверяем, что появился контейнер vault - `docker ps -a`.  

![Контейнер vault](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab1/images/vault_container.png 'Контейнер vault')

### Создание Pod
Запускаем minikube - `minikube start`.  
Проверяем, что появился узел - `kubectl get nodes`.  

Создадим **manifest file**, в котором будет описан наш под.  

Для создания корректного описания манифеста в YAML-формате достаточно знать только два типа структур:

* списки (lists)
* мапы (maps)

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: vault
  labels:
    environment: dev
    tier: vault
spec:
  containers:
    - name: vault
      image: vault
      ports:
        - containerPort: 8200
```
Переходим в папку с .yaml файлом и выполняем команду `kubectl create -f vault_pod.yaml`.

> На данном этапе я столкнулся с ошибкой #3, так как не добавил метку в манифест пода.

Проверяем, что появился Pod - `kubectl get pods`.

![Pod vault](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab1/images/vault_pod.png 'Pod vault')

### Создание сервиса
Создаем сервис для доступа к Pod - `minikube kubectl -- expose pod vault --type=NodePort --port=8200`.

![Service vault](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab1/images/vault_service.png 'Service vault')

Перенаправляем трафик с Pod на локальный - `minikube kubectl -- port-forward service/vault 8200:8200`.

![Port-forward](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab1/images/port_forward.png 'Port-forward')

Открываем страницу авторизации Vault `http://localhost:8200`.

![Vault page](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab1/images/localhost.png 'Vault page')

### Поиск токена
Чтобы найти токен для авторизации, открываем второй терминал и используем команду ~~`docker logs vault`~~ или `minikube kubectl -- logs service/vault`.

> Root Token: hvs.LlAzp5F68hfi8M90qGBa7wPa

![Successful authorization](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab1/images/auth_success.png 'Successful authorization')

Работа выполнена - останавливаем узел командой `minikube stop`.

### Диаграмма
Схема организации контейнера и сервиса, нарисованная в [draw.io](https://app.diagrams.net/).

![Диаграмма](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab1/images/lab1_diagram.png 'Диаграмма')

---
## Ошибки (в хронологическом порядке)
1. Docker не запускался на Windows 10.

> Docker daemon fails to start up on Windows or stops for some reason and when you try to run any commands:  
error during connect: Get http://%2F%2F.%2Fpipe%2Fdocker_engine/v1.30/info: open //./pipe/docker_engine: The system cannot find the file specified. In the default daemon configuration on Windows,
the docker client must be run elevated to connect. This error may also indicate that the docker daemon is not running.

* Решение  
Установка [пакета](https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi) обновления ядра Linux в WSL 2 для 64-разрядных компьютеров с [официальной страницы Microsoft](https://learn.microsoft.com/ru-ru/windows/wsl/install-manual#step-4---download-the-linux-kernel-update-package).

2. Minicube не работал
> Unable to connect to the server: dial tcp [::1]:8080: connectex: No connection could be made because the target machine actively refused it.

* Решение  
В Docker desktop надо было отметить [Enable Kubernetes](https://stackoverflow.com/questions/50490808/unable-to-connect-to-the-server-dial-tcp-18080-connectex-no-connection-c).

3. Не добавил labels в manifest
> error: couldn't retrieve selectors via --selector flag or introspection: the pod has no labels and cannot be exposed

* Решение  
Удаляем Pod `kubectl delete pod vault`.

Дописываем любые метки, например environment и tier. Метки позволяют понять сервису, с какими именно подами ему нужно работать.

```
labels:
  environment: dev
  tier: vault
```

Заново создаем Pod `kubectl create -f vault_pod.yaml`.

---
## Полезные ссылки
### Docker
1. Установка Docker с [официального сайта](https://www.docker.com/)  
2. Расширение для работы с [Docker](https://code.visualstudio.com/docs/containers/overview) в VSCode
3. [Docker для Начинающих - Полный Курс](https://www.youtube.com/watch?v=n9uCgUzfeRQ) (для ознакомления)
4. [Изучаем Docker, часть 1: основы](https://habr.com/ru/company/ruvds/blog/438796/)
5. [Изучаем Docker, часть 2: термины и концепции](https://habr.com/ru/company/ruvds/blog/439978/)
6. [Изучаем Docker, часть 3: файлы Dockerfile](https://habr.com/ru/company/ruvds/blog/439980/)
7. [Изучаем Docker, часть 4: уменьшение размеров образов и ускорение их сборки](https://habr.com/ru/company/ruvds/blog/440658/)
8. [Изучаем Docker, часть 5: команды](https://habr.com/ru/company/ruvds/blog/440660/)
9. [Изучаем Docker, часть 6: работа с данными](https://habr.com/ru/company/ruvds/blog/441574/)

### Kubernetes
1. [Основы Kubernetes](https://kubernetes.io/ru/docs/tutorials/kubernetes-basics/) на русском
2. [Руководство по Kubernetes, часть 1: приложения, микросервисы и контейнеры](https://habr.com/ru/company/ruvds/blog/438982/)
3. [Руководство по Kubernetes, часть 2: создание кластера и работа с ним](https://habr.com/ru/company/ruvds/blog/438984/)
4. [Полезные команды и советы при работе с Kubernetes через консольную утилиту kubectl](https://habr.com/ru/company/flant/blog/333956/)
5. [Как эффективнее использовать kubectl: подробное руководство](https://habr.com/ru/company/vk/blog/502828/)
6. [Руководство по Minikube](https://kubernetes.io/ru/docs/tutorials/hello-minikube/) на русском

### Vault
1. [Как не хранить секреты где придётся, или зачем нам Hashicorp Vault](https://habr.com/ru/post/306812/)
2. [Управление всеми вашими секретами с помощью Vault. Обзор и практические примеры.](https://khannz.medium.com/rus-hashi-vault-intro-1615ae2c0116)