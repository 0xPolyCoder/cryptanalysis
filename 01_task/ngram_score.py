"""
    ngram_score module to provide a mechanism to score
    texts based on a n-gram lookup table. The lookup
    table has to be created out-of-band.
"""

from math import log10


class NGramScore:
    """
        ngram_score class to calculate the n-gram score
        of a text based on a lookup table of the most
        common n-grams in a specific language.
    """

    def __init__(self, file_name, sep=' '):
        """
            Construct a new n-gram lookup table from the
            provided file. The assumed file structure is
            <ngram> <number-of-occurrences>, separated by
            a whitespace.
        """
        # read in raw file
        self.ngrams = {}
        with open(file_name, 'r') as raw_file:
            for line in raw_file:
                ngram, count = line.split(sep)
                self.ngrams[ngram] = int(count)

        # store some internal parameters
        self.order = len(ngram)
        self.total_ngrams = sum(self.ngrams.values())

        # calculate probabilities
        for ix in self.ngrams:
            p = log10(float(self.ngrams[ix]) / self.total_ngrams)
            self.ngrams[ix] = p

        # define default probability for n-grams
        # not occurring in the given lookup table
        self.default_value = log10(0.01/self.total_ngrams)

    def score(self, input_text, normalize=False):
        """
            Calculate the score of the input text based on
            the lookup table. The option 'normalize' is used
            to normalize the score based on the text input
            length. While this is required to compare texts of
            different length, it has negative effects on scoring
            texts of same length! Only enable it if required!
        """
        score = 0
        text = input_text.upper()
        for idx in range(len(text)-self.order+1):
            current_ngram = text[idx:idx+self.order]
            if current_ngram in self.ngrams:
                score += self.ngrams[current_ngram]
            else:
                score += self.default_value

        if normalize:
            score = score / (len(text)-self.order+1)

        return score
