# Лекционный курс "Введение в распределенные технологии 2022/2023"

## Список лекций
1. Введение в виртуализацию и контейнеризацию. Переход от монолита к микросервисам.
2. Архитектура Docker и Kubernetes, docker registry и все что с этим связано. Истории создания и основные идеи.
3. Диспетчеры и служебные сервисы Kubernetes. Мой первый "Pod"
4. Жизненый цикл микросервиса, ввод и вывод из эксплуатации. Ci/Cd на минималках.
5. Развертывание и эксплуатация Kubernetes кластера.
6. Безопасность и хранение данных в Kubernetes.
7. Сети связи в Kubernetes и "почему все так непонятно?"
8. БОНУС. Kubernetes у больших дяденек и как они делают бизнес с Kubernetes.

## 1. Введение в виртуализацию и контейнеризацию. Переход от монолита к микросервисам.

### Что такое ПО?
ПО - набор программ, алгоритмов, которые **решают задачи**, *автоматизируют* вычисления для **сокращения расходов**.

### Монолитная архитектура
Когда бизнес-логика, БД и GUI находится в одном месте, все элементы жестко связаны.

Невозможно изменить какой-то элемент, не затронув остальные.

Пример: сковородка.

### Микросервисная архитектура
Когда есть отдельно GUI, который связан со множеством микросервисов, которые связаны с БД.  

Docker-контейнер по сути и есть микросервис.

Пример: автомобиль.

> Архитектура выбирается в зависимости от размера приложения.

> Надо помнить про инженерный подход: для решения задачи необходимо прикладывать минимальное количество усилий.

### Как сделать ПО? 
Разработка программного продукта знает много достойных **методологий** — иначе говоря, устоявшихся best practices.

