import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.svm import SVC

traindf = pd.read_csv('data\\train.csv')
testdf = pd.read_csv('data\\test.csv')
hz = 250  # частота оцифровки сигнала

# Функции для работы с ЭКГ
def getPeaks(ecg, thold=0.3):
	"""Вычисление индексов точек, соответствующих вершинам R-зубцов
	thold - пороговое значение сигнала выше которого будут искаться
	пики"""
	i = 0
	peaks = []
	while i < len(ecg) - 1:
    	if ecg[i] > 0.3 and ecg[i-1] < ecg[i] > ecg[i+1]:
        	peaks.append(i)
        	i += 100
    	else:
        	i += 1
	return np.array(peaks)


def getIntervals(ecg):
	"""Вычисление интервалов между R-зубцами"""
	peaks = getPeaks(ecg)
	intervals = np.zeros(len(peaks)-1)
	for i in range(len(intervals)):
    	intervals[i] = peaks[i+1] - peaks[i]
	return intervals


def getHR(ecg):
	"""Вычисление ЧСС по индексам пиков. Вычисляется по крайним
	пикам в подаваемом в качестве аргумента сигнале"""
	peaks = getPeaks(ecg)
	hr = 60/((peaks[-1] - peaks[1])/hz/(len(peaks)-1))
	return hr


# Функции для работы с КГР
def getDerivative(vector):
	"""Вычисляет производную сигнала"""
	return vector[1:]-vector[:-1]


def stabilize(vector, begin, end):
	"""Убирает наклон графика КГР"""
	vector[end+1:] -= vector[end]-vector[begin]
	vector[begin:end+1] -= np.linspace(0, vector[end]-vector[begin],
                                   	end-begin+1)


def integrate(vector, const=0, thold=None):
	"""Интегрирует сигнал. vector - массив производных некого сигнала,
	const - его начальное значение. Отсекает все производные, превышающие
	по модулю пороговое значение thold."""
	ans = np.zeros(len(vector)+1)
	ans[0] = const
	if thold is not None:
    	absVec = np.abs(vector)
    	if absVec[0] > thold:
        	vector[0] = 0.0
    	for i in range(1, len(vector)):
        	if absVec[i] > thold:
            	vector[i] = vector[i-1]
	for i, der in enumerate(vector):
    	ans[i+1] = ans[i] + der
	return ans


def getLocalMaxsGSR(gsr):
	"""Возвращает индексы локальных максимумов сигнала КГР"""
	der = getDerivative(gsr)
	i = 10
	maxs = []
	while i < len(der) - 10:
    	if der[i-10] < der[i] > der[i+10] and der[i]-der[i+10] > 1e-12\
                                      	and der[i]-der[i-10] > 1e-12:
        	maxs.append(i)
        	i += 249
    	i += 1
	maxs = np.array(maxs)
	return maxs


def getClosestInterval(index, intervalsDict):
	"""Возвращает ближайший к index временной интервал между
	локальными максимумами производной сигнала КГР"""
	closestIndex = min(intervalsDict.keys(), key=lambda x: abs(x-index))
	return intervalsDict[closestIndex]


def processTestGSR(df):
	"""Обрабатывает GSR из тестовых данных: фильтрует производные,
	сглаживает выборосы"""
	der1 = getDerivative(df.gsr.values)
	der2 = getDerivative(der1)
	der1 = integrate(der2, thold=0.00000025)
	testGSR = integrate(der1, df.gsr.values[0])
	maxs = getLocalMaxsGSR(testGSR)
	der = getDerivative(maxs)
	for i in range(70, 200):
    	if der[i] < 11000:
        	der[i] = der[i-1]
	for i in range(250, len(der)):
    	if der[i] < 10000:
        	der[i] = der[i-1]
	intervalsDict = dict(zip(maxs[1:], der))
	return intervalsDict


def processTrainGSR(df):
	"""Обрабатывает GSR из обучающих данных: фильтрует производные,
	сглаживает выборосы"""
	der1 = getDerivative(df.gsr.values)
	der2 = getDerivative(der1)
	der1 = integrate(der2, thold=0.00000025)
	trainGSR = integrate(der1, df.gsr.values[0])
	stabilize(trainGSR, 1820500, len(trainGSR)-1)
	maxs = getLocalMaxsGSR(trainGSR)
	der = getDerivative(maxs)
	for i in range(120, 200):
    	if der[i] < 4000:
        	der[i] = der[i-1]
	for i in range(420, 450):
    	if der[i] < 4000:
        	der[i] = der[i-1]
	for i in range(470, 500):
    	if der[i] < 6000:
        	der[i] = der[i-1]
	for i in range(500, 700):
    	if der[i] < 6000:
        	der[i] = der[i-1]
	intervalsDict = dict(zip(maxs[1:], der))
	return intervalsDict


