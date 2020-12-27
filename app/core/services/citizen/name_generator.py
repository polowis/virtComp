from __future__ import annotations
import numpy as np
import pickle

import os
from tensorflow import keras # noqa
from keras.preprocessing.text import text_to_word_sequence
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras.layers import LSTM, TimeDistributed
from typing import Union


class NameGenerator(object):
    """
    The Machine Learning Model to generate words.
    You can pass text in any language. Numbers and any symbol such as @#$ will be trimmed.

    Unless you want to train the dataset, otherwise. Please consider using
    NameGenerator.load() to load the model

    Package prequestities: Tensorflow, numpy
    """
    def __init__(self, file_model: Union[str, None] = None, wordlist=None, config: dict = None):
        self._debug = True

        if file_model is not None:
            # replace new line with spaces
            wordlist = self.read_file_content(file_model)

        self._epochs = 100

        self._batch_size = 64

        self._n_layers = 2

        self._hidden_dim = 50

        self.temperature = 1.0
        
        self.min_word_len = 4
        
        self.max_word_len = 12
        
        self.suffix_word = ''

        self.prefix_word = ''

        if config is not None:
            self.load_config(config)


        # Keep only unique words:
        self.wordlist = sorted(set(wordlist))
        # Terminate each word with a newline:
        self.wordlist = [word.strip() + '\n' for word in self.wordlist]

        # find unique characters
        self.chars = sorted(list(set(
            [char for word in self.wordlist for char in word]
        )))

        self.vocab_size = len(self.chars)
        self.corpus_size = len(self.wordlist)

        # generate mapping from index to char and char to index
        self.char_to_idx = {u: i for i, u in enumerate(self.chars)}
        self.idx_to_char = np.array(self.chars)

        self.print_overall_stats()
    
    
    def debug(self, value: bool = True) -> NameGenerator:
        """
        Set the debug mode. Default is True
        """
        self._debug = value
        return self
    
    def epochs(self, value: int = 100) -> NameGenerator:
        """
        Number of epochs to train RNN
        """
        self._epochs = value
        return self
    
    def batch_size(self, value: int = 64) -> NameGenerator:
        """
        The batch size for training the RNN
        """
        self._batch_size = value
        return self
    
    def n_layers(self, value: int = 2) -> NameGenerator:
        """Number of LSTM layers in the model"""
        self._n_layers = value
        return self
    
    def hidden_dim(self, value: int = 50) -> NameGenerator:
        """Number of hidden units per LSTM layer"""
        self._hidden_dim = value
        return self
    

    def read_file_content(self, path):
        """Read the content in the file and return list of words that are alphabetical"""
        text_contents = open(path).read().replace('\n', ' ')
        if self._debug:
            print('Received content!')
        # exclude non alphabetical characters
        wordlist = text_to_word_sequence(
            text_contents,
            filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~0123456789–…\'\"’«·»' # noqa
        )

        return wordlist
    
    def load_config(self, config: dict) -> None:
        """Load config keys from dict. The dict must contains ONLY supported config keys"""
        for key, value in config.items():
            setattr(self, key, value)

    def save(self, directory: str = './app/core/services/model/name_generator', overwrite=False) -> None:
        """Save the model to specific directory. Will create new if file does not exist."""
        if not overwrite:
            assert not os.path.exists(directory), 'Directory already ' + \
                'exists! Please choose a non-existing path.'

        if not os.path.exists(directory):
            os.makedirs(directory)

        pickle.dump(self.config_to_dict(),
                    open(os.path.join(directory, 'config.pkl'), "wb"), pickle.HIGHEST_PROTOCOL)
        pickle.dump(self.wordlist,
                    open(os.path.join(directory, 'words.pkl'), "wb"), pickle.HIGHEST_PROTOCOL)
        self.model.save(os.path.join(directory, 'model.h5'))
    
    def print_overall_stats(self):
        """Print the overall stats observing this dataset"""
        print(self.corpus_size, "unique words\n")
        print(len(self.chars), "characters, including the \\n:")
        print(self.chars)
        print("\nFirst five sample words:")
        print(self.wordlist[:5])
    
    def fit(self):
        """Fitting model"""
        if self._debug:
            print("Training....")
        X = np.zeros((self.corpus_size,
                      self.max_word_len,
                      self.vocab_size))
        Y = np.zeros((self.corpus_size,
                      self.max_word_len,
                      self.vocab_size))
        
        for word_i in range(self.corpus_size):
            word = self.wordlist[word_i]
            chars = list(word)

            for char_j in range(min(len(word), self.max_word_len)):
                char = chars[char_j]
                char_idx = self.char_to_idx[char]
                X[word_i, char_j, char_idx] = 1
                if char_j > 0:
                    # the 'next char' at time point char_j
                    Y[word_i, char_j - 1, char_idx] = 1
        
        model = Sequential()
        model.add(LSTM(self._hidden_dim, input_shape=(None, self.vocab_size),
                       return_sequences=True))
        for i in range(self._n_layers - 1):
            model.add(LSTM(self._hidden_dim, return_sequences=True))
        model.add(TimeDistributed(Dense(self.vocab_size)))
        model.add(Activation('softmax'))
        model.compile(loss="categorical_crossentropy", optimizer="rmsprop")

        model.fit(X, Y, batch_size=self._batch_size, verbose=0, epochs=self._epochs)

        self.model = model
        if self._debug:
            print("Training complete")
    
    def generate_word(self, n=10) -> list:
        """Call this function to generate word
        
        :param n: The number of words you wish to train
        """
        assert hasattr(self, 'model'), 'Call the fit() method first!'
        words = []
        for i in range(n):
            words.append(self.proccess_output(self.model))
            # words.append(word + self.config.suffix)
        return words
    
    @classmethod
    def load(cls, directory: str = './app/core/services/model/name_generator'):
        """Load model from given directory
        
        The directory must contains pre trained model with 3 files named as follow:

        'config.pkl' => store configuration key

        'words.pkl' => store lists of words (in any language, NOT SENTENCE)

        'model.h5' => the core model
        """
        if not os.path.exists(directory):
            raise FileExistsError("Directory not found")
        config = pickle.load(
            open(os.path.join(directory, 'config.pkl'), 'rb'))
        wordlist = pickle.load(
            open(os.path.join(directory, 'words.pkl'), 'rb'))
        
        model = keras.models.load_model(os.path.join(directory, 'model.h5'))
        generator = cls(config=config, wordlist=wordlist)
        generator.model = model
        return generator
        

    
    def proccess_output(self, model: Sequential) -> str:
        """
        This is the core function to generate word
        """
        X = np.zeros((1, self.max_word_len, self.vocab_size))

        # sample the first character
        initial_char_distribution = self.scale_temperature(
            model.predict(X[:, 0:1, :]).flatten(), self.temperature
        )

        ix = 0

        # make sure the initial character is not a newline (i.e. index 0)
        while ix == 0:
            ix = int(np.random.choice(self.vocab_size, size=1,
                                      p=initial_char_distribution))

        X[0, 0, ix] = 1

        # start with first character, then later successively append chars
        generated_word = [self.idx_to_char[ix].upper()]

        # sample all remaining characters
        for i in range(1, self.max_word_len):
            next_char_distribution = self.scale_temperature(
                model.predict(X[:, 0:i, :])[:, i - 1, :].flatten(),
                self.temperature
            )

            ix_choice = np.random.choice(
                self.vocab_size, size=1, p=next_char_distribution
            )

            ctr = 0
            while ix_choice == 0 and i < self.min_word_len:
                ctr += 1
                # sample again if you picked the end-of-word token too early
                ix_choice = np.random.choice(
                    self.vocab_size, size=1, p=next_char_distribution
                )
                if ctr > 1000:
                    print("caught in a near-infinite loop."
                          "You might have picked too low a temperature "
                          "and the sampler just keeps sampling \\n's")
                    break

            next_ix = int(ix_choice)
            X[0, i, next_ix] = 1
            if next_ix == 0:
                break
            generated_word.append(self.idx_to_char[next_ix])

        return ('').join(generated_word)

    def scale_temperature(self, probs, temperature=1.0):
        """Scale probabilities according to some temperature.
        Temperatures lower than 1 mean "cold", i.e. more conservative sampling. A
        low temperature (< 1 and approaching 0) results in the char sampling
        approaching the argmax. A high temperature (> 1, approaching infinity)
        results in sampling from a uniform distribution)
        """

        probs = np.exp(np.log(probs) / temperature)
        probs = probs / np.sum(probs)
        return probs
    
    def config_to_dict(self) -> dict:
        """Return configuration keys as dict"""
        config_objects: dict = {
            '_epochs': self._epochs,
            '_batch_size': self._batch_size,
            '_n_layers': self._n_layers,
            '_hidden_dim': self._hidden_dim,
            'temperature': self.temperature,
            'min_word_len': self.min_word_len,
            'max_word_len': self.max_word_len,
            'suffix_word': self.suffix_word,
            'prefix_word': self.prefix_word
        }
        
        return config_objects