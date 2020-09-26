import argparse
import os
import sys
import warnings

from summarizer import summarize
from keywords import keywords

# Types of summarization
SENTENCE = 0
WORD = 1

DEFAULT_RATIO = 0.5


def textrank(text1, text2, summarize_by=SENTENCE, ratio=DEFAULT_RATIO, words=None, additional_stopwords=None):
    if summarize_by == SENTENCE:
        return summarize(text1, text2, ratio, words, additional_stopwords=additional_stopwords)
    else:
        return keywords(text1, text2, ratio, words, additional_stopwords=additional_stopwords)


def existing_file(file_name):
    try:
        with open(file_name, 'r') as file:
            return file.read()
    except Exception:
        raise argparse.ArgumentTypeError("The file provided could not be opened.")


def restricted_float(x):
    x = float(x)
    if x < 0.0 or x > 1.0:
        raise argparse.ArgumentTypeError("{} not in range [0.0, 1.0]".format(x))
    return x


def parse_args(args):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter, prog="textrank", description="Extract the most relevant sentences or keywords of a given text using the TextRank algorithm.")

    # group = parser.add_mutually_exclusive_group(required=True)
    # New API
    parser.add_argument('--summarize_text_1',
                       help="Run textrank to summarize the input text.")
    parser.add_argument('--summarize_text_2',
                       help="Run textrank to summarize the input text.")
    parser.add_argument('--ratio', '-r', metavar="r", type=restricted_float, default=DEFAULT_RATIO,
                        help="Float number (0,1] that defines the length of the summary. It's a proportion of the original text")
    parser.add_argument('--words', '-w', metavar="#words", type=int,
                        help="Number to limit the length of the summary. The length option is ignored if the word limit is set.")
    parser.add_argument('--additional_stopwords', '-a', metavar="list,of,stopwords",
                        help="Either a string of comma separated stopwords or a path to a file which has comma separated stopwords in every line")

    return parser.parse_args(args)


def main():
    args = parse_args(sys.argv[1:])

    mode = None
    text = None

    if args.summarize_text_1 and args.summarize_text_2:
        text1 = args.summarize_text_1
        text2 = args.summarize_text_2
        mode = SENTENCE
    elif args.keywords:
        text = args.keywords
        mode = WORD
    elif args.summary:  # Old api
        warnings.warn("The --summary option is deprecated. Please use either --summarize or --keywords", DeprecationWarning)
        text = args.text
        mode = args.summary

        if text is None:
            raise argparse.ArgumentTypeError('Error: no text to summarize provided.')
    else:
        raise argparse.ArgumentTypeError('Error: --summarize or --keywords is required')

    additional_stopwords = None
    if args.additional_stopwords:
        if os.path.exists(args.additional_stopwords):
            with open(args.additional_stopwords) as f:
                additional_stopwords = {s for l in f for s in l.strip().split(",")}
        else:
            additional_stopwords = args.additional_stopwords.split(",")

    print(textrank(text1, text2, summarize_by=mode, ratio=args.ratio))


if __name__ == "__main__":
    main()
