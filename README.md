# pengu

Search for POSIX commands effortlessly and locally.

## FAQ

- **Why pengu?**
  - Although `man` pages and documentation exist for this purpose, pengu aims to provide a hassle-free and intuitive experience for searching POSIX commands. Since pengu can run locally without an internet connection after installation, it can serve as a temporary replacement for similar online tools.
- **Will pengu replace `man` pages and documentation?**
  - No, pengu does not aim to replace these tools. Although pengu provides a similar experience, the documentation should always be your top priority.
- **How many commands can pengu return?**
  - As of June 2025, pengu only has 160 commands in its memory. These compose the full POSIX command library. However, we do plan to expand pengu's library and hopefully keep it as lightweight as possible.
- **Is pengu accurate?**
  - Of course, pengu won't always give you an accurate answer, as it was built with a relatively lightweight model using spaCy and scikit-learn. However, you can reduce error rates by simply providing more detailed prompts with no spelling mistakes.

## Disclaimer
- Do not prioritize this over `man` pages and documentation. It should only be used when access to such tools are limited or restricted.

## Prerequisites

Ensure that the following packages are installed:
- [Python 3](https://www.python.org) accessible in your PATH and with virtual environment support.

Additionally, install the following **Python** packages:
- [spaCy](https://spacy.io), which provides support for the en_core_web_sm used by pengu.
- [NumPy](https://numpy.org) for generating more efficient arrays.
- [scikit-learn](https://scikit-learn.org), a set of tools for predictive data analysis.

## Installation

To install pengu, follow the instructions below.

### 1. Install Python (if applicable)

If you haven't done this already, make sure Python 3 or newer is installed. To check your version, run:

```
python --version
```

### 2. Clone the repository

Ensure [Git](https://git-scm.com/downloads) is installed on your system. Run:

```bash
git clone https://github.com/v81d/pengu.git
cd pengu
```

### 3. Install dependencies

```bash
pip install -U pip setuptools wheel
pip install spacy numpy scikit-learn
```

### 4. Download the language model from spaCy

```bash
python -m spacy download en_core_web_sm
```

### 5. Install the program using the setup tool

```bash
bash setup.sh
```
