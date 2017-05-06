'''
Created on 28.04.2017

@author: andigenu
'''
from sklearn import datasets, svm, metrics
import matplotlib.pyplot as plt

digits = datasets.load_digits()
#create tuples (in this case pairs) of (image, label) as array through list(zip())
images_and_labels = list(zip(digits.images, digits.target))
for index, (image, label) in enumerate(images_and_labels[:4]):
    #organise subplots as 2x4 grid 
    plt.subplot(2, 4, index + 1)
    plt.axis('off')
    plt.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')
    plt.title('Training: %i' % label)
#plt.show()

n_samples = len(digits.images)
#print(digits.images.shape)
data = digits.images.reshape((n_samples, -1))
#print(data.shape)
        
#clf = svm.SVC(gamma=0.001, C=100.)
clf = svm.SVC(gamma=0.001)
#clf.fit(digits.data[:-1], digits.target[:-1])
clf.fit(data[:(n_samples/2)], digits.target[:(n_samples/2)])
#print(clf.predict(digits.data[-1:]))
expected = digits.target[(n_samples/2):]
predicted = clf.predict(data[(n_samples / 2):])

print("Classification report for classifier %s:\n%s\n"
      % (clf, metrics.classification_report(expected, predicted)))
print("Confusion matrix:\n%s" % metrics.confusion_matrix(expected, predicted))

images_and_predictions = list(zip(digits.images[n_samples / 2:], predicted))
for index, (image, prediction) in enumerate(images_and_predictions[:4]):
    plt.subplot(2, 4, index + 5)
    plt.axis('off')
    plt.imshow(image, cmap=plt.cm.gray_r, interpolation='nearest')
    plt.title('Prediction: %i' % prediction)

plt.show()
