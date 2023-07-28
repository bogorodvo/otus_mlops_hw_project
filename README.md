# Otus MLOps HomeWork Project
Repository for the MLOps project on the OTUS training program.

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
