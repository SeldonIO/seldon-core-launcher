from sklearn.externals import joblib

class IrisClassifier(object):

    def __init__(self):
        self.model = joblib.load('IrisClassifier.sav')
        self.class_names = ["iris-setosa","iris-vericolor","iris-virginica"];

    def predict(self,X,features_names):
        return self.model.predict_proba(X)
