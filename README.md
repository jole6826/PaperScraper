# PaperScraper  

---


Recently the trend of pre-print servers has developed as a way to share research results quickly. Pages like [arXiv.org](https://arxiv.org) offer a wide variety of subjects and fields to roam. 

Most researchers or students do not have the time to look through every possible page to keep up-to-date. This is why I started developing this tool. The goal is to have a simple, automated way of keeping track of new papers (pre-prints) of a field one might be interested in.

There is a bunch of similar projects out there ([Daily arXiv](http://dailyarxiv.com/), [ArXiv Sanity Preserver](http://www.arxiv-sanity.com/)) helping you to search paper. 

My tool on the other hand is supposed to automate the process of finding papers that might be interesting and saving the time of going online and actively searching. I see it as an addition to the above tools, not a replacement. 

* [Installation](#install)
* [Getting Started](#getStarted)
  * [Basic Usage](#basic)
  * [Subject-field combination](#subjectField)
  * [Multiple keywords and modes](#keywords)
  * [Custom output path](#outputPath)
  * [Automating and custom name](#name)
  * [Downloading PDFs](#download)
  * [Regular Expressions](#regex)

<a id='install'></a>
### Installation 

---

**PaperScraper** uses Python's standard library. The only other packages needed are [Pandas](https://pandas.pydata.org/) and [lxml](https://lxml.de/). Both  packages can be installed using [Anaconda](https://www.anaconda.com/) like 

```bash
conda install pandas lxml
```

When installed simply clone the repo and get started. 

```bash
git clone https://github.com/jole6826/PaperScraper.git
```

<a id='getStarted'></a>
### Getting started

---

PaperScraper is a command line tool (for now) that searches the latest papers in a given field for keywords. 

Run `python main.py --help` for details.

The publications on [arXiv.org](https://arxiv.org) is sorted by subject (e.g. maths, computer science, ...) and fields within a subject (e.g. probability, artificial intelligence, ...). Check [Subjects and Fields](SubjectsAndFields.md) for the entire list (including the shorthands in the URLs).

By default each of the follwing commands will create `/data/reports_{year}_{week}` in the `/PaperScraper/` folder. It uses the current year and week as the script only searches the last week's papers.

Within the reports folder you can find the output HTML file `arxiv_{subject}_{field}_{year}_{week}.html` that contains a table with the **title** as well as links to the **abstract** and **PDF**.

<a id='basic'></a>
#### Basic usage

---

FInd all papers in a subject containing a keyword.

```bash
# Subject: Computer Science
python main.py --subject cs --keywords intelligence
# or short 
python main.py -s cs -k intelligence
```

<a id='subjectField'></a>
#### Subject-field combination

---

Find all papers in a field of a subject containing a keyword.


```bash
# Subject: Computer Science, field: AI
python main.py --subject cs --field ai --keywords intelligence 
# or short 
python main.py -s cs -f ai -k intelligence
```

<a id='keywords'></a>
#### Multiple keywords and modes

---

It is also possible to give multiple keywords. 

The mode defines the way papers are selected:
* **any**: (default) Select if **one** of the keywords is found in the title. This is similar to a logical **OR**.
* **all**: Select if **all** of the keywords are found in the title. This is similar to a logical **AND**.

```bash
python main.py --subject cs --field ai --keywords deep learning  # using default mode=any
python main.py --subject cs --mode all --keywords deep learning  # using mode=all

# or short 

python main.py -s cs -f ai -k deep learning # using default mode=any
python main.py --s cs --m all --k deep learning  # using mode=all

```

<a id='outputPath'></a>
#### Custom output path

--- 

The output path can be adjusted to a custom directory using the `--output_path` or `-o` flag.

```bash
python main.py --subject cs --field ai --out_path /path/to/data --keywords deep learning  # using default mode=any

# or short 

python main.py -s cs -f ai -o /path/to/data -k deep learning # using default mode=any
```
<a id='name'></a>
#### Automating and custom name

--- 

On most platforms you can perform tasks at a regular interval. This script is best run once a week with a number of settings, to keep up-to-date on all your interests. 

In the case that you want to search the same subject/field combination for different keywords/modes, you can add a custom `name` to the output file with `--name custom_name`.

<a id='download'></a>
#### Downloading PDFs

--- 

Using the `--download` or `-d` flag it is possible to download the found papers right away. 
Papers are only downloaded if there is not already a file with the same name in the output directory.

**Be careful, this could cause a large number of papers to be downloaded at once.**

See [Robots](https://arxiv.org/help/robots) and [Bulk Download](https://arxiv.org/help/bulk_data)
for more information! 

The files will be stored in a subfolder of the output path similar to the reports folder.

<a id='regex'></a>
#### Regular Expressions 

---

Mode can also be **regex** in which case the keyword will be interpreted as a [Regular Expression](https://docs.python.org/3/howto/regex.html).

**Note:** If regular expression is used, there can only be **one** keyword, i.e. the regular expression.


