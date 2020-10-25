import os
import glob
import argparse
import pandas
import Levenshtein


def parse_arguments():
    parser = argparse.ArgumentParser(description='Configuration for Pop Couning')
    parser.add_argument("--root", type=str, default="",
                        help="root folder of where you store you csv files exported "
                             "from Publish or Perish")
    parser.add_argument("--names", nargs='+',
                        help="A list of name of csv files exported from Publish or Perish")
    parser.add_argument("--leven_thres", type=int, default=5,
                        help="Levenshtein distance threhold for 2 paper")
    args = parser.parse_args()
    return args


def find_common_citations(args):
    assert len(args.names) >= 2
    if args.root:
        root_folder = os.path.expanduser(args.root)
    else:
        root_folder = "./citation_csv"
    all_titles, all_citations = [], []
    for csv_file in glob.glob(os.path.join(root_folder, "*.csv")):
        csv_name = csv_file.split("/")[-1]
        if not any([name == csv_name for name in args.names]):
            continue
        data = pandas.read_csv(csv_file, header=None)
        all_titles.append(data[2].tolist()[1:])
        all_citations.append(data[0].tolist()[1:])

    common = {}
    for i in range(len(all_titles) - 1):
        title_list_1, title_list_2 = all_titles[i], all_titles[i+1]
        num_cite_1, num_cite_2 = all_citations[i], all_citations[i+1]
        for i_t1, title_1 in enumerate(title_list_1):
            for i_t2, title_2 in enumerate(title_list_2):
                dist = Levenshtein.distance(title_1, title_2)
                if dist < args.leven_thres:
                    if dist > 0:
                        print("Levenshtein distance: %d\n%s\n==> %s\n" % (dist, title_1, title_2))
                    if title_1 in common:
                        common[title_1] = max(common[title_1], num_cite_1[i_t1])
                    else:
                        common.update({title_1: num_cite_1[i_t1]})
    if len(common.keys()) == 0:
        print("No common citation between: %s" % ", ".join(args.names))

    common_citations, common_num_cite = [], []
    for _title, _num_citation in common.items():
        common_citations.append(_title)
        common_num_cite.append(int(_num_citation))

    sorted_paper = [(_, x) for _, x in sorted(zip(common_num_cite, common_citations))]
    for num_cite, paper_title in sorted_paper:
        print("%s: %s" % (num_cite, paper_title))
    print("Common citation between: %s is %s" % (", ".join(args.names), len(sorted_paper)))


if __name__ == '__main__':
    args = parse_arguments()
    find_common_citations(args)
