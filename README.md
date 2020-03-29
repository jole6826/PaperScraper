# PaperScraper  

---


Recently the trend of pre-print servers has developed as a way to share research results quickly. Pages like [arXiv.org](https://arxiv.org) offer a wide variety of subjects and fields to roam. 

Most researchers or students do not have the time to look through every possible page to keep up-to-date. This is why I started developing this tool. The goal is to have a simple, automated way of keeping track of new papers (pre-prints) of a field one might be interested in. 

### Installation 

---

**PaperScraper** uses Python's standard library. The only other packages needed are [Pandas](https://pandas.pydata.org/) and [lxml](https://lxml.de/). Both  packages can be installed using [Anaconda](https://www.anaconda.com/) like 

```bash
conda install pandas lxml
```

When available simply clone the repo and get started. 

```bash
git clone https://github.com/jole6826/PaperScraper.git
```

### Getting started

---

PaperScraper is a command line tool (for now) that searches the latest papers in a given field for keywords. 

Run `python main.py --help` for details.

The publications on [arXiv.org](https://arxiv.org) is sorted by subject (e.g. maths, computer science, ...) and fields within a subject (e.g. probability, artificial intelligence, ...). Check [arXiv.org](https://arxiv.org) for the entire list (including the shorthands in the URLs).

By default each of the follwing commands will create `/data/reports_{year}_{week}` in the `/PaperScraper/` folder. It uses the current year and week as the script only searches the last week's papers.

Within the reports folder you can find the output HTML file `arxiv_{subject}_{field}_{year}_{week}.html`

#### Basic usage

FInd all papers in a subject containing a keyword.

```bash
# Subject: Computer Science
python main.py --subject cs --keywords intelligence
# or short 
python main.py -s cs -k intelligence
```

#### Subject-field combination

Find all papers in a field of a subject containing a keyword.


```bash
# Subject: Computer Science, field: AI
python main.py --subject cs --field ai --keywords intelligence 
# or short 
python main.py -s cs -f ai -k intelligence
```

#### Multiple keywords and modes

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

#### Custom output path

The output path can be adjusted to a custom directory using the `--output_path` or `-o` flag.

```bash
python main.py --subject cs --field ai --out_path /path/to/data --keywords deep learning  # using default mode=any

# or short 

python main.py -s cs -f ai -o /path/to/data -k deep learning # using default mode=any
```

#### Regular Expressions 

Mode can also be **regex** in which case the keyword will be interpreted as a [Regular Expression](https://docs.python.org/3/howto/regex.html).

**Note:** If regular expression is used, there can only be **one** keyword, i.e. the regular expression.