Оригинальная статья: [Ещё раз про семь основных методологий разработки
](https://habr.com/ru/company/edison/blog/269789/).

1. **Waterfall Model**  
   Подразумевает последовательное прохождение стадий, каждая из которых должна **завершиться полностью** до начала следующей.  

   Подходит только для проектирования **монолитной** архитектуры.   
   
   Сложно подстраивается под постоянно меняющийся рынок.

2. **Incremental Model**  
   Сначала реализуется **базовый** функционал, потом докручивается **дополнительный**.  
   
   Возможно применить для проектирования **монолитной** архитектуры, но **не рекомендуется**.

   Минусом методологии является то, что базовый функционал может быть **изначально не приспособлен** к какой-нибудь дополнительной функции, которую захотели внедрить.
   
   Пример: хотим превратить двухэтажный домик в небоскреб - небоскреб развалится, так как у него был фундамент домика.

3. **Agile Model**  
   Каждая команда работает над отдельной функцией в рамках **спринтов**, что позволяет быстро делать [MVP](https://ru.wikipedia.org/wiki/Минимально_жизнеспособный_продукт). То есть все разделено, общей может быть шина передачи данных.

   Преимущество такого подхода в том, что разработчик может знать только API другой функции и не разбираться, как работает кусок чужого кода.

   Подходит только для проектирования **микросервисной** архитектуры.

> Сначала появились подходы, а уже потом технологии!

### Микросервис
Можно понимать микросервис, как **запчасть автомобиля**. Есть сервис автомобиль, который состоит из микросервиса руля, микросервиса кресло и т.д.

### Виртуализация
Главная идея виртуализации- оптимизация расходывания ресурсов.

* Программная виртуализация
* Аппаратная виртуализация - лучше, чем программная. Например, Intel-VT и AMD-V.

[Гипервизор (оркестратор)](https://habr.com/ru/company/vps_house/blog/349788/) - ОС, которая позволяет запускать на себе другие ОС. Например, Hyper-V, VirtualBox.

### Причем тут Docker?
**Docker** - средство виртуализации, но это не виртуальная машина.

ВМ разворачивает **гостевую ОС**, а Docker делает **изолированное окружение**, то есть делит основную ОС на куски. Внутри каждого контейнера есть только код. Docker работает **быстрее** ВМ.

### Kubernetes
**Kubernetes** - система управления Docker, развернутых на **кластере**. Изначально была разработкой компании Google.

Позволяет развернуть контейнеры на множестве серверов.

### Fan Facts
1. «Минск-1» — первая оригинальная белорусская ЭВМ.
2. Первый «русский хакер» создал "программную бомбу" для остановки конвейера на АвтоВАЗе, чтобы заработать премиальные за ремонт.
3. Cyberpunk 2077 разрабатывали методологией Waterfall, поэтому было долго, тяжело и по итогу в игре оказалось много багов.

## 2. Архитектура Docker и Kubernetes, docker registry и все что с этим связано. Истории создания и основные идеи.

### Архитектура Docker

В документации есть [схема](https://docs.docker.com/engine/images/architecture.svg).

![Docker architecture](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/images/docker_architecture.png 'Архитектура Docker')

По сути есть три части:
* Client (мы)
* Docker Host (наша машина)
* Registry (хранилище образов)

В отчете lab1_report.md есть шпаргалка по Docker.

**Проброс порта**  
Когда мы сопоставляем порты компьютера и порты docker (например, port-forward 8200:8200), мы связываем изолированное окружение контейнера с нашем компьютером - образуем сеть.

### Архитектура Kubernetes

![K8S architecture](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/images/k8s_architecture.jpg 'Архитектура K8S')

Элементы:
* Master Node (Control Plane) - управляет кластером
   * API Server настраивает Container Runtime и kube-proxy, разработчик общается с API Server с помощью утилиты kubectl
   * Scheduler - следит за Pods, не распределенными на Worker Node, он выбирает им подходящую ноду по множеству критериев
   * Сontroller-manager - запускает Controllers (ресурс K8S), которые подписываются в API Server на свой ресурс
   * etcd (key-value store) - база данных, типа ключ-значение, как MongoDB, там хранятся все переменные, по сути туда записывается состояние системы, K8S кластер можно полностью восстановить, имея резервную копию etcd
* Worker Node (Data Plane) - железка, в ней 3 монстра, не считая элементов (k8s objects)
   * kubelet - агент, связывает Container Runtime и API Server
      > The Container Runtime Interface (CRI) is the main protocol for the communication between the kubelet and Container Runtime.
      * CRI - это плагин, позволяющий kubelet'у использовать разные исполняемые среды контейнеров
   * Container Runtime - это программа, предназначенная для выполнения контейнеров, по сути Docker, в первой лабе - **Pod**
   * kube-proxy
      * то с чем работает user - тот самый **сервис**, который создавали для Pod в первой лабе
      * нужен для настройки сетевого трафика в Pods, то есть частично реализует концепцию Сервиса
      * конфигурирует правила сети на узлах
      * при помощи него разрешаются сетевые подключения к Pods изнутри и снаружи кластера

# 3. Диспетчеры и служебные сервисы Kubernetes. Мой первый "Pod"

## Пример служебного сервиса?
[Container Networking Interface (CNI)](https://habr.com/ru/company/flant/blog/329830/) - служебный сервис организует сетевое взаимодействие между ресурсами K8S.


# 4. Жизненый цикл микросервиса, ввод и вывод из эксплуатации. Ci/Cd на минималках.

## Жизненный цикл ПО
В общем виде жизненный цикл ПО выглядит так:

> ТЗ -> проектирование -> разработка -> тестирование -> развертывание -> поддержка -> вывод из эксплуатации

При этом некоторые этапы имеют **обратную связь**, например возвращение на этап разработки после этапа тестирования.

## Ci/Cd

~~Формальное определение~~ Ci/Cd (Continuous Integration, Continuous Delivery — непрерывная интеграция и доставка) — это технология автоматизации тестирования и доставки новых модулей разрабатываемого проекта заинтересованным сторонам (разработчики, аналитики, инженеры качества, конечные пользователи и др.). Почитать подробнее можно [тут](https://selectel.ru/blog/what-is-ci-cd/) и [тут](https://medium.com/@thulanakannangara/ci-cd-pipeline-for-orangehrm-open-source-application-89ef2dddc929).

Ci/Cd - методология (aka философия, стиль жизни), по сути модель эффективного управления бизнесом.

Любой код создан, чтобы решать задачи, благодаря этому компания зарабатывает. Если из-за плохого тестирования при деплои новой версии приложения, система умрет на 10 минут, то компания будет нести убытки. Если с сервиса зарабатывался 1 млн руб./мин., то за время простоя в 10 минут компания потеряет 10 млн руб.

Чтобы такого недопустить используют методологию Ci/Cd, при этом реализована она может быть абсолютно разными инструментами.

![Ci/Cd](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/images/ci_cd.png 'Ci/Cd')

Как только нагрузка на сервис увеличивается, снижаются расходы на эксплуатацию (происходит более эффективное расходывание ресурсов).

С помощью сервиса [sketchpad](https://sketchpad.app/) изобразим три графика:

![Plots](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/images/ci_cd_plots.png 'Ci/Cd plots')

Таким образом, Ci/Cd позволяет не терять деньги.

## GitOps
GitOps - тоже методология, подробнее о ней можно прочитать здесь:
1. [Методология GitOps на русском](https://habr.com/ru/company/flant/blog/526102/)
2. [Методология GitOps на английском](https://www.gitops.tech/)

### Helm
Helm - система шаблонизации для развертывания софта. Например, с помощью библиотеки шаблонизации для python jinja2, можно автоматизировать написание манифестов для K8S.

# 5. Развертывание и эксплуатация Kubernetes кластера.

Принципиально существует 2 типа развертывания:
* On-premise (на железе)
   * Вам предоставляется ВМ и вы руками что-то устанавливаете на конкретные компьютеры.
* Cloud (в облаке)
   * Компания предоставляет **услугу** по выделенным вычислениям, которые выполняются на **их инфраструктуре**.
   * У облачных провайдеров есть свой **API** и с ними можно взаимодействовать, как с интерфейсом, например с помощью [Terraform](https://habr.com/ru/company/otus/blog/696694/).

## On-prem

### kubeadm (Simpleway)
Самый простой способ создать кластер - это использовать инструмент [kubeadm](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/).

Всего будет необходимо установить три вещи:
* kubeadm - программа для настройки K8S кластера.
   * развертывает кластер: прописывает настройки, конфигы, выпускает сертификаты.
* kubectl - это инструмент командной строки для управления кластерами K8S.
* kubelet - агент K8S, связывающий мастер-узел и рабочие узлы.

В документации есть требования к установке (Linux машина, полная сетевая связность со всеми элементами в кластере и т.д) и все шаги.

Кроме того, необходимо установить контейнерную среду выполнения - **Container Runtime Interface (CRI)**:
* containerd
* CRI-O
* Docker Engine (using cri-dockerd)
* ~~rkt~~

Далее следовать шагам из официальной [документации](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/).

Для инициализации control-plane (мастер-узла) используют команду - `kubeadm init <args>`.

### Hardway
Есть более долгий путь, в котором вы вручную прописывайте конфигурацию, создаете сертификаты и т.д.

Репозиторий с описанием процесса: [Kubernetes The Hard Way](https://github.com/kelseyhightower/kubernetes-the-hard-way)

### Как развертывать быстрее?
Использовать систему для удаленного управления конфигурациями [Ansible](https://habr.com/ru/company/selectel/blog/196620/).

**Ansible** — этот продукт с открытым кодом, который автоматизирует подготовку облачных решений, управление конфигурацией и развертывание приложений.

[Достать до звезд: Осваиваем операторы Ansible для управления приложениями в Kubernetes](https://habr.com/ru/company/redhatrussia/blog/440188/)

## Cloud

### Google Cloud Platform (GCP)

Первым шагом включаем K8S Engine API. Каждый API-сервер GCP - это отдельный микросервис.

Для взаимодействия с GCP используем приложение GCloud - `gcloud auth login`.

В качестве примера, был создан кластер и развернуто два приложения nginx и vault.

Также использовалась команда `gcloud config set compute/zone ZONE_NAME` и др.

GCP предоставляет *кластеру (?)* **белый-IP**.

### Что такое nginx? Веб-сервер?
Нет, в K8S nginx - это балансировщик, он видит запрос и перенаправляет на сервис, а у каждого Pod свой веб-сервер (типо L7-balancer). Прочитать, как работает NGINX Ingress Controller  можно [тут](https://docs.nginx.com/nginx-ingress-controller/intro/how-nginx-ingress-controller-works/).

### Как делают deploy приложения?
На практике, чтобы распространить приложение пишется **Helm chart** (шаблон).

> Нормальные разработчики пишут ingress.

### ~~Можно ли добавить МО к K8S?~~
[Технологическая сингулярность](https://ru.wikipedia.org/wiki/Технологическая_сингулярность).