__author__ = 'yleonychev'

import numpy
import pickle
import datetime
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier


class Classifier(object):
    classifier = None
    update_dt = None

    def get_classifier(self):
        forest = pickle.loads(self.classifier)
        return forest

    def set_classifier(self, classifier):
        self.classifier = pickle.dumps(classifier)

    def save(self):
        pass

    def relearn(self):
        print('relearning classifier')
        train_data = []
        #features = ...
        #for item in features:
        #    item_hash = item.get_hash()
        #    features = item.get_features()
        #    if features:
        #        train_data.append([int(item.is_anomaly()), item_hash, ] + item.get_features())
        #train_data = numpy.array(train_data)  # first column should be the class, +3 for class, name, 0
        #forest = AdaBoostClassifier(base_estimator=RandomForestClassifier(n_estimators=100), n_estimators=100)
        #forest = forest.fit(train_data[0::, 2::], train_data[0::, 0])
        #self.set_classifier(forest)
        self.update_dt = datetime.datetime.now()
        self.save()

    def classify(self, data):
        if not self.classifier:
            self.relearn()
        forest = self.get_classifier()
        output = int(forest.predict(numpy.array(data)).astype(int)[0])
        print('CLASS: %s' % output)
        return output
