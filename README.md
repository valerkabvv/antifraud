## Проект Антифрод

### Структура проекта

* [aggregated_features.py](https://github.com/valerkabvv/antifraud/blob/master/aggregated_features.py)

  Содержит функции для вычисления статистик по транзакционным историям: среднее и 
  общее количество транзакций определенного типа для каждого клиента. 
  Далее для к признакам показывающим количество транзакций применяется TF-IDF.
  
* [time_features.py](https://github.com/valerkabvv/antifraud/blob/master/time_features.py)

  Содержит функции для вычисления временных статистик по транзакционным исторям.
  Считается среднее периодическое и переодическое среднеквадратичное отклонение.
  Также, функции для подсчета части попаданий в определенный временной интервал.
  Далее за эти интервалы берутся 80% доверительные интервалы для мошенников и обычных клиентов.
  
* [mcc2vec.py](https://github.com/valerkabvv/antifraud/blob/master/mcc2vec.py) 

  Функция для составления документов и предложений из mcc кодов где документ - пользователь,
  предложение - серия транзакций время между между которыми менее 12 часов. Далее на этом корпусе обучается
  doc2vec и возвращается таблица содержащая вектора для каждого пользователя.
  
* [Calculating_features.ipynb](https://github.com/valerkabvv/antifraud/blob/master/Calculate_features.ipynb)
  
  Расчитываются все признаки и сохраняются.
  
* [Preprocess_features.ipynb](https://github.com/valerkabvv/antifraud/blob/master/Preprocess_features.ipynb)

  Признаки склеиваются в одну таблицу, формируются данные для обучения, берется таргет, и сохраняется.
  
* [Learning.ipynb](https://github.com/valerkabvv/antifraud/blob/master/Learning.ipynb)

  Обучается модель, считаются метрики и строятся графики.
