#!/home/mojo/anaconda3/bin/python
import argparse
import datetime
import os
import sys
import warnings

from lxml import html
import pandas as pd
import re
import requests

pd.set_option('display.max_colwidth', -1)

my_date = datetime.date.today()
year, week_num, day_of_week = my_date.isocalendar()


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
    parser.add_argument('-n', '--name', action='store', type=str,
                        help='Custom name for a filter, will be added to the file name for '
                             'different searches on the same subject/field combination.')
    parser.add_argument('-k', '--keywords', nargs='+',
                        help='Keywords to search in the title. Can be combined depending on mode. '
                             'Regular expressions can be used with mode="regex"', required=True)
    return parser.parse_args()


def save_ckpt(data, path, name, subject, field):
    path = os.path.join(path, f"reports_{year}_{week_num}")
    print(f'Creating output dir: \n\n\t{path}')
    os.makedirs(path, exist_ok=True)

    df = pd.DataFrame(data)
    if name:
        out_name = f"arxiv_{subject}_{field}_{name}_{year}_{week_num}"
    else:
        out_name = f"arxiv_{subject}_{field}_{year}_{week_num}"
    out_path = os.path.join(path, out_name)

    print(f"\nWriting table to: \n\n\t{out_path}.html")

    # df.to_csv(f'{out_path}.csv')
    # df.to_json(f'{out_path}.json')
    df.to_html(f'{out_path}.html', render_links=True, justify='center')


def get_number_of_entries(base_url):
    page = requests.get(base_url)
    tree = html.fromstring(page.content)
    n_entries_list = tree.get_element_by_id('dlpage')[3].text.split(' ')
    return int(n_entries_list[3])


def get_info_if_relevant(tree, keywords, search_mode):
    content = tree.get_element_by_id('content')[0]
    data = []
    print(f'Found: \n')
    for child in content:  # in the body
        if child.tag == 'dl':  # One for every day
            for entry in child:
                if entry.tag == 'dt':  # temporarily store link to pdf if needed later
                    pdf_link = entry[1][1].attrib['href']
                    abs_link = entry[1][0].attrib['href']
                    pdf_link = 'https://arxiv.org' + pdf_link
                    abs_link = 'https://arxiv.org' + abs_link
                if entry.tag == 'dd':  # This is now an entry element
                    title = entry[0][0][0].tail[1:-1]
                    title_to_search = title.lower()
                    if search_mode == 'any':
                        if any(keyword.lower() in title_to_search for keyword in keywords):
                            data.append({'title': title, 'pdf': pdf_link, 'abstract': abs_link})
                            print(f'\t* {title} \n\t\t({pdf_link})')
                    elif search_mode == 'all':
                        if all(keyword.lower() in title_to_search for keyword in keywords):
                            data.append({'title': title, 'pdf': pdf_link, 'abstract': abs_link})
                            print(f'\t* {title} \n\t\t({pdf_link})')
                    elif search_mode == 'regex':
                        assert len(keywords) is 1
                        if re.search(keywords[0], title_to_search):
                            data.append({'title': title, 'pdf': pdf_link, 'abstract': abs_link})
                            print(f'\t* {title} \n\t\t({pdf_link})')
                    else:
                        raise NotImplementedError

    return data


def main(args):
    subject = args.subject
    if args.field:
        field = args.field
        base_url = f"https://arxiv.org/list/{subject}.{field}/pastweek"
    else:
        field = 'all'
        base_url = f"https://arxiv.org/list/{subject}/pastweek"
    mode = args.mode
    kws = args.keywords
    path = args.out_path

    try:
        n_entries = get_number_of_entries(base_url)
    except KeyError:
        warnings.warn(f'The page you requested ({base_url}) does not exist. Check the subject and field.')
        sys.exit(1)

    # Go to page containing all entries
    base_url = base_url + f"?show={n_entries}"
    print(f'\nWelcome to the arXiv paper scraper. \n\n(c) Johann Lembach, 2020\n\n')
    print(f"Searching {n_entries} papers for:\n"
          f"\n\tSubject: {subject}\n\tField: {field}\n\tKeywords: {kws}\n\tMode: {mode} \n\n\tURL: \n\n\t>>> {base_url} <<<\n")
    page = requests.get(base_url)
    tree = html.fromstring(page.content)

    data = get_info_if_relevant(tree, keywords=kws, search_mode=mode)

    if not len(data) == 0:
        save_ckpt(data, path, args.name, subject, field)
    else:
        print('\tNone')

    print(f"\nDONE")


if __name__=='__main__':
    args = parse_args()

    main(args)

