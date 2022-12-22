University: [ITMO University](https://itmo.ru/ru/)  
Faculty: [FICT](https://fict.itmo.ru)  
Course: [Introduction to distributed technologies](https://github.com/itmo-ict-faculty/introduction-to-distributed-technologies)  
Year: 2022/2023  
Group: K4111c  
Author: Briushinin Anatolii Alekseevich  
Lab: Lab4  
Date of create: 21.10.2022  
Date of finished: -

# Лабораторная работа №4 "Сети связи в Minikube, CNI и CoreDNS"

## Описание
Это последняя лабораторная работа в которой вы познакомитесь с сетями связи в Minikube. Особенность Kubernetes заключается в том, что у него одновременно работают underlay и overlay сети, а управление может быть организованно различными CNI.

## Цель работы
Познакомиться с CNI Calico и функцией IPAM Plugin, изучить особенности работы CNI и CoreDNS.

---
## Ликбез

### Network Policy

[NetworkPolicy (сетевая политика)](https://kubernetes.io/docs/concepts/services-networking/network-policies/) - ресурс K8S для управления трафиком, проходящим через кластер.

Как уже отмечалось в описании лабораторной работы, в K8S одновременно работают **underlay** и **overlay** сети, что отражено в документации:

> Kubernetes NetworkPolicies allow the control of pod network traffic passing through the cluster, at the IP address or port level (OSI layer 3 or 4).

Можно регулировать трафик, проходящий через Pod как на **Cетевом (3)**, так и на **Транспортном (4)** уровне модели [OSI](https://habr.com/ru/company/serverspace/blog/689704/).

* Underlay сеть - это **физическая IP сеть** со стабильной конфигурацией. Это база поверх которой уже строится overlay сеть.

* Overlay сеть - это **виртуальная сеть туннелей**, натянутая поверх underlay, она позволяет ВМ одного клиента общаться друг с другом, при этом обеспечивая изоляцию от других клиентов.

### CNI

Чтобы разобраться какую роль играет **Интерфейс контейнерной сети (CNI)** в системе, K8S рекомендую прочитать статью [Как pod в Kubernetes получает IP-адрес](https://habr.com/ru/company/flant/blog/521406/).

Проект **CNI** представляет собой **спецификацию** для организации универсального сетевого решения для Linux-контейнеров.

Другими словами, **CNI** - **набор требований** к исполняемой среде контейнеров (container runtimes) и плагинам (plugins), соответствие которым позволяет любому плагину работать с любым runtime'ом.

**Плагин CNI (CNI plugin)** - это исполняемый файл, соответствующий спецификации. Существуют плагины, отвечающие за различные функции **при настройке сети** Pod'а. 

CNI, который используется в Minikube по-умолчанию, не поддерживает никакую NetworkPolicy, поэтому необходимо установить другую CNI - **Calico**.

**Calico** является **сетевым "провайдером"**, который обеспечивает каждому Pod'у в кластере свой IP.

У каждого сетевого провайдера имеется свой **CNI plugin**.

> Runtime контейнера запускает CNI plugin, чтобы **сконфигурировать сеть** для Pod'a в процессе его запуска.

При этом у каждого провайдера есть свой **агент**. Он устанавливается во все узлы K8S и **отвечает за сетевую настройку** Pod'ов. Этот агент идет либо в комплекте с конфигом CNI, либо самостоятельно создает его на узле. Конфиг помогает CRI plugin установить, какой CNI plugin вызывать.

### Что происходит при создании Pod'a?
**kubelet** вызывает **CRI plugin**, чтобы создать Pod, а тот уже вызывает **CNI plugin** для настройки сети Pod'а. При этом CNI plugin сетевого провайдера (например, Calico) вызывает другие базовые CNI plugins для настройки различных аспектов сети.

> kubelet -> CRI plugin -> CNI plugin -> configure the Pod network

Таким образом, CNI отвечает за организацию сетевого взаимодействия в K8S.

### IPAM
**IP address management (IPAM)** - служба управления IP адресами, используется Kubernetes'ом для выделения IP адресов Pod'ам.

IPAM представляет собой платформу для обнаружения, мониторинга, управления и аудита для пространства IP адресов в сети организации.

### CoreDNS
**CoreDNS** - DNS-сервер, появившийся в начале 2016 года (под свободной лицензией Apache License v2) как форк быстрого веб-сервера Caddy, написанного на языке Go. Сам HTTP-сервер в Caddy реализован пакетом httpserver, двумя важнейшими типами в котором являются Handler (функция обработки HTTP-запроса) и Middleware (промежуточный слой, прицепляющий один Handler к другому, — таким образом формируется цепочка из обработчиков).

> CoreDNS используется как Service Discovery для Kubernetes.

**Service Discovery (обнаружение сервисов)** позволяет приложению или компоненту получать информацию об их окружении и “соседях”. Как правило, данный функционал реализуется при помощи распределённого хранилища “ключ-значение” (“key-value”), которое также может служить для хранения деталей конфигурации. Настройка инструмента обнаружения сервисов позволяет разделить runtime-конфигурацию и сам контейнер, что позволяет использовать один и тот же образ в нескольких окружениях.

> Главная идея, лежащая в основе обнаружения сервисов, состоит в том, что любой новый экземпляр приложения должен быть в состоянии программно определить детали своего текущего окружения. Это необходимо для того, чтобы новый экземпляр мог подключиться к существующему окружению приложения без ручного вмешательства. 

* Service Discovery создан для того, чтобы с минимальными затратами можно подключить новое приложение в уже существующее окружение
* в Service Discovery могут храниться конфиги nginx, сертификаты и список активных backend-серверов
* Service Discovery позволяет обнаружить сбой, обнаружить отказы.

---
## Ход работы и мои замечания

### Calico и Multi-Node Clusters
При запуске minikube устанавливаем [плагин](https://projectcalico.docs.tigera.io/getting-started/kubernetes/minikube) `CNI=calico`, режим работы `Multi-Node Clusters` и разворачиваем [2 Node](https://minikube.sigs.k8s.io/docs/tutorials/multi_node/) командой:

```minikube start --network-plugin=cni --cni=calico --nodes 2 -p multinode-demo```

Проверяем, что запустились 2 Node: `kubectl get nodes`.

![get_nodes](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab4/images/get_nodes.png 'get_nodes')

Чтобы проверить работу CNI Calico, посмотрим Pod'ы с меткой **calico-node**: `kubectl get pods -l k8s-app=calico-node -A`.

![get_pods](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab4/images/get_pods.png 'get_pods')

### calicoctl и IPPool
Для назначения IP адресов в Calico необходимо написать манифест для **IPPool** ресурса.

С помощью IPPool можно создать IP-pool (блок IP-адресов), который выделяет IP-адреса только для узлов с определенной **меткой (label)**.

Чтобы назначить метки узлам, используем следующие команды: 
`kubectl label nodes multinode-demo zone=east`
`kubectl label nodes multinode-demo-m02 zone=west`

[Шаблон манифеста IPPool](https://projectcalico.docs.tigera.io/networking/assign-ip-addresses-topology) берем из официальной документации Calico:
```yaml
apiVersion: projectcalico.org/v3
kind: IPPool
metadata:
   name: zone-east-ippool
spec:
   cidr: 192.168.0.0/24
   ipipMode: Always
   natOutgoing: true
   nodeSelector: zone == "east"
---
apiVersion: projectcalico.org/v3
kind: IPPool
metadata:
   name: zone-west-ippool
spec:
   cidr: 192.168.1.0/24
   ipipMode: Always
   natOutgoing: true
   nodeSelector: zone == "west"
```

Чтобы применить манифест для IPPool, надо установить **calicoctl**, для этого скачаем [config-файл](https://github.com/projectcalico/calico/blob/master/manifests/calicoctl.yaml) с официального репозитория и выполним команду: `kubectl create -f calicoctl.yaml`.

![calicoctl_created](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab4/images/calicoctl_created.png 'calicoctl_created')

> Команды calicoctl начинаются с: `kubectl exec -i -n kube-system calicoctl -- /calicoctl --allow-version-mismatch`.

Перед тем, как добавить собственные IPPool'ы, проверим созданные по-умолчанию:
```kubectl exec -i -n kube-system calicoctl -- /calicoctl --allow-version-mismatch get ippools -o wide```

Удаляем IPPool по-умолчанию: `kubectl delete ippools default-ipv4-ippool`.

![delete_default_ippool](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab4/images/delete_default_ippool.png 'delete_default_ippool')

Создаем IPPool'ы:
```kubectl exec -i -n kube-system calicoctl -- /calicoctl --allow-version-mismatch create -f - < lab4-ippool.yaml```

IDE VS Code ругается на оператор `<` (аналог Get-Content), поэтому выполняю команды в cmd.

```
E:
cd E:\HDD\Magistracy\EducationCourses\ITMO\2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a\lab4
```

![create_ippools](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab4/images/create_ippools.png 'create_ippools')

Проверяем, что появилось два pool'а:
```kubectl exec -i -n kube-system calicoctl -- /calicoctl --allow-version-mismatch get ippool -o wide```

![ippools](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab4/images/ippools.png 'ippools')

Заметим, что их [маски подсети (CIDR)](https://ru.wikipedia.org/wiki/Маска_подсети) соответствуют тем, которые указаны в диапазон pool'ов в манифесте. Прочитать про CIDR можно [здесь](https://habr.com/ru/post/351574/).

### Deployment и Service
Манифест для развертывания берем из 2 лабораторной работы и заменяем метку на `lab4-frontend`.

[Шаблон манифеста](https://kubernetes.io/docs/tasks/access-application-cluster/create-external-load-balancer/?hl=ru) для сервиса типа Load-Balancer возьмем с официальной документации и также заменим метку на `lab4-frontend`.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: lab4-service
spec:
  selector:
    app: lab4-frontend
  ports:
    - port: 3000
      targetPort: 3000
  type: LoadBalancer
```

Переходим в папку с .yaml файлом и выполняем команду `kubectl apply -f lab4-deployment.yaml -f lab4-service.yaml`.

Проверяем, что появилось развертывание и сервис: `kubectl get deployments`, `kubectl get services`.

![create_deployment_and_service](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab4/images/create_deployment_and_service.png 'create_deployment_and_service')

Проверяем IP созданных Pod'ов: `kubectl get pods -o wide`.

![check_pods_ip](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab4/images/check_pods_ip.png 'check_pods_ip')

### Проброс порта
Пробрасываем порт для подключения к сервису через браузер: `kubectl port-forward service/lab4-service 8200:3000`

Переходим по ссылке: `http://localhost:8200/`.

![browser](https://github.com/AnatoliyBr/2022_2023-introduction_to_distributed_technologies-k4111c-briushinin_a_a/blob/master/lab4/images/browser.png 'browser')

### Попингуем?

---
## Ошибки (в хронологическом порядке)

---
## Полезные ссылки
1. [Как pod в Kubernetes получает IP-адрес](https://habr.com/ru/company/flant/blog/521406/)
2. [CoreDNS — DNS-сервер для мира cloud native и Service Discovery для Kubernetes](https://habr.com/ru/company/flant/blog/331872/)