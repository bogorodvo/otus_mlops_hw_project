# Otus MLOps HomeWork Project
Repository for the MLOps project on the OTUS training program.

# HW1

## Цели 
С целью минимизации финансовых и репутационных потерь организации требуется:

* В течение 3 месяцев разработать ML-алгоритм выявления мошеннических транзакций. 
Ошибка модели должна составить не более 2 мошеннических транзакций на 100 наблюдений.
* Подтвердить экономическую эффективность ML-алгоритма в результате проведения AB-тестов. 
Отток в результате применения модели должен составить менее 5%.
* В течение 6 месяцев разработать ML-систему для автоматизации процесса исполнения 
и переобучения ML-модели. Система должна уметь использовать 
пакетные данные для переобучения модели, работать с потоковыми данными и очередью сообщений, 
обрабатывать 50 сообщений в секунду, масштабироваться при высоких нагрузках для обработки до 
400 сообщений в секунду, обладать отказоустойчивостью.
* В течение 1-го месяца согласовать процесс получения и анонимизации данных, в течение 3 месяцев - 
политики безопасности и возможные риски разрабатываемой системы с представлителями безопасности заказчика.
* Затратить менее 10 млн. рублей на реализацию проекта, в том числе с учетом финансовых потерь в связи
с проведением AB-тестов. Для оценки затрат на инфраструктуру в течение 1-го месяца проекта требуется 
проработать архитектуру решения с учетом выбранного Cloud провайдера.

## Метрики

FP - ошибка I-го рода. Модель может предсказывать, что транзакция мошенническая, 
а на самом деле не мошенническая. Это может приводить к тому, что модель будет блокировать нормальные 
транзакции и понижать лояльность клиентов, повышать уровень оттока, снижать комиссионный доход.

FN - ошибка II-го рода. Модель может предсказывать, что транзакция не мошенническая, 
а на самом деле мошенническая. Это может приводить к тому, что мы будем пропускать мошеннические 
транзакции и нести репутационные потери, финансовые потери за счёт компенсации.

В данной задаче ошибка II-го рода может быть более критична. В то же время следует уметь управлять 
ошибкой I-го рода, так как потери, которые могут возникнуть в случае блокировки нормальных 
транзакций и оттока клиентов, могут превышать потери в связи с мошенническими транзакциями.

