# pengu

Search for POSIX commands effortlessly and locally.

## FAQ

### Why pengu?

Although `man` pages and documentation exist for this purpose, pengu aims to provide a hassle-free and intuitive experience for searching POSIX commands. Since pengu can run locally without an internet connection after installation, it can serve as a simple alternative for similar online tools.

### Will pengu replace `man` pages and documentation?

pengu does not aim to replace these tools. It is meant to be a concise **alternative** to the `man` pages, but is not a drop-in replacement.

### How many commands does pengu know?

As of now, pengu has only been trained to provide 160 commands. Its memory comprises of the full POSIX command library. However, we plan to expand pengu's library and hopefully keep it as lightweight as possible.

### Is pengu accurate?

Of course, pengu won't always give you an accurate answer, as it was built with a relatively lightweight model using spaCy and scikit-learn. However, you can reduce error rates by providing more specific prompts.

## Prerequisites

Install the following packages:

- [Python 3](https://www.python.org).

Additionally, install the following **Python** packages:

- [spaCy](https://spacy.io), which provides support for the en_core_web_sm used by pengu.
- [NumPy](https://numpy.org) for generating more efficient arrays.
- [scikit-learn](https://scikit-learn.org), a set of tools for predictive data analysis.

## Installation

To install pengu, follow the instructions below.

1. If you haven't done it already, install Python 3.9 or later. To check your version, run:

```
python --version
```

2. Clone the repository:

```bash
git clone https://github.com/v81d/pengu.git
cd pengu
```

3. Install dependencies:

```bash
pip install -U pip setuptools wheel
pip install spacy numpy scikit-learn
```

4. Download the language model from spaCy:

```bash
python -m spacy download en_core_web_sm
```

5. Install the program using the setup tool:

```bash
bash setup.sh
```
