#!/home/mojo/anaconda3/bin/python
import argparse
import pandas as pd

from Scraper import ArxivScraper

pd.set_option('display.max_colwidth', -1)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', action="store", default='any',
                        choices=['any', 'all', 'regex'], type=str,
                        help='Searching mode to use.\n'
                             'any - True if any of the keywords is found in a title.\n'
                             'all - True if all the keywords are found in a title.\n'
                             'regex - True if regular expression is found.')
    parser.add_argument('-s', '--subject', action='store', default='cs', type=str,
                        help='Subject of the topic. Default: cs (Computer Science).'
                             'Other popular options: math, stat, econ, eess (Electical Engineering and Sys Science).'
                             'See https://arxiv.org for more.')
    parser.add_argument('-f', '--field', action='store', type=str,
                        help='Field within the subject.'
                             'See https://arxiv.org for more.')
    parser.add_argument('-o', '--out_path', action='store', default='./data', type=str,
                        help='Output path. Where to store the tables.')
    parser.add_argument('-d', '--download', help='Set downloading flag, this can lead to download of a '
                                                 'large number of papers!', action='store_true')
    parser.add_argument('-n', '--name', action='store', type=str,
                        help='Custom name for a filter, will be added to the file name for '
                             'different searches on the same subject/field combination.')
    parser.add_argument('-k', '--keywords', nargs='+',
                        help='Keywords to search in the title. Can be combined depending on mode. '
                             'Regular expressions can be used with mode="regex"', required=True)
    return parser.parse_args()


def main(args):
    scraper = ArxivScraper(args.subject, args.field, args.keywords, args.mode, args.name)
    scraper.scrape()
    scraper.save_html(args.out_path)
    if args.download:
        scraper.save_pdfs(args.out_path)


if __name__ == '__main__':
    args = parse_args()
    main(args)