# Обработка ЭЭГ


def compl(sig, coef=0.95):
	"""Комплементарный фильтр с коэффициентом coef.
	Возвращает сигнал после фильтрации."""
	for i in range(1, len(sig)):
    	sig[i] = coef * sig[i-1] + (1-coef) * sig[i]
	return sig


def med(sig, coef=15):
	"""Возвращает массив длины len(sig)//coef, содержащий
	медианный значения отрезков sig длиной coef."""
	ret = np.zeros(len(sig)//coef)
	for i in range(len(ret)):
    	ret[i] = np.average(sig[i*coef:(i+1)*coef])
	return ret


def getAlBeta(eeg, chunkSize=15*hz):
	"""Вычисляет уровни альфа- и бета-ритмов в сигнале.
	Вычисляется для chunkSize числа точек."""
	nChunks = eeg.shape[0]//chunkSize
	alphas = np.zeros(nChunks)
	betas = np.zeros(nChunks)
	coef = chunkSize // hz
	for i in range(nChunks):
    	chunk = eeg[i*chunkSize:(i+1)*chunkSize]
    	spec = np.fft.fft(chunk)
    	spec = np.abs(spec)
    	alphas[i] = sum(spec[8*coef:13*coef+1])
    	betas[i] = sum(spec[15*coef:30*coef+1])
	return pd.DataFrame({'alpha': alphas,
                     	'beta': betas
                     	})


def getAlphaToBetaSmooth(eeg, coef=15):
	"""Вычисляет отношение альфа-ритма к бета- в сигнале ЭЭГ.
	После получение уровней альфа- и бета-ритмов сглаживает их.
	Изначально уровни вычисляются во временном окне равном 1 с.
	Параметр coef определяет число последовательных значений
	уровней, по которым считается медианное значение."""
	new = getAlBeta(eeg, chunkSize=hz)
	alpha = new.alpha.values
	beta = new.beta.values
	alpha = compl(alpha)
	beta = compl(beta)
	alpha = med(alpha, coef)
	beta = med(beta, coef)
	alpha = compl(alpha)
	beta = compl(beta)
	alphaToBeta = compl(alpha/beta)
	return alphaToBeta


def getFeatures(df, chunkSize=15*hz, gsrProcess=processTrainGSR):
	"""Генерируем вектор признаков для массива данных с датчиков."""
	# Вычисляем ЧСС
	hrs = np.zeros(df.shape[0] // chunkSize)
	# Вычисляем параметры КГР
	intervalsGSR = np.zeros(df.shape[0] // chunkSize)
	GSRDict = gsrProcess(df)
	for i in range(len(hrs)):
    	hrs[i] = getHR(df.ecg[i*chunkSize:(i+1)*chunkSize].values)
    	intervalsGSR[i] = getClosestInterval(i*chunkSize, GSRDict)
	# Вычисляем соотношение альфа- к бета-
	alphaToBeta = getAlphaToBetaSmooth(df.eeg.values)
	return pd.DataFrame({'HR': hrs,
                     	'GSRInterval': intervalsGSR,
                     	'albeta': alphaToBeta})

# Записываем вычисленные для обучающих данных признаки в X_train,
# верные для обучающих данных ответы в y_train, а вычисленные для
# тестовых данных признаки - в X_test
X_train = getFeatures(traindf, gsrProcess=processTrainGSR)
y_train = traindf.target[::15*hz].values
X_test = getFeatures(testdf, gsrProcess=processTestGSR)

# Обучаем модель на данных из train.csv и предсказываем значения
# из столбца target для test.csv. Полученные результаты записываем
# в myAnswer.csv, которые можно загрузить на kaggle.com в качестве
# ответа
svc = SVC(C=10, kernel='linear').fit(X_train, y_train)
answerDF = pd.DataFrame({'ID': testdf.ID.values[::15*hz],
                     	'target': svc.predict(X_test)
                    	})
answerDF.to_csv('myAnswer.csv', index=False)
