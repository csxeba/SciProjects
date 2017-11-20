from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA, QuadraticDiscriminantAnalysis as QDA
from sklearn.naive_bayes import GaussianNB as GNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier as KNN
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier

from csxdata.utilities.vectorop import separate_validation
from csxdata.stats.inspection import category_frequencies
from csxdata.visual.confusion import plot_confmatrix

from SciProjects.fruits.fruitframe import FruitData
from SciProjects.fruits import projectroot


df = FruitData(transform=True)
X = df.volatile.as_matrix()
X -= X.mean(axis=0)
X /= X.std(axis=0)
y = df["GYUM"].as_matrix()

category_frequencies(y)


def resplit_data(split=0.1):
    return separate_validation(split, X, y, balanced=True, nowarning=False)


def get_model(name):
    return {
        "lda": LDA(), "qda": QDA(), "gnb": GNB(), "knn": KNN(),
        "forest": RandomForestClassifier(),
        "svm": SVC(kernel="linear", class_weight="balanced"),
        "rbf svm": SVC(kernel="rbf", class_weight="balanced"),
        "poly svm": SVC(kernel="poly", degree=3, class_weight="balanced"),
        "mlp": MLPClassifier(learning_rate_init=0.1)
    }[name]


def xperiment(modelname, repeat=100):
    lX, lY, tX, tY = resplit_data()
    model = get_model(modelname)
    model.fit(lX, lY)
    acc = plot_confmatrix(tX, tY, model, title=f"{modelname.upper()} confusion matrix")


if __name__ == '__main__':
    for mn in ("lda", "qda", "gnb", "knn", "forest", "svm", "rbf svm", "poly svm", "mlp"):
        xperiment(mn, repeat=1)
