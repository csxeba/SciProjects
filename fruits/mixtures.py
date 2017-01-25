import numpy as np

from scipy.stats.stats import ttest_1samp

from sklearn.svm import SVC
from sklearn.decomposition import PCA

from csxdata.utilities.parsers import parse_csv

from SciProjects.fruits import gyumpath


def pull_fruits_data(fruit):
    X, Y, head = parse_csv(gyumpath, indeps=4, filterby="Species", selection=fruit)
    return X[:, (0, 2)]


def maize_parameters():
    means = np.array([110.8, -10.3])
    covar = np.array([
        [2.81, -0.17],
        [-0.17, 0.67]])
    return means, covar


def fake_maize_data(N=100):
    means, covar = maize_parameters()
    return np.random.multivariate_normal(means, covar, size=(N,))


def get_sample_xs(average=True):
    d = {
     "4473": ("Cseresznye",
              (105.21, 104.53), (-19.46, -19.60)),
     "4472": ("Kajszi",
              (105.07, 103.80, 105.24), (-18.99, -19.15, -19.02)),
     "4471": ("Szilva",
              (106.37, 106.30), (-17.35, -17.44)),
     "44A6": ("Szilva",
              (101.20, 101.59), (-23.09, -22.47)),
     "TM50": ("Meggy",
              (104.74,), (-20.05,)),
     "TS50": ("Szilva",
              (104.385,), (-18.33,)),
     "TA70": ("Alma",
              (105.23,), (-17.64,)),
     "TA50": ("Alma",
              (103.28,), (-20.06,)),
     "TA30": ("Alma",
              (101.36,), (-23.31,))
    }
    if average:
        return {smpname: (spec, np.mean(dh1), np.mean(d13c))
                for smpname, (spec, dh1, d13c) in
                sorted(d.items(), key=lambda t: t[0])}
    else:
        return d


def ellipse_params(cov, ellipse_sigma=2):
    vals, vecs = np.linalg.eig(cov)

    a = np.sqrt(vals[0]) * ellipse_sigma * 2
    b = np.sqrt(vals[1]) * ellipse_sigma * 2
    theta = np.arctan2(*vecs[:, 0][::-1])

    return a, b, theta


def rotate(vec, theta, ccv=True):
    transformation = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta), np.cos(theta)]])
    if not ccv:
        transformation[1, 0] *= -1
    return vec.dot(transformation)


def intersect(ellipse, vector, right=True):
    a, b = ellipse
    e, f = vector
    coef = (a * b) / np.sqrt((a**2 * f**2) + (b**2 * e**2))
    isct = np.array([coef * e, coef * f])
    if right:
        return isct
    return -isct


def xperiment_twoclass_svm():
    print("SMPL     PROB      PROB     PREDICTION")
    print("--------------------------------------")
    maize = fake_maize_data()
    samples = get_sample_xs()
    for i, smplnm in enumerate(sorted(samples)):
        species, dh1, d13c = samples[smplnm]
        fruit = pull_fruits_data(species)

        X = np.concatenate((fruit, maize))
        Y = np.array([species]*len(fruit) + ["Kukorica"]*len(maize))

        svm = SVC(kernel="linear", probability=True)
        svm.fit(X, Y)

        sX = np.array([[dh1, d13c]])
        probs = svm.predict_proba(sX).ravel()
        pred = svm.predict(sX).ravel()
        print("{}    {:.2%}    {:.2%}    {:>10}".format(smplnm, probs[0], probs[1], pred[0]))


def xperiment_euclidean_distance():
    maize_center = maize_parameters()[0]
    samples = get_sample_xs()
    for smplnm in sorted(samples):
        species, dh1, d13c = samples[smplnm]
        fruit_center = pull_fruits_data(species).mean(axis=0)

        s = np.array([dh1, d13c])

        d1 = np.sqrt((fruit_center - s)**2).sum()
        d2 = np.sqrt((maize_center - s)**2).sum()

        print("{} ({}) maize content: {:>.4%}".format(smplnm, species, (d1 / (d1+d2))))


def xperiment_codename_tunneling():
    maize_param = maize_parameters()
    maize_means, maize_sdevs = maize_param[0], np.sqrt(np.diagonal(maize_param[1]))
    samples = get_sample_xs(average=True)
    norm = np.linalg.norm
    for smplnm in sorted(samples):
        species, dh1, d13c = samples[smplnm]
        fruit = pull_fruits_data(species)
        fruit_means = fruit.mean(axis=0)
        line = maize_means - fruit_means
        sample = np.array([dh1, d13c]) - fruit_means
        enum = sample @ line
        denom = norm(line)
        proj = enum / denom
        print("{} ({}) maize content: {:>.2%}".format(smplnm, species, proj / norm(line)))


def xperiment_codename_tunneling2():

    def display(e1xycov, e2xycov, p1, p2, skiprot=False):
        from matplotlib import pyplot as plt
        from matplotlib.patches import Ellipse
        ax = plt.gca()
        eigvals1, eigvecs1 = np.linalg.eig(e1xycov[-1])
        eigvals2, eigvecs2 = np.linalg.eig(e2xycov[-1])
        (a1, b1), (a2, b2) = np.sqrt(eigvals1) * 4, np.sqrt(eigvals2) * 4
        if skiprot:
            theta1 = theta2 = 0.
        else:
            theta1 = np.degrees(np.arctan2(*eigvecs1[:, 0][::-1]))
            theta2 = np.degrees(np.arctan2(*eigvecs2[:, 0][::-1]))

        ell1 = Ellipse(e1xycov[:2], a1, b1, theta1)
        ell2 = Ellipse(e2xycov[:2], a2, b2, theta2)
        ell1.set_facecolor("none")
        ell2.set_facecolor("none")
        ax.add_artist(ell1)
        ax.add_artist(ell2)
        ax.plot([e1xycov[0], e2xycov[0]], [e1xycov[1], e2xycov[1]],
                color="red")
        ax.plot(*p1, marker="o", color="black")
        ax.plot(*p2, marker="o", color="black")

        plt.show()

    mmean, mcov = maize_parameters()
    mellipse = ellipse_params(mcov)
    samples = get_sample_xs(True)
    norm = np.linalg.norm
    for smplnm in sorted(samples):
        species, dh1, d13c = samples[smplnm]
        fruit = pull_fruits_data(species)
        fmean = fruit.mean(axis=0)
        fcov = np.cov(fruit.T)
        fellipse = ellipse_params(fcov)
        v = mmean - fmean
        mv = rotate(v, mellipse[-1], ccv=False)
        fv = rotate(v, fellipse[-1], ccv=False)
        mellipse_right = float(mmean[0]) > float(fmean[0])
        pre_mp = intersect(mellipse[:2], mv, right=mellipse_right)
        pre_fp = intersect(fellipse[:2], fv, right=(not mellipse_right))
        display([0, 0, mcov],
                [0, 0, fcov],
                pre_mp, pre_fp, skiprot=True)
        mp = mmean + rotate(pre_mp, mellipse[-1])
        fp = fmean + rotate(pre_fp, fellipse[-1])
        line = mp - fp
        sample = np.array([dh1, d13c]) - fmean
        enum = sample @ line
        denom = norm(line)
        proj = enum / denom
        print("{} ({}) maize content: {:>.2%}".format(smplnm, species, proj / norm(line)))
        display((mmean[0], mmean[1], mcov),
                (fmean[0], fmean[1], fcov),
                mp, fp)


if __name__ == '__main__':
    xperiment_codename_tunneling2()
