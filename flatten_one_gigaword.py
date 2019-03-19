import logging
import os
import re

from argparse import ArgumentParser
from bs4 import BeautifulSoup
from spacy.lang.zh import Chinese
nlp = Chinese()

def flatten_one_gigaword_file(file_path):
    # Parse the text with BeautifulSoup
    soup = BeautifulSoup(open(file_path), "html.parser")

    # Iterate over all <p> items and get the text for each.
    all_paragraphs = []
    all_headelines = []
    for doc in soup("doc"):
        for paragraph, headline in zip(doc("text"), doc("headline")):
            # Turn inter-paragraph newlines into spaces
            paragraph = paragraph.get_text()
            paragraph = re.sub(r"\s+", "", paragraph)
            paragraph = re.sub(r"\n+", "\n", paragraph)
            paragraph = paragraph.replace("\n", " ")
            # Turn inter-paragraph newlines into spaces
            headline = headline.get_text()
            headline = re.sub(r"\s+", "", headline)
            headline = re.sub(r"\n+", "\n", headline)
            headline = headline.replace("\n", " ")
            # Tokenize the paragraph into words
            tokens = nlp(paragraph)
            para_words = [str(token) for token in tokens if not
                     str(token).isspace()]
            if len(para_words) < 10:
                continue
            tokens = nlp(headline)
            head_words = [str(token) for token in tokens if not
                     str(token).isspace()]
            if len(head_words) < 5:
                continue
            all_paragraphs.append(para_words)
            all_headelines.append(head_words)
    # Return a list of strings, where each string is a
    # space-tokenized paragraph.
    return [" ".join(headline) for headline in all_headelines]\
                ,[" ".join(paragraph) for paragraph in all_paragraphs]


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    logger = logging.getLogger(__name__)

    parser = ArgumentParser(description=("Flatten a gigaword data file for "
                                         "use in language modeling."))
    parser.add_argument("--gigaword-path", required=True,
                        metavar="<gigaword_path>", type=str,
                        help=("Path to Gigaword directory, with "
                              "all .gz files unzipped."))
    parser.add_argument("--output-dir", required=True, metavar="<output_dir>",
                        type=str, help=("Directory to write final flattened "
                                        "Gigaword file."))

    A = parser.parse_args()
    all_headelines, all_paragraphs = flatten_one_gigaword_file(A.gigaword_path)
    output_paragraph_path = os.path.join(A.output_dir,
                               os.path.basename(A.gigaword_path) + ".flat")
    output_headline_path = os.path.join(A.output_dir,
                               os.path.basename(A.gigaword_path) + ".headline")
    with open(output_headline_path, "w") as output_headline_file, open(output_paragraph_path, "w") as output_paragraph_file:
        for headline, paragraph in zip(all_headelines, all_paragraphs):
            #remove space between a-zA-Z0-9
            headline = re.sub("(?<=[a-zA-Z\d])\s+(?=[a-zA-Z\d])","", headline)
            paragraph = re.sub("(?<=[a-zA-Z\d])\s+(?=[a-zA-Z\d])","", paragraph)
            output_headline_file.write("{}\n".format(headline))
            output_paragraph_file.write("{}\n".format(paragraph))
