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