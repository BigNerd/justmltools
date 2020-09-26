import numpy as np
import os
import pathlib
from unittest import TestCase
from justmltools.nlp.word_embedder import WordEmbedder


class TestWordEmbedder(TestCase):

    """ sample_text consists of the 100 words contained in the embedding file,
        however, the three '/'-separated words, e.g. zürich/winterthur, will not be loaded by the word embedder
        because '/' is used as a word boundary in the same way as whitespace by its tokenizer
    """
    sample_text = """
        humboldtgesellschaft gallersbach risikopositionswert „sekunde gallesium kleindemsin eboracensium qorig pagamento 
        beisammenbleiben homosexuellenprozesse polymerasekomplex unharmonisches brennstofflagerung balabin 
        „dauerkonflikt bildgießereien vvitch durchkonjugiert gainsbarre flugbootpionier „organisiertes todiraș 
        hintergrundannahme sorridere strategieprofil navesi quadripustulata rightmire halbjahresabonnement davorstand 
        steenaben gläsgen herrschaftsstellung femtogramm forstlehrlinge sternenplatz memmingen/archiv/ axialvektoren 
        pertubuhan tempolimiten aliyye plagiatmasche relevanzkriterieum wüstenbewohnende senstadtum xwars bartholdo 
        anlagesystem benennungsschemas „nrated „forg börsenrechtliche blautopfes „forge waidhauser dolds assignierten 
        voiß worowitz weirowa türsturze iovita supergravitations oradeafc labelgruppe metallblöcken dysphemistisch 
        conferuntur kuntas einzelbestand bestandsaufnahme/diskussion börsenrechtlicher „spurensuche… hervicusgasse 
        toteisblockes wirtschaftskontakten hohnohka drainageplatten flackenheide chaonnophris lindakoennecke 
        möbelabteilung lehrgangsende ‚ecke‘ motife schutzbestrebungen corval corythucha mölmschen sanandi ysatis 
        metronetze albumbilder døttre zürich/winterthur stevenisten forstén sandener batrachotoxine
        """

    def setUp(self) -> None:
        dir_path: str = pathlib.Path(__file__).parent.absolute()
        embedding_file_path: str = os.path.join(dir_path, "embedding_wiki_de_tail_100.vec")
        self.word_embedder: WordEmbedder = WordEmbedder(embedding_file_path=embedding_file_path)

    def test_embedding_dim(self):
        self.assertEqual(300, self.word_embedder.embedding_dim())

    def test_tokenize_texts(self):
        token_matrix: np.nd_array = self.word_embedder.tokenize_texts([self.sample_text])
        self.assertEqual(1, token_matrix.shape[0])  # one row for one text
        self.assertEqual(3000, token_matrix.shape[1])  # 3000 columns for 3000 tokens (including padded 0s at the end)

        tokenized_text = token_matrix[0]

        number_of_non_zero_tokens: int = np.count_nonzero(tokenized_text)
        self.assertEqual(97, number_of_non_zero_tokens)  # only 97, not 100 because '/'-separated words are skipped

        number_of_unique_tokens = np.unique(tokenized_text).shape[0]
        self.assertEqual(97 + 1, number_of_unique_tokens)  # one unique token for each unique word plus one for 0

    def test_embed_texts(self):
        embedded_texts: np.nd_array = self.word_embedder.embed_texts([self.sample_text])
        self.assertEqual(3, len(embedded_texts))  # 3 embeddings, for text, left context and right context

        embedded_text = embedded_texts[0]
        self.assertEqual(3000, embedded_text.shape[1])

        embedded_left_context = embedded_texts[1]
        self.assertEqual(3000, embedded_left_context.shape[1])

        embedded_right_context = embedded_texts[2]
        self.assertEqual(3000, embedded_right_context.shape[1])
