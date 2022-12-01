University: [ITMO University](https://itmo.ru/ru/)  
Faculty: [FICT](https://fict.itmo.ru)  
Course: [Introduction to distributed technologies](https://github.com/itmo-ict-faculty/introduction-to-distributed-technologies)  
Year: 2022/2023  
Group: K4111c  
Author: Briushinin Anatolii Alekseevich  
Lab: Lab3  
Date of create: 21.10.2022  
Date of finished: -

# Лабораторная работа №3 "Сертификаты и "секреты" в Minikube, безопасное хранение данных."

## Описание
В данной лабораторной работе вы познакомитесь с сертификатами и "секретами" в Minikube, правилами безопасного хранения данных в Minikube.

## Цель работы
Познакомиться с сертификатами и "секретами" в Minikube, правилами безопасного хранения данных в Minikube.

---
## Ликбез

### ConfigMaps
Из официальной документации [ConfigMap](https://kubernetes.io/docs/concepts/configuration/configmap/) - это объект API, используемый для хранения **неконфиденциальных** данных в парах ключ-значение.

ConfigMaps позволяют разделить данные конфигурации и код приложения, при этом объем данных не должен превышать 1 Мб.

### Secrets
Из официальной документации [Secret](https://kubernetes.io/docs/concepts/configuration/secret/) - это объект, содержащий небольшое количество **конфиденциальных** данных, таких как пароль, токен или ключ.

По сути это те же ConfigMaps только для хранения конфиденциальных данных, при этом данные кодируются в base64.

### ReplicaSets
Из официальной документации [ReplicaSet](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/) - ресурс K8S, который гарантирует работу определенного числа реплик Pod.

### TLS
SSL расшифровывается как Secure Sockets Layer, **TLS – Transport Layer Security**. Сертификат представляет собой технологию безопасности, с помощью которой шифруется связь между браузером и сервером. Из-за такого сертификата сложнее украсть или подменить данные пользователей. SSL/TLS-сертификат устанавливают на сервер. Помимо шифрования всех коммуникаций, с его помощью можно проверить подлинность веб-сайта.

> сертификат с публичным ключом для шифрования, приватный ключ для расшифровки

### Ingress
[Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) - ресурс, с помощью которого мы можем задать единую точку входа в наш кластер. Ingress позволяет нам назначить для каждого сервиса свой URL, доступный вне кластера.
---
## Ход работы и мои замечания

### Создание ConfigMap
Запускаем minikube - `minikube start`. Иначе **context (контекст)** будет не minikube, а другой - например docker-desktop, и после запуска minikube, ваше развертывание не будет видно.

Пример манифеста для ConfigMap, также как и для остальных ресурсов K8S можно найти в [официальной документации](https://kubernetes.io/docs/concepts/configuration/configmap/).

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: frontend-configmap
data:
  react_app_user_name: "Anatolii"
  react_app_company_name: "ITMO"
```
По ключам `react_app_user_name` и `react_app_company_name` будем хранить значения для переменных REACT_APP_USERNAME и REACT_APP_COMPANY_NAME, соответственно.

Переходим в папку с .yaml файлом и выполняем команду `kubectl create -f frontend-configmap.yaml`.

Проверяем, что появился ConfigMap - `kubectl get configmaps`.

![configmap](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab3/images/configmap.png 'configmap')

### Создание ReplicaSet
Пример манифеста для ReplicaSet в [официальной документации](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/).

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: frontend-replicaset
  labels:
    app: lab3-frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: lab3-frontend
  template:
    metadata:
      labels:
        app: lab3-frontend
    spec:
      containers:
      - name: frontend-container
        image: ifilyaninitmo/itdt-contained-frontend:master
        ports:
        - containerPort: 3000
        env:
        - name: REACT_APP_USERNAME
          valueFrom:
            configMapKeyRef:
              name: frontend-configmap
              key: react_app_user_name
        - name: REACT_APP_COMPANY_NAME
          valueFrom:
            configMapKeyRef:
                name: frontend-configmap
                key: react_app_company_name
```

Шаблон пода задается в объекте `Template`. С помощью свойства `env` объявляем внутри подов переменные окружения `REACT_APP_USERNAME` и `REACT_APP_COMPANY_NAME`, а их значения берем из ConfigMap frontend-configmap, который мы создали ранее.

Создаем контроллер командой - `kubectl create -f frontend-replicaset-manifest.yaml`.

Проверяем, что появился контроллер - `kubectl get rs`.

![replicaset](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab3/images/configmap.png 'replicaset')

### Создание сервиса
Для создания Inngress ресурса потребуется сервис, поэтому пишем манифест по шаблону из [официальной документации](https://kubernetes.io/docs/concepts/services-networking/service/)

```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
  labels:
    app: lab3-frontend
spec:
  type: NodePort
  selector:
    app: lab3-frontend
  ports:
    - protocol: TCP
      port: 3000
      targetPort: 3000
      nodePort: 30333
```

> Доступны только порты 30000–32767, пусть `nodePort` 30333.

Согласно [документации на Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/), этот ресурс работает с сервисами типа `NodePort` или `LoadBalancer`, поэтому указываем в поле `type` один из этих типов.

Посмотреть список используемых портов можно командой - `netstat -aon`.

> Note: A Service can map any incoming port to a targetPort. By default and for convenience, the `targetPort` is set to **the same value** as the `port` field.

Создаем сервис командой - `kubectl create -f frontend-service.yaml`. У меня уже был сервис с таким названием, но другого типа, удалил его.

Проверяем, что появился сервис - `kubectl get services`.

![service](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab3/images/service.png 'service')

### Генерация TLS
Для генерации TLS сертификата будем использовать инструмент командной строки [OpenSSL](https://losst.pro/sozdanie-sertifikata-openssl). [Скачиваем по ссылке](https://slproweb.com/products/Win32OpenSSL.html).

Чтобы утилитой можно было пользоваться из cmd, добавляем в [переменную среды PATH](https://lumpics.ru/environment-variables-in-windows-10/) путь к bin папке, по сути следуем [инструкции](https://stackoverflow.com/questions/50625283/how-to-install-openssl-in-windows-10).

Генерируем приватный ключ [RSA](https://ru.wikipedia.org/wiki/RSA). Опция `-out` указывает на имя файла для сохранения ключа, а число `2048` - размер ключа в битах (по умолчанию 512).

`openssl genrsa -out lab3.key 2048`

![private key](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab3/images/private_key.png 'private key')

Для того чтобы получить сертификат, который можно использовать нужно этот ключ подписать. А для этого надо создать запрос на подпись.

`openssl req -key lab3.key -new -out lab3.csr`

![query for cert](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab3/images/query_for_cert.png 'query for cert')

При создании запроса на подпись нужно указать необходимую информацию. Обязательное поле здесь - это Common Name, например server FQDN or YOUR name.

Можно подписать сертификат тем же ключом, с помощью которого он был создан.

`openssl x509 -signkey lab3.key -in lab3.csr -req -days 30 -out lab3.crt`

![cert](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab3/images/cert.png 'cert')

### Создание Secret
Создаем секрет командой - `kubectl create secret tls lab3-tls --cert=lab3.crt --key=lab3.key`.

![secret](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab3/images/secret.png 'secret')

### Создание Ingress

Подключаем Ingress в minikube:

```
minikube addons enable ingress
minikube addons enable ingress-dns
```

![ingress on](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab3/images/ingress_on.png 'ingress on')

Манифест для Ingress пишем по шаблону из [официальной документации](https://kubernetes.io/docs/concepts/services-networking/ingress/).

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: frontend-ingress
spec:
  tls:
  - hosts:
      - frontend-lab3.anatolii
    secretName: lab3-tls
  rules:
  - host: frontend-lab3.anatolii
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend-service
            port:
              number: 3000
```

Добавляем `192.168.49.2 frontend-lab3.anatolii` в hosts файл, который лежит по пути: `C:\Windows\System32\drivers\etc`. Подробнее можно почитать [тут](https://windows10x.ru/hosts-windows-10/).

Создаем точку входа в кластер minikube командой - `kubectl create -f frontend-ingress.yaml`.

Проверяем, что появился Ingress - `kubectl get ingress`.

![ingress create](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab3/images/ingress_create.png 'ingress create')

Подключаемся к ingress командой - `minikube tunnel`.

`https://frontend-lab3.anatolii`

Видим наши параметры, переданные через ConfigMap:
![window](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab3/images/window.png 'window')

Данные сертификата:
![cert check](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab3/images/cert_check.png 'cert check')

### Диаграмма
Схема организации кластера minikube и ingress, нарисованная в [draw.io](https://app.diagrams.net/).

![Диаграмма](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab2/images/lab3_diagram.png 'Диаграмма')

---
## Ошибки (в хронологическом порядке)

---
## Полезные ссылки
1. [Kubernetes NodePort vs LoadBalancer vs Ingress? Когда и что использовать?](https://habr.com/ru/company/southbridge/blog/358824/)