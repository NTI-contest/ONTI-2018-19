from sklearn.svm import SVC
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
import numpy as np

data = np.loadtxt('ML.txt')
X,y = data[:,:-1],data[:,-1]
model = Pipeline([('scaler', MinMaxScaler()),
                  ('svm', SVC())])
param_grid = [
  {'svm__C': [1, 10, 100, 1000],
   'svm__kernel': ['linear']},
  {'svm__C': [1, 10, 100, 1000],
   'svm__gamma': [0.001, 0.0001],
   'svm__kernel': ['rbf']},
 ]
clf = GridSearchCV(model, param_grid, cv=10)
clf.fit(X, y)
print(clf.best_params_)
