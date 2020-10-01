import io
import numpy as np
import six
from typing import Dict, List, Optional, Union


class WordEmbedder:
    """ splits one or more texts into words,
        maps words to word indexes and
        maps word indexes to word embedding vectors.

        Although, the task of embedding words could also be accomplished by using an embedding layer of a Keras neural
        network model instead of this class, integrating the embedding into each model as a layer does not exploit the
        potential to share the embedding lookup table between multiple models in order save main memory when keeping
        around a larger number of models at the same time.
    """

    def __init__(self,
                 embedding_file_path: str,
                 embedding_limit: Optional[int] = None,
                 embedding_sequence_length: int = 3000
                 ):
        """
        :param embedding_file_path:
            absolute file system path to a non-compressed embedding data file from
            https://fasttext.cc/docs/en/crawl-vectors.html
            in text format (file name suffix '.vec')
        :param embedding_limit:
            the maximum number of word embeddings to read and use from embedding_path, None means 'no limit'
        :param embedding_sequence_length:
            the fixed number of word vectors to return for a given input text,
            if the input text has more words, excess words will be truncated at the end,
            if the input text has fewer words, zero vectors will be padded at the end
        """
        self.__embedding_sequence_length: int = embedding_sequence_length
        self.__word_2_index_dict, self.__embedding_matrix, almost_only_lower_case_words = \
            self.__create_word_index_dict_and_embedding_matrix(embedding_file_path, embedding_limit)
        self.__convert_texts_to_lower_case = almost_only_lower_case_words
        if self.__convert_texts_to_lower_case:
            print("will convert all input texts to lower case before looking up their word embeddings")
        self.__embedding_dim: int = self.__embedding_matrix.shape[1]
        self.__zero_embedding_vector = np.zeros(shape=self.__embedding_dim, dtype='float32')

    def embedding_dim(self) -> int:
        """
        :return: the number of dimensions of the embedding vectors, e. g. 300, depends on the embedding file used
        """
        return self.__embedding_dim

    def embed_texts(self, texts: List[str]):
        """
        returns embeddings of one or more texts.

        :param texts: a list of texts to tokenize and embed
        :return: result is a (3, len(texts), embedding_sequence_length, embedding_dim) float32 numpy.ndarray (tensor).
                 result[0] contains all embedded texts.
                 result[1] contains all embedded left contexts, i. e. embedded texts shifted by one word to the right.
                 result[2] contains all embedded right contexts, i. e. embedded words shifted by one word to the left.
        """
        padded_token_vectors = self.tokenize_texts(texts)
        embedded_texts = self.embed_token_vectors(padded_token_vectors)
        return embedded_texts

    def tokenize_texts(self, texts: List[str]):
        """
        returns fixed sized token/word index sequences of one or more texts
        :param texts: the texts to tokenize
        :return: numpy.ndarray of numpy.ndarrays of ints, plug these into embed_token_vectors to get embeddings
        """
        token_vectors = self.__texts_to_word_index_lists(texts, lower=self.__convert_texts_to_lower_case)
        padded_token_vectors = self.__pad_sequences(
            token_vectors, maxlen=self.__embedding_sequence_length, padding='post', truncating='post', value=0)
        return padded_token_vectors

    def embed_token_vector(self, token_vector):
        """
        returns embedding of a single token vector. A token is an int index into the embedding matrix.

        :param token_vector: numpy.ndarray of tokens
        :return: result is a (3, 1, token_vector.shape[0], embedding_dim) float32 tensor.
                 result[0] contains the embedded text.
                 result[1] contains the embedded left context, i. e. embedded tokens shifted by one token to the right.
                 result[2] contains the embedded right context, i. e. embedded tokens shifted by one token to the left.
        """

        token_vectors = np.asarray([token_vector])
        embedded_token_vectors = self.embed_token_vectors(token_vectors)
        return embedded_token_vectors

    def embed_token_vectors(self, token_vectors):
        """
        returns embeddings of token vectors. A token is an int index into the embedding matrix.

        :param token_vectors: numpy.ndarray of numpy.ndarrays of tokens
        :return: result is a (3, token_vectors.shape[0], token_vectors.shape[1], embedding_dim) float32 tensor.
                 result[0] contains all embedded texts.
                 result[1] contains all embedded left contexts, i. e. embedded tokens shifted by one token to the right.
                 result[2] contains all embedded right contexts, i. e. embedded tokens shifted by one token to the left.
        """

        num_words: int = token_vectors.shape[1]  # e.g. 3000
        embedding_tensor = np.empty(
            shape=(token_vectors.shape[0], num_words + 2, self.__embedding_dim), dtype='float32')
        for i, token_vector in enumerate(token_vectors):
            embedding_tensor[i, 0] = self.__zero_embedding_vector
            embedding_tensor[i, 1:num_words + 1] = self.__embedding_matrix.take(token_vector, axis=0)
            embedding_tensor[i, num_words + 1] = self.__zero_embedding_vector

        # slice 3 views from the batch_embedding_tensor
        embedded_tensor_with_contexts = [
            embedding_tensor[:, 1:-1],  # all embedded texts
            embedding_tensor[:, 0:-2],  # all embedded left contexts
            embedding_tensor[:, 2:]     # all embedded right contexts
        ]

        return embedded_tensor_with_contexts

    def __create_word_index_dict_and_embedding_matrix(
            self, embedding_file_path: str, embedding_limit: Optional[int] = None):
        """
        loads the embedding data into a dictionary mapping words to array indices (word indexes)
        and a numpy array holding a word vector numpy array per index (so-called embedding matrix)

        :param embedding_file_path: the path to the embedding file
        :param embedding_limit: the maximum number of embeddings to read from the embedding file
        :return: the word to array index dictionary,
                 the embedding matrix numpy array,
                 whether the dictionary contains (almost) only lower case words
        """
        number_of_non_lower_case_words: int = 0
        embedding_file = io.open(embedding_file_path, 'r', encoding='utf-8', newline='\n', errors='strict')
        number_of_embeddings, embedding_dim = map(int, embedding_file.readline().split())
        if embedding_limit is not None:
            number_of_embeddings: int = min(number_of_embeddings, embedding_limit)
        print(f"loading up to {number_of_embeddings} word embeddings...")
        word_2_index_dict: Dict[str, int] = {}
        embedding_matrix = np.empty((number_of_embeddings, embedding_dim), dtype='float32')
        embedding_matrix[0] = np.zeros(shape=embedding_dim, dtype='float32')  # 0 -> zero vector
        next_word_index: int = 1
        for line in embedding_file:
            if next_word_index >= number_of_embeddings:  # reached the limit or end of file
                break
            tokens = line.rstrip().split(' ')
            if len(tokens) != embedding_dim + 1:
                print(f"WARN: skipped unexpected line in embedding file: {line}")
                continue  # line does not have the expected number of tokens
            word = tokens[0]
            if word is not None and len(word) > 0:
                word_sequence = self.__text_to_word_list(word)
                if len(word_sequence) == 1:
                    # word from embedding is a single word with respect to our own word splitting method
                    if word_sequence[0].lower() != word_sequence[0]:
                        number_of_non_lower_case_words += 1
                    word_2_index_dict[word_sequence[0]] = next_word_index
                    embedding_matrix[next_word_index] = np.asarray(tokens[1:], dtype='float32')
                    next_word_index += 1
                else:
                    #print(f"skipping line with compound word {word} because it splits into {word_sequence}")
                    pass
        embedding_file.close()
        print(f"loaded {next_word_index - 1} word embeddings")
        non_lower_case_percentage: float = 100 * number_of_non_lower_case_words / max(next_word_index, 1)
        if non_lower_case_percentage < 5:
            almost_only_lower_case_words = True
            print("loaded less than 5% non-lower-case words from embedding file")
        else:
            almost_only_lower_case_words = False
            print(f"loaded {non_lower_case_percentage:.2f}% non-lower case words from embedding file")
        return word_2_index_dict, embedding_matrix, almost_only_lower_case_words

    def __texts_to_word_index_lists(self, texts: List[str], lower: bool = False) -> List[List[int]]:
        """
        transforms each text in texts to a list of word indexes (integers).
        Only words available in the word_2_index dictionary will be taken into account.

        :param a list of texts (strings)
        :return a list of lists of word indexes (ints)
        """
        return list(self.__texts_to_word_index_lists_generator(texts, lower=lower))

    def __texts_to_word_index_lists_generator(self, texts: List[str], lower: bool = False) -> List[List[int]]:
        """
        transforms each text in texts to a list of word indexes (integers).
        Only words available in the word_2_index dictionary will be taken into account.

        :param texts a list of texts (strings)
        :return yields individual lists of word indexes (ints)
        """
        for text in texts:
            word_sequence = self.__text_to_word_list(text, lower=lower)
            word_index_sequence = []
            for word in word_sequence:
                word_index = self.__word_2_index_dict.get(word)
                if word_index is not None:
                    word_index_sequence.append(word_index)
            yield word_index_sequence

    @staticmethod
    def __text_to_word_list(text: str,
                            filters: Union[List[str], str] = '!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n\r',
                            lower: bool = False,
                            split: str = ' ') -> List[str]:
        """
        splits a text into a list of words (also known as 'tokens').

        # Arguments
        :param text Input text (string).
        :param filters list (or concatenation) of characters to filter out, such as punctuation
        :param lower Whether to convert the input to lowercase.
        :param split Separator for word splitting.
        :return a list of words.
        """
        if lower:
            text = text.lower()

        translate_dict = dict((c, split) for c in filters)
        translate_map = str.maketrans(translate_dict)
        text = text.translate(translate_map)

        word_sequence = text.split(split)
        return [word for word in word_sequence if word]  # without empty words

    @staticmethod
    def __pad_sequences(sequences, maxlen=None, dtype='int32',
                        padding='pre', truncating='pre', value=0.):
        """Pads sequences to the same length.

        This function is a copy from Keras 2.3/keras_preprocessing/sequence.py
        in order to get rid of the full Keras dependency.

        This function transforms a list of
        `num_samples` sequences (lists of integers)
        into a 2D Numpy array of shape `(num_samples, num_timesteps)`.
        `num_timesteps` is either the `maxlen` argument if provided,
        or the length of the longest sequence otherwise.

        Sequences that are shorter than `num_timesteps`
        are padded with `value` at the beginning or the end
        if padding='post.

        Sequences longer than `num_timesteps` are truncated
        so that they fit the desired length.
        The position where padding or truncation happens is determined by
        the arguments `padding` and `truncating`, respectively.

        Pre-padding is the default.

        # Arguments
            sequences: List of lists, where each element is a sequence.
            maxlen: Int, maximum length of all sequences.
            dtype: Type of the output sequences.
                To pad sequences with variable length strings, you can use `object`.
            padding: String, 'pre' or 'post':
                pad either before or after each sequence.
            truncating: String, 'pre' or 'post':
                remove values from sequences larger than
                `maxlen`, either at the beginning or at the end of the sequences.
            value: Float or String, padding value.

        # Returns
            x: Numpy array with shape `(len(sequences), maxlen)`

        # Raises
            ValueError: In case of invalid values for `truncating` or `padding`,
                or in case of invalid shape for a `sequences` entry.
        """
        if not hasattr(sequences, '__len__'):
            raise ValueError('`sequences` must be iterable.')
        num_samples = len(sequences)

        lengths = []
        sample_shape = ()
        flag = True

        # take the sample shape from the first non empty sequence
        # checking for consistency in the main loop below.

        for x in sequences:
            try:
                lengths.append(len(x))
                if flag and len(x):
                    sample_shape = np.asarray(x).shape[1:]
                    flag = False
            except TypeError:
                raise ValueError('`sequences` must be a list of iterables. '
                                 'Found non-iterable: ' + str(x))

        if maxlen is None:
            maxlen = np.max(lengths)

        is_dtype_str = np.issubdtype(dtype, np.str_) or np.issubdtype(dtype, np.unicode_)
        if isinstance(value, six.string_types) and dtype != object and not is_dtype_str:
            raise ValueError("`dtype` {} is not compatible with `value`'s type: {}\n"
                             "You should set `dtype=object` for variable length strings."
                             .format(dtype, type(value)))

        x = np.full((num_samples, maxlen) + sample_shape, value, dtype=dtype)
        for idx, s in enumerate(sequences):
            if not len(s):
                continue  # empty list/array was found
            if truncating == 'pre':
                trunc = s[-maxlen:]
            elif truncating == 'post':
                trunc = s[:maxlen]
            else:
                raise ValueError('Truncating type "%s" '
                                 'not understood' % truncating)

            # check `trunc` has expected shape
            trunc = np.asarray(trunc, dtype=dtype)
            if trunc.shape[1:] != sample_shape:
                raise ValueError('Shape of sample %s of sequence at position %s '
                                 'is different from expected shape %s' %
                                 (trunc.shape[1:], idx, sample_shape))

            if padding == 'post':
                x[idx, :len(trunc)] = trunc
            elif padding == 'pre':
                x[idx, -len(trunc):] = trunc
            else:
                raise ValueError('Padding type "%s" not understood' % padding)
        return x