В случае сильно несбалансированных классов для оценки качества модели могут быть использованы
следующие метрики
[[Source]](https://fraud-detection-handbook.github.io/fraud-detection-handbook/Chapter_4_PerformanceMetrics/Assessment_RealWorldData.html)
:
* ROC AUC (Receiver Operating Characteristic AUC). 
Позволяет оценивать общее качество ранжирования.
* Average precision (Calculated based on Precision-Recall function). 
Позволяет оценивать Precision при заданных значения Recall.
* Card Precision@k (The share of daily detected frauded cards at top k bucket).
Позволяет оценивать Precision в баккете k размера. Учитываются заблокированные карты.

Мы можем ввести метрики для оценки финансовых потерь (могут быть чувствительны к выбросам):
* TPVR - True positive volume rate  = TPVolume / (FNVolume + TPVolume). Доля от объема мошеннических транзакций,
которую мы верно заблокировали. Учитывает ошибку II рода для оценки финансовых потерь, 
которую пропускает классификатор.
* PPVV - Positive predictive volume value = TPVolume / (FPVolume + TPVolume). Доля верно заблокированного объема 
транзакций. Учитывает ошибку I рода для оценки потерь комиссионного дохода.

Для оценнки оттока можем ввести метрику:
* CR - Churn Rate. Доля оттока. Клиенты которые не совершили транзакций в выбранный период, например 1 месяц.

## Canvas
![Project Canvas V1](https://github.com/bogorodvo/otus_mlops_hw_project/blob/main/project_content/MLOPs_Canvas_v1.png)

## Baseline Solution
Эффективный дизайн прототипа разрабатываемой антифрод системы рассмотрен в [[Source]](https://fraud-detection-handbook.github.io/fraud-detection-handbook/Chapter_3_GettingStarted/BaselineModeling.html). В дальнейшем возможна его проработка в результате проработки данных проекта и с учетом планиуремой инфраструктуры.
![Project Canvas V1](https://github.com/bogorodvo/otus_mlops_hw_project/blob/main/project_content/baseline_ML_workflow.png)

# HW2

## Загрузка данных в S3  

Данные из `s3://mlops-data/fraud-data/` скопираваны в
`s3://otus-mlops-bucket-bvo/fraud-data/` с помощью команды 
`s3cmd sync --acl-public s3://mlops-data/fraud-data/ s3://otus-mlops-bucket-bvo/fraud-data/`.

![S3 Bucket](https://github.com/bogorodvo/otus_mlops_hw_project/blob/main/project_content/HW2_1.png)

## Создание Data Proc кластера
a) Мастер-подкластер: класс хоста s3-c2-m8, размер хранилища 40 ГБ.

б) Data-подкластер: класс хоста s3-c4-m16, 3 хоста, размер хранилища 128 ГБ.

![Data Proc](https://github.com/bogorodvo/otus_mlops_hw_project/blob/main/project_content/HW2_2.png)

## Копирование данных из S3 в HDFS
Копирование данных из `s3` хранилища в `hdfs` осуществлено с помощью команды `hadoop distcp` с 2-ой репликацией
`hadoop distcp -D dfs.replication=2 s3a://otus-mlops-bucket-bvo/fraud-data/ hdfs:///user/ubuntu/`

![HDFS](https://github.com/bogorodvo/otus_mlops_hw_project/blob/main/project_content/HW2_3.png)

## Биллинг
Стоимость содержания созданного кластера 36.20 руб/час (36.2x24x365.25/12 ~ `26 444 руб/месяц`).

Содерджание мастер ноды обходится в 5.72 руб/час (5.72x24x365.25/12 ~ `4 178 руб/месяц`).

Содержание стандартного S3 хранилилища обходится в 2.01x210 ~ `241 руб/месяц`, при условии что у нас около 120 ГБ данных.
В стандартном S3 хранилилище также не тарифицируется первые 10 000 / 100 000 операций за месяц.

Исходящий/входяший трафик внутри VPC не тарифицируется.

## Пути оптимизации Spark кластера
1. Преобразование данных из .csv в .parquet или .orc с целью сжатия данных. 
2. Использование меньшего количества реплик (например 1 или 2).
3. Партиционирование данных (например по дате) с целью исключение ненужных данных для анализа
4. Создавать data ноды только на время выполнения требуемых рачетов.
5. В случае если данными пользуется мало пользователей и обращения к кластеру не регулярные, то к данным можно обращаться
напрямую в S3. В таком случае тарификация за операции в S3 может быть меньше тарификации использования
data-нод. Стандартный тип хранилища S3 может быть оптимальным вариантом.
6. C помощью Spark данные можно сжать и партиционировать, сохранив в новый s3 баккет. Также при сохранении можно указать размер
блоков (например 64/128 МБ) для реализации преумуществ работы Spark.

# HW3

## Настройка сети для работы со Spark Cluster

Для создания кластера из Master и Сompute нод с установленным Spark, который способен использовать Object Storage вместо HDFS, потребуется создание виртуальной сети по [[инструкции]](https://cloud.yandex.ru/docs/data-proc/tutorials/configure-network).

При создании Service Account сохранить `Access Key` и `Secret Key`. Ключи потребуются при настройке s3cmd. Роли: `mdb.dataproc.agent`; `storage.uploader`; `storage.viewer`.

При настройке Security Group указать:

![Security Group IN](https://github.com/bogorodvo/otus_mlops_hw_project/blob/main/project_content/HW3_3.png)

![Security Group Out](https://github.com/bogorodvo/otus_mlops_hw_project/blob/main/project_content/HW3_4.png)


## Создание Bucket в Object Storage

Предварительно нужно установить утилиту `s3cmd`
[[Инструкция]](https://cloud.yandex.ru/docs/storage/tools/s3cmd). Для настройки следует использовать ключи от `Service Account`.

Баккет для полученных данных (из HW2): `s3://otus-mlops-bucket-bvo/`

Баккет для обработанных данных: `s3://otus-mlops-bucket-bvo-processed/`

![Bucket](https://github.com/bogorodvo/otus_mlops_hw_project/blob/main/project_content/HW3_2.png)

## Создание Spark Cluster

Параметры Spark кластера (40.99 руб/час):

a) Мастер-подкластер: класс хоста s3-c2-m8, размер хранилища 40 ГБ.

б) Compute-подкластер: класс хоста s3-c4-m16, 3 хоста, размер хранилища 128 ГБ.

![Spark Cluster](https://github.com/bogorodvo/otus_mlops_hw_project/blob/main/project_content/HW3_5.png)

Для проверки Spark после создания кластра требутся зайти на мастер-ноду `ssh ubuntu@public_ip` и следовать [[инструкции]](https://cloud.yandex.ru/docs/data-proc/tutorials/run-spark-job?from=int-console-help-center-or-nav). Для работы с Objact Storage также потребуется настройка s3cmd на мастер-ноде.

После запуска Spark в баккете Objact Storage появятся новые папки.

![Bucket](https://github.com/bogorodvo/otus_mlops_hw_project/blob/main/project_content/HW3_6.png)


## Установка Jupyter Lab и доступ к данным

На мастер-ноду скачиваем  дистрибутив `wget 'https://repo.anaconda.com/archive/Anaconda3-2023.09-0-Linux-x86_64.sh'` и устанавливаем. Запускаем Jupyter `jupyter notebook --no-browser --port=8888 --ip=*` и вставляем ссылку в браузер `http://publicip:8888/?token=xxxx`.

Проверяем доступ к данным (пример в `notebook/HW3_InitialSparkReading.ipynb`).

![Initial Job](https://github.com/bogorodvo/otus_mlops_hw_project/blob/main/project_content/HW3_7.png)
