University: [ITMO University](https://itmo.ru/ru/)  
Faculty: [FICT](https://fict.itmo.ru)  
Course: [Introduction to distributed technologies](https://github.com/itmo-ict-faculty/introduction-to-distributed-technologies)  
Year: 2022/2023  
Group: K4111c  
Author: Briushinin Anatolii Alekseevich  
Lab: Lab2  
Date of create: 21.10.2022  
Date of finished: 17.11.2022

# Лабораторная работа №2 "Развертывание веб сервиса в Minikube, доступ к веб интерфейсу сервиса. Мониторинг сервиса."

## Описание
В данной лабораторной работе вы познакомитесь с развертыванием полноценного веб сервиса с несколькими репликами.

## Цель работы
Ознакомиться с типами "контроллеров" развертывания контейнеров, ознакомится с сетевыми сервисами и развернуть свое веб приложение.

---
## Ликбез

## Deployment (развертывание)
Deployment - ресурс K8S, который позволяет автоматизировать процесс перехода от одной версии приложения к другой без прерывания работы системы.

* Поддержание системы в нужном состоянии (например, если мы удалим из развертывания 1 под, K8S запустет другой)
* Выполнение развёртываний с нулевым временем простоя системы
* Откат к предыдущему состоянию системы

---
## Ход работы и мои замечания

### Создание контейнера frontend-container
Скачиваем образ itdt-contained-frontend командой `docker pull ifilyaninitmo/itdt-contained-frontend:master`.

Проверяем, что появился образ itdt-contained-frontend - `docker images`.

![Образ itdt-contained-frontend](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab2/images/itdt-contained-frontend_image.png 'Образ itdt-contained-frontend')

Создаем контейнер на основе образа itdt-contained-frontend - `docker run -d --name frontend-container ifilyaninitmo/itdt-contained-frontend:master`.

Проверяем, что появился контейнер frontend_container - `docker ps -a`.  

![Контейнер frontend-container](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab2/images/frontend-container.png 'Контейнер frontend-container')

### Создание Deployment

Запускаем minikube - `minikube start`. Иначе **context (контекст)** будет не minikube, а другой - например docker-desktop, и после запуска minikube, ваше развертывание не будет видно.

Пример манифеста для развертывания, также как и для пода можно найти в [официальной документации](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/).

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  labels:
    app: frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend_pod
  template:
    metadata:
      labels:
        app: frontend_pod
    spec:
      containers:
      - name: frontend-container
        image: ifilyaninitmo/itdt-contained-frontend:master
        ports:
        - containerPort: 3000
        env:
        - name: REACT_APP_USERNAME
          value: Anatolii
        - name: REACT_APP_COMPANY_NAME
          value: ITMO
```

~~Чтобы посмотреть переменные окружения используем команду `kubectl explain env`.~~

Чтобы запустить 2 экземпляра пода, используем свойства `replicas: 2`.

Шаблон пода задается в объекте `Template`. С помощью свойства `env` объявляем внутри подов переменные окружения `REACT_APP_USERNAME` и `REACT_APP_COMPANY_NAME` со значениями `Anatolii` и `ITMO`, соответственно.

Переходим в папку с .yaml файлом и выполняем команду `kubectl create -f frontend-deployment.yaml`.

> На этом моменте я столкнулся с ошибкой #1, потому что в названии конейнера был символ нижнего подчеркивания.

Проверяем, что появилось развертывание - `kubectl get deployments`.

![frontend deployment](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab2/images/frontend_deployment.png 'frontend deployment')

### Создание сервиса frontend-service

Создаем сервис для доступа к развертыванию - `minikube kubectl -- expose deployment frontend --port=3000 --target-port=3000 --name=frontend-service --type=LoadBalancer`.

Тип сервиса `LoadBalancer` будет решать задачу балансировки нагрузки между подами.

![frontend service](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab2/images/frontend_service.png 'frontend service')

Пробрасываем локальный порт на порт контейнера - `minikube kubectl -- port-forward service/frontend-service 3000:3000`.

![Port-forward](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab2/images/port_forward.png 'Port-forward')

Открываем страницу `http://localhost:3000`.

![Frontend page](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab2/images/frontend_page.png 'Frontend page')

### Логи подов

Посмотрим список всех подов - `minikube kubectl get pods`. Как и должно было быть, deployment запустил 2 пода.

![Pods](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab2/images/get_pods.png 'Pods')

Смотрим логи первого пода - `minikube kubectl -- logs pod/frontend-9c975bc96-b5q2z`.

![Log pod 1](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab2/images/log_pod1.png 'Log pod 1')

Смотрим логи второго пода - `minikube kubectl -- logs pod/frontend-9c975bc96-kh262`.

![Log pod 2](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab2/images/log_pod2.png 'Log pod 2')

Чтобы удалить развертывание используем команду - `kubectl delete deployments/frontend`.

Проверяем - `kubectl get deployments` и останавливаем minikube командой `minikube stop`.

### Итоги
1. Ресурс deployment позволяет создавать несколько подов на основе одного контейнера.
2. Сервис типа LoadBalancer - эта абстракция, которая позволяет нам воспринимать группу подов (с одинаковой меткой) как единую сущность и работать с ними, используя сервис как единую точку доступа к ним.

    Именно поэтому логи первого и второго пода идентичны.

### Диаграмма
Схема организации контейнера и сервиса, нарисованная в [draw.io](https://app.diagrams.net/).

![Диаграмма](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab2/images/lab2_diagram.png 'Диаграмма')

---
## Ошибки (в хронологическом порядке)

1. Нельзя использовать символ нижнего подчеркивания в названии контейнера, который будет использоваться в K8S.

> The Deployment "frontend" is invalid: spec.template.spec.containers[0].name: Invalid value: "frontend_container": a lowercase RFC 1123 label must consist of lower case alphanumeric 
characters or '-', and must start and end with an alphanumeric character (e.g. 'my-name',  or '123-abc', regex used for validation is '[a-z0-9]([-a-z0-9]*[a-z0-9])?')

* Решение  
Удаляем контейнер и создаем с новым названием.

---
## Полезные ссылки
1. [Руководство по Kubernetes, часть 2: создание кластера и работа с ним](https://habr.com/ru/company/ruvds/blog/438984/)