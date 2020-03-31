from lxml import html
import requests


def get_shortcuts(tree):
    pass


def main():
    url = 'https://arxiv.org/'
    page = requests.get(url)
    header_found = False
    tree = html.fromstring(page.content)
    content = tree.get_element_by_id('content')
    shortcuts = {}
    for elem in content:
        if elem.tag == 'ul':
            subject_dict = {}
            for list_elem in elem:
                first_elem = True
                second_elem = False
                for le in list_elem:
                    if 'new' == le.text or 'recent' == le.text or 'search' == le.text or None is le.text or 'detailed' in le.text:
                        continue
                    if first_elem:
                        subject = le.text
                        first_elem = False
                        second_elem = True
                    elif second_elem:
                        short_subject = le.text
                        subject_dict[subject] = short_subject
                        second_elem = False
                    else:
                        short = le.attrib['id']
                        subject_dict[le.text] = short
                        print('\t', le.text)
                shortcuts[subject] = subject_dict

    return shortcuts


if __name__ == '__main__':
    shortcuts = main()
    print(shortcuts)
