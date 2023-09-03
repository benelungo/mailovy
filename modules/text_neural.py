import os
import pickle

import numpy as np
from googletrans import Translator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, MaxPooling1D, Conv1D, GlobalMaxPooling1D, Dropout, LSTM, GRU
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras import utils
import pandas as pd

from modules import tools
from modules.tools import save_in_bites, load_from_bites

text_to_classify = [r'''Fears for T N pension after talks","Unions representing workers at Turner Newall say they are 'disappointed' after talks with stricken parent firm Federal Mogul."''',
                    r'''The Race is On: Second Private Team Sets Launch Date for Human Spaceflight (SPACE.com)","SPACE.com - TORONTO, Canada -- A second\team of rocketeers competing for the  #36;10 million Ansari X Prize, a contest for\privately funded suborbital space flight, has officially announced the first\launch date for its manned rocket.''',
                    r'''Ky. Company Wins Grant to Study Peptides (AP)","AP - A company founded by a chemistry researcher at the University of Louisville won a grant to develop a method of producing better peptides, which are short chains of amino acids, the building blocks of proteins.''',
                    r'''"Calif. Aims to Limit Farm-Related Smog (AP)","AP - Southern California's smog-fighting agency went after emissions of the bovine variety Friday, adopting the nation's first rules to reduce air pollution from dairy cow manure."''',
                    r'''Open Letter Against British Copyright Indoctrination in Schools","The British Department for Education and Skills (DfES) recently launched a ""Music Manifesto"" campaign, with the ostensible intention of educating the next generation of British musicians. Unfortunately, they also teamed up with the music industry (EMI, and various artists) to make this popular. EMI has apparently negotiated their end well, so that children in our schools will now be indoctrinated about the illegality of downloading music.The ignorance and audacity of this got to me a little, so I wrote an open letter to the DfES about it. Unfortunately, it's pedantic, as I suppose you have to be when writing to goverment representatives. But I hope you find it useful, and perhaps feel inspired to do something similar, if or when the same thing has happened in your area.''',
                    r'''Loosing the War on Terrorism","\\""Sven Jaschan, self-confessed author of the Netsky and Sasser viruses, is\responsible for 70 percent of virus infections in 2004, according to a six-month\virus roundup published Wednesday by antivirus company Sophos.""\\""The 18-year-old Jaschan was taken into custody in Germany in May by police who\said he had admitted programming both the Netsky and Sasser worms, something\experts at Microsoft confirmed. (A Microsoft antivirus reward program led to the\teenager's arrest.) During the five months preceding Jaschan's capture, there\were at least 25 variants of Netsky and one of the port-scanning network worm\Sasser.""\\""Graham Cluley, senior technology consultant at Sophos, said it was staggeri ...\\"''']

PATH_TO_DATASETS = "data/datasets/"
PATH_TO_MODELS = "data/models/"

class DatasetBBC:
    def __init__(self):
        self.num_words = 10000
        self.max_news_len = 100
        self.nb_classes = 5
        self.name = "bbc"
        self.dataset_path = os.path.join(PATH_TO_DATASETS, self.name)
        self.model_path = os.path.join(PATH_TO_MODELS, self.name + ".h5")
        self.tokenizer_path = os.path.join(PATH_TO_MODELS, self.name + ".tok")
        self.class_names = ["business", "entertainment", "politics", "sport", "tech"]

    def get_train_data(self):
        train_data = []
        train_classes = []
        for class_index, class_name in enumerate(self.class_names):
            path_to_data_folder = os.path.join(self.dataset_path, class_name)
            for file_name in os.listdir(path_to_data_folder):
                path_to_data = os.path.join(path_to_data_folder, file_name)
                try:
                    with open(path_to_data, 'r') as f:
                        data = " ".join(f.readlines())
                    train_data.append(data)
                    train_classes.append(class_index)
                except Exception as e:
                    print(e)
                    print(class_name)
                    print(file_name)

        return train_data, train_classes

class DatasetAgNews:
    def __init__(self):
        self.num_words = 10000
        self.max_news_len = 100
        self.nb_classes = 4
        self.name = "ag_news_csv"
        self.train_name = 'train.csv'
        self.val_name = 'test.csv'
        self.classes_name = "classes.txt"
        self.dataset_path = os.path.join(PATH_TO_DATASETS, self.name)
        self.train_path = os.path.join(self.dataset_path, self.train_name)
        self.val_path = os.path.join(self.dataset_path, self.val_name)
        self.model_path = os.path.join(PATH_TO_MODELS, self.name + ".h5")
        self.tokenizer_path = os.path.join(PATH_TO_MODELS, self.name + ".tok")
        with open(os.path.join(self.dataset_path, self.classes_name)) as f:
            self.class_names = [line.strip() for line in f.readlines()]

    def get_train_data(self):
        train = pd.read_csv(self.train_path,
                            header=None,
                            names=['class', 'title', 'text'])
        train_data = train['title'] + " " + train["text"]
        train_classes = train['class'] - 1
        return train_data, train_classes

    def get_val_data(self):
        val = pd.read_csv(self.val_path,
                            header=None,
                            names=['class', 'title', 'text'])
        val_data = val['title'] + " " + val["text"]
        val_classes = val['class'] - 1
        return val_data, val_classes

