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

---
## Ход работы и мои замечания

---
## Ошибки (в хронологическом порядке)

---
## Полезные ссылки
1. [Как pod в Kubernetes получает IP-адрес](https://habr.com/ru/company/flant/blog/521406/)