import numpy as np
# from sklearn.svm import SVC

from csxdata import roots
from csxdata.utilities.parsers import parse_csv


def pull_fruits_data(fruit):
    X, Y, head = parse_csv(roots["csvs"] + "kozma.csv", indeps=4, filterby="Species", selection=fruit)
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


def get_sample_xs_rasberries(average=True):
    d = {
     "15070049": ("Malna",
                  (105.13,), (-16.44,)),
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
    # theta = np.arctan2(*vecs[:, 0][::-1])
    theta = np.arctan(vecs[0, 1])

    return a, b, theta


def rotate(vec, theta, ccv=True):
    transformation = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta), np.cos(theta)]])
    if not ccv:
        transformation[(0, 1), (1, 0)] *= -1
    return vec @ transformation


def intersect(ellipse, vector, right=True):
    a, b = ellipse
    e, f = vector
    m = f / e
    coef = (a * b) / np.sqrt(a**2 * m**2 + b**2)
    isct = np.array([coef, coef * m])
    if right:
        return isct
    return -isct


def display(xycov1, xycov2, p1, p2, species, smplnm, smpl=None, skiprot=False,
            ellipse_sigma=2, dump=True):
    from matplotlib import pyplot as plt
    from matplotlib.patches import Ellipse

    def toellipse(params):
        a, b, theta = ellipse_params(params[-1], ellipse_sigma=ellipse_sigma)
        if skiprot:
            theta = 0.
        xy = params[:2]
        return Ellipse(xy, a * 2, b * 2, theta)

    ax = plt.gca()

    ell1, ell2 = toellipse(xycov1), toellipse(xycov2)
    ell1.set_facecolor("none")
    ell2.set_facecolor("none")
    ax.add_artist(ell1)
    ax.add_artist(ell2)
    ax.plot([xycov1[0], xycov2[0]], [xycov1[1], xycov2[1]],
            color="blue")
    ax.plot(*p1, marker="o", color="green")
    ax.plot(*p2, marker="o", color="blue")
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], linestyle="--", color="black")
    if smpl is not None:
        ax.plot(*smpl, marker="o", color="red")
    eps = 0
    ax.set_xlim([min(ell1.center[0]-ell1.width-eps, ell2.center[0]-ell2.width-eps),
                max(ell1.center[0]+ell1.width+eps, ell2.center[0]+ell2.width+eps)])
    ax.set_ylim([min(ell1.center[1]-ell1.height-eps, ell2.center[1]-ell2.height-eps),
                max(ell1.center[1]+ell1.height+eps, ell2.center[1]+ell2.height+eps)])
    ax.set_xlabel("$D/H_I$")
    ax.set_ylabel(r"$\delta^{13}C$")

    plt.title("{} ({}) vs. Kukorica".format(smplnm, species), y=1.05)
    if dump:
        plt.savefig("D:/tmp/alkpics/{}.png".format(smplnm), bbox_inches="tight")
    plt.close()


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

    def euclidean(sample, reference):
        return np.sqrt((sample - reference)**2).sum()

    maize_center = maize_parameters()[0]
    samples = get_sample_xs()
    for smplnm in sorted(samples):
        species, dh1, d13c = samples[smplnm]
        fruit_center = pull_fruits_data(species).mean(axis=0) + 0.6

        s = np.array([dh1, d13c]) - 0.6

        d1 = euclidean(s, fruit_center)
        d2 = euclidean(s, maize_center)

        print("{} ({}) maize content: {:>.4%}".format(smplnm, species, (d1 / (d1+d2))))


def xperiment_mahalanobis_distance():

    def mahal(p1, m2, cov2):
        dif = p1 - m2
        icov = np.linalg.inv(cov2)
        a = dif.dot(icov)
        b = a.dot(dif.T)
        c = np.sqrt(b)
        return c

    mmean, mcov = maize_parameters()
    samples = get_sample_xs()
    for smplnm in sorted(samples):
        species, dh1, d13c = samples[smplnm]
        fruit_data = pull_fruits_data(species)
        fmean = fruit_data.mean(axis=0) + 0.6
        fcov = np.cov(fruit_data.T)

        s = np.array([dh1, d13c]) - 0.6

        d1 = mahal(s, fmean, fcov)
        d2 = mahal(s, mmean, mcov)

        print("{} ({}) maize content: {:>.4%}".format(smplnm, species, (d1 / (d1+d2))))


def xperiment_codename_tunneling():
    maize_param = maize_parameters()
    maize_means, maize_sdevs = maize_param[0], np.sqrt(np.diagonal(maize_param[1]))
    samples = get_sample_xs(average=True)
    norm = np.linalg.norm
    for smplnm in sorted(samples):
        species, dh1, d13c = samples[smplnm]
        fruit = pull_fruits_data(species)
        fruit_means = fruit.mean(axis=0) + 0.6
        line = maize_means - fruit_means
        sample = np.array([dh1, d13c]) - 0.6
        sample -= fruit_means
        enum = sample @ line
        denom = norm(line)
        proj = enum / denom
        print("{} ({}) maize content: {:>.2%}".format(smplnm, species, proj / norm(line)))


def xperiment_codename_tunneling2():
    mmean, mcov = maize_parameters()
    mellipse = ellipse_params(mcov)
    samples = get_sample_xs(True)
    norm = np.linalg.norm
    for smplnm in sorted(samples):
        species, dh1, d13c = samples[smplnm]
        fruit = pull_fruits_data(species)
        fmean = fruit.mean(axis=0) + np.array([0.6, 0.6])
        fcov = np.cov(fruit.T)
        fellipse = ellipse_params(fcov)
        v = mmean - fmean
        mv = rotate(v, mellipse[-1], ccv=False)
        fv = rotate(v, fellipse[-1], ccv=False)
        mellipse_right = float(mmean[0]) > float(fmean[0])
        pre_mp = intersect(mellipse[:2], mv, right=(not mellipse_right))
        pre_fp = intersect(fellipse[:2], fv, right=mellipse_right)
        mp = mmean + rotate(pre_mp, mellipse[-1])
        fp = fmean + rotate(pre_fp, fellipse[-1])
        line = mp - fp
        pre_sample = np.array([dh1, d13c]) - 0.6
        sample = pre_sample - fp
        enum = sample @ line
        denom = norm(line)
        proj = enum / denom
        print("{} ({}) maize content: {:>.2%}".format(smplnm, species, proj / norm(line)))
        display((mmean[0], mmean[1], mcov),
                (fmean[0], fmean[1], fcov),
                mp, fp, species, smplnm, smpl=pre_sample,
                dump=True)


if __name__ == '__main__':
    print("Euklideszi távolság")
    print("-------------------")
    xperiment_euclidean_distance()
    print("\nMahalanobis távolság")
    print("--------------------")
    xperiment_mahalanobis_distance()
    print("\nGeometriai, átlagokból")
    print("----------------------")
    xperiment_codename_tunneling()
    print("\nGeometriai, 95% interszekciótól")
    print("-------------------------------")
    xperiment_codename_tunneling2()
