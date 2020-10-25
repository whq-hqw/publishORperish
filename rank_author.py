import os
import glob
import argparse
import pandas
import numpy as np


def parse_arguments():
    parser = argparse.ArgumentParser(description='Configuration for Pop Couning')
    parser.add_argument("--root", type=str, default="",
                        help="root folder of where you store you csv files exported "
                             "from Publish or Perish")
    parser.add_argument("--names", type=str, required=True,
                        help="The name of csv file exported from Publish or Perish")
    parser.add_argument("--rank_by", type=str, default="citation",
                        choices=["citation", "paper", "position"],
                        help="rank by total citation number, published paper number "
                             "or by author position.")
    parser.add_argument("--topk", type=int, default=5)
    args = parser.parse_args()
    return args


def rank_authors(args):
    rank2score = {
        1: 10,
        2: 8,
        3: 6,
        4: 4,
        5: 3,
        6: 2,
        7: 1,
        8: 0,
    }
    if args.root:
        root_folder = os.path.expanduser(args.root)
    else:
        root_folder = "./citation_csv"
    all_titles, all_citations, all_authors = [], [], []
    for csv_file in glob.glob(os.path.join(root_folder, "*.csv")):
        csv_name = csv_file.split("/")[-1][:-4]
        if args.names != csv_name:
            continue
        data = pandas.read_csv(csv_file, header=None)
        all_citations += data[0].tolist()[1:]
        all_authors += data[1].tolist()[1:]
        all_titles += data[2].tolist()[1:]

    author_data = {}
    for i, authors_list in enumerate(all_authors):
        author_list = authors_list.strip("…").split(", ")
        for rank, name in enumerate(author_list):
            if name in author_data:
                author_data[name][0].append(rank + 1)
                author_data[name][1].append((all_titles[i], all_citations[i]))
            else:
                author_data.update({name: ([rank + 1], [(all_titles[i], all_citations[i])])})
    paper_num_candidate = []
    author_candidate = []
    rank_candidate = []
    citation_candidate = []
    paper_candidate = []

    for author, achievement in author_data.items():
        paper_num = len(achievement[1])
        if paper_num < 5:
            continue
        paper_num_candidate.append(paper_num)
        author_candidate.append(author)
        rank_candidate.append(sum([rank2score[r] for r in achievement[0]]) / paper_num)
        citation_candidate.append(sum([int(t[1]) for t in achievement[1]]))
        top3_paper_idx = np.array([int(t[1]) for t in achievement[1]]).argsort()[-3:][::-1]
        paper_candidate.append([(achievement[1][idx][0], achievement[1][idx][1])
                                for idx in top3_paper_idx])

    if args.rank_by == "citation":
        top_k_idx = np.array(citation_candidate).argsort()[-args.topk:][::-1]
    elif args.rank_by == "paper":
        top_k_idx = np.array(paper_num_candidate).argsort()[-args.topk:][::-1]
    elif args.rank_by == "position":
        top_k_idx = np.array(rank_candidate).argsort()[-args.topk:][::-1]
    else:
        raise NotImplementedError()

    for idx in top_k_idx:
        author = author_candidate[idx]
        paper_num = paper_num_candidate[idx]
        represent_paper = paper_candidate[idx]
        citation = citation_candidate[idx]
        rank = rank_candidate[idx]

        text_1 = "%s, Paper num: %d" % (author, paper_num)
        text_2 = "Total Citation: %d" % citation
        text_3 = "Author Position Rank: %.2f" % rank

        max_len = max([len(text_1), len(text_2), len(text_3)]) + 1
        print("--%s--" % ("".join(["-"] * max_len)))
        print("| %s %s |" % (text_1, "".join([" "] * (max_len - len(text_1) - 1))))
        print("| %s %s |" % (text_2, "".join([" "] * (max_len - len(text_2) - 1))))
        print("| %s %s |" % (text_3, "".join([" "] * (max_len - len(text_3) - 1))))
        print("--%s--" % ("".join(["-"] * max_len)))
        for paper, cite_num in represent_paper:
            print("%s, citation: %s" % (paper, cite_num))
        print("")


if __name__ == '__main__':
    args = parse_arguments()
    rank_authors(args)