class DatasetAmazon:
    def __init__(self):
        self.num_words = 100000
        self.max_news_len = 1000
        self.nb_classes = 6
        self.name = "amazon-texts"
        self.train_name = 'train_40k.csv'
        self.val_name = 'val_10k.csv'
        self.classes_name = "classes.txt"
        self.dataset_path = os.path.join(PATH_TO_DATASETS, self.name)
        self.train_path = os.path.join(self.dataset_path, self.train_name)
        self.val_path = os.path.join(self.dataset_path, self.val_name)
        self.model_path = os.path.join(PATH_TO_MODELS, self.name + ".h5")
        self.tokenizer_path = os.path.join(PATH_TO_MODELS, self.name + ".tok")

        self.class_names = None

        train = pd.read_csv(self.train_path)
        train_classes = train['Cat1']  # + " | " + train['Cat2'] + " | " + train['Cat3']
        self.class_names = train_classes.unique()
        self.nb_classes = len(self.class_names)

    def get_train_data(self):
        train = pd.read_csv(self.train_path)
        train_data = train['Title'] + " " + train["Text"]
        train_classes = train['Cat1']  # + " | " + train['Cat2'] + " | " + train['Cat3']
        train_classes = train_classes.apply(lambda x: np.where(self.class_names == x)[0][0])
        return str(train_data), train_classes

class TextNeural:
    def __init__(self, dataset):
        self.translator = Translator()
        self.dataset = dataset
        # self.dataset = DatasetEmail()

        self.checkpoint_callback_cnn = ModelCheckpoint(self.dataset.model_path,
                                                       monitor='val_accuracy',
                                                       save_best_only=True,
                                                       verbose=1)
        self.tokenizer = Tokenizer(num_words=self.dataset.num_words)
        self.model = self.cnn_model_compile()
        self.load_model()

    def cnn_model_compile(self):
        model_cnn = Sequential()
        model_cnn.add(Embedding(self.dataset.num_words, 32, input_length=self.dataset.max_news_len))
        model_cnn.add(Conv1D(250, 5, padding='valid', activation='relu'))
        model_cnn.add(GlobalMaxPooling1D())
        model_cnn.add(Dense(128, activation='relu'))
        model_cnn.add(Dense(self.dataset.nb_classes, activation='softmax'))

        model_cnn.compile(optimizer='adam',
                          loss='categorical_crossentropy',
                          metrics=['accuracy'])
        return model_cnn

    def load_model(self):
        if os.path.exists(self.dataset.model_path):
            try:
                self.model = self.cnn_model_compile()
                self.model.load_weights(self.dataset.model_path)
            except Exception as e:
                print(e)
                tools.rm(self.dataset.model_path)
                self.create_new_model()
        if os.path.exists(self.dataset.tokenizer_path):
            try:
                self.tokenizer = load_from_bites(self.dataset.tokenizer_path)
            except Exception as e:
                print(e)
                tools.rm(self.dataset.tokenizer_path)
                self.create_new_model()

    def create_new_model(self):
        train_data, train_classes = self.dataset.get_train_data()
        self.tokenizer.fit_on_texts(train_data)
        sequences = self.tokenizer.texts_to_sequences(train_data)
        x_train = pad_sequences(sequences, maxlen=self.dataset.max_news_len)
        y_train = utils.to_categorical(train_classes, self.dataset.nb_classes)

        self.model = self.cnn_model_compile()

        self.model.fit(x_train,
                       y_train,
                       epochs=3,
                       batch_size=8,
                       validation_split=0.1,
                       callbacks=[self.checkpoint_callback_cnn],
                       shuffle=True)

        save_in_bites(self.tokenizer, self.dataset.tokenizer_path)

        '''
        # Evaluate model
        val_data, val_classes = self.dataset.get_val_data()

        test_sequences = self.tokenizer.texts_to_sequences(val_data)
        x_test = pad_sequences(test_sequences, maxlen=self.dataset.max_news_len)
        y_test = utils.to_categorical(val_classes, self.dataset.nb_classes)
        self.model.load_weights(self.dataset.model_path)
        self.model.evaluate(x_test, y_test, verbose=1)
        '''

    def predict(self, texts):
        self.load_model()
        texts = [self.translator.translate(txt, dest='en').text for txt in texts]
        sequences = self.tokenizer.texts_to_sequences(texts)
        sequences = pad_sequences(sequences, maxlen=self.dataset.max_news_len)
        prediction = self.model.predict(sequences)
        result = []
        for i, pred in enumerate(prediction):
            result.append([])
            for j, class_name in enumerate(self.dataset.class_names):
                if pred[j] > 0.1:
                    result[i].append([class_name.capitalize(), pred[j]])
        return result

# TextNeural().create_new_model()

