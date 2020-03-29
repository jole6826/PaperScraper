import datetime
import sys
import warnings

from lxml import html
import requests
import os
import re

import pandas as pd


class Scraper:

    my_date = datetime.date.today()
    year, week, day = my_date.isocalendar()

    def __init__(self, url, subject, field, keywords, mode, name=None):
        self.url = url
        self.subject = subject
        self.field = field
        self.keywords = keywords
        self.mode = mode
        self.data = []
        self.name = name
        self.prefix = None

    def scrape(self):
        raise NotImplementedError

    def save_html(self, out_path):
        if not len(self.data) == 0:
            path = os.path.join(out_path, f"reports_{self.year}_{self.week}")
            print(f'Creating output dir: \n\n\t{path}')
            os.makedirs(path, exist_ok=True)

            df = pd.DataFrame(self.data)
            if self.name:
                out_name = f"{self.prefix}_{self.subject}_{self.field}_{self.name}_{self.year}_{self.week}"
            else:
                out_name = f"{self.prefix}_{self.subject}_{self.field}_{self.year}_{self.week}"
            out_path = os.path.join(path, out_name)

            print(f"\nWriting table to: \n\n\t{out_path}.html")
            df.to_html(f'{out_path}.html', render_links=True, justify='center')
            print("\nDONE")
        else:
            print('\tNONE')

    def print_welcome_mssg(self, n_entries):
        print(f'\nWelcome to the arXiv paper scraper. \n\n'
              f'(c) Johann Lembach, 2020\n\n')
        print(f"Searching {n_entries} papers for:\n"
              f"\n\tSubject: {self.subject}\n"
              f"\tField: {self.field}\n"
              f"\tKeywords: {self.keywords}\n"
              f"\tMode: {self.mode} \n\n")


class ArxivScraper(Scraper):
    def __init__(self, subject, field, keywords, mode, name=None):
        super().__init__('https://arxiv.org', subject, field, keywords, mode, name)
        self.prefix = 'arxiv'

    def scrape(self):

        base_url = self.get_base_url()
        try:
            n_entries = self.get_number_of_entries(base_url)
            self.print_welcome_mssg(n_entries)
        except KeyError:
            warnings.warn(f'The page you requested ({base_url}) does not exist. Check the subject and field.')
            sys.exit(1)

        # Go to page containing all entries
        base_url = base_url + f"?show={n_entries}"
        print(f"\tURL: \n\n\t>>> {base_url} <<<\n")

        page = requests.get(base_url)
        tree = html.fromstring(page.content)
        self.data = self.get_info(tree)

    def get_base_url(self):
        if self.field:
            base_url = f"{self.url}/list/{self.subject}.{self.field}/pastweek"
        else:
            self.field = 'all'
            base_url = f"{self.url}/list/{self.subject}/pastweek"
        return base_url

    @staticmethod
    def get_number_of_entries(base_url):
        page = requests.get(base_url)
        tree = html.fromstring(page.content)
        n_entries_list = tree.get_element_by_id('dlpage')[3].text.split(' ')
        return int(n_entries_list[3])

    def get_info(self, tree):
        content = tree.get_element_by_id('content')[0]
        data = []
        print(f'Found: \n')
        for child in content:  # in the body
            if child.tag == 'dl':  # One for every day
                for entry in child:
                    if entry.tag == 'dt':  # temporarily store link to pdf if needed later
                        pdf_link = entry[1][1].attrib['href']
                        abs_link = entry[1][0].attrib['href']
                        pdf_link = self.url + pdf_link
                        abs_link = self.url + abs_link
                    if entry.tag == 'dd':  # This is now an entry element
                        title = entry[0][0][0].tail[1:-1]
                        title_to_search = title.lower()
                        if self.mode == 'any':
                            if any(keyword.lower() in title_to_search for keyword in self.keywords):
                                data.append({'title': title, 'pdf': pdf_link, 'abstract': abs_link})
                                print(f'\t* {title} \n\t\t({pdf_link})')
                        elif self.mode == 'all':
                            if all(keyword.lower() in title_to_search for keyword in self.keywords):
                                data.append({'title': title, 'pdf': pdf_link, 'abstract': abs_link})
                                print(f'\t* {title} \n\t\t({pdf_link})')
                        elif self.mode == 'regex':
                            assert len(self.keywords) is 1
                            if re.search(self.keywords[0], title_to_search):
                                data.append({'title': title, 'pdf': pdf_link, 'abstract': abs_link})
                                print(f'\t* {title} \n\t\t({pdf_link})')
                        else:
                            raise NotImplementedError
        return data

