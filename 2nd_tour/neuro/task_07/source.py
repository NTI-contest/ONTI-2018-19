from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline

models=[None,None,None]
 
models[0] = Pipeline([('scaler', MinMaxScaler()),   # 97.2%
              ('logreg', LogisticRegression(solver='newton-cg',
                                       random_state=0))])
models[1] = Pipeline([('scaler', MinMaxScaler()),   # 97.2%
                      ('estimator',KNeighborsClassifier())])
models[2] = RandomForestClassifier(criterion='entropy',
                                   random_state=0)  # 95.6%
