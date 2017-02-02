import os

os.chdir("E:/PyCharm/SciProjects/txtanalyzer/")


def parsefl(flnm, label):
    article_number = 0
    article_body = ""
    article_bodies = []

    with open(flnm) as infl:
        try:
            lines = infl.read().split("\n")
        except UnicodeDecodeError:
            print("I died @", flnm)
            raise

    for line in lines:
        if line[:8] == "Article ":
            article_number += 1
            article_bodies.append(article_body)
            article_body = ""
            continue
        article_body += line + "\n"

    assert article_number == len(article_bodies)
    print("Found {} article bodies!".format(article_number))

    for i, ab in enumerate(article_bodies):
        with open("byartcl/{}_art_{:02d}.txt".format(label, i), "w") as outfl:
            outfl.write("ARTICLE {}\n----------\n".format(i) + ab)

parsefl("mrgd/prp.txt", "prp")
parsefl("mrgd/ori.txt", "ori")
