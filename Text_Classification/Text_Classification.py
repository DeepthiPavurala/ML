import os
from tensorflow import keras
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split


class ModelTrainer:
    def __init__(self, dataset_path, max_phrase_length):
        self.dataset_path = dataset_path
        self.max_phrase_length = max_phrase_length
        self.num_epochs = 15
        self.batch_size = 64
        self.max_number_words = 50000

    def load_dataset(self):
        df = pd.read_csv(os.path.join(self.dataset_path, 'Movie_Reviews.csv'))

        tokenizer = keras.preprocessing.text.Tokenizer(num_words=self.max_number_words, filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~', lower=True)
        tokenizer.fit_on_texts(df['text'].values)
        x = tokenizer.texts_to_sequences(df['text'].values)
        x = keras.preprocessing.sequence.pad_sequences(x, maxlen=self.max_phrase_length)
        y = pd.get_dummies(df['label']).values
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)

        return (x_train, y_train), (x_test, y_test)

    def build_model(self, lstm_units, embedding_dim, max_phrase_length):
        model = keras.models.Sequential()
        model.add(keras.layers.Embedding(input_dim=self.max_number_words, output_dim=embedding_dim,
                                         input_shape=(max_phrase_length,)))
        model.add(keras.layers.SpatialDropout1D(0.1))
        model.add(keras.layers.LSTM(units=lstm_units, activation='relu', dropout=0.2, recurrent_dropout=0.2))
        model.add(keras.layers.Dense(units=128, activation='relu'))
        model.add(keras.layers.Dropout(0.2))
        model.add(keras.layers.Dense(units=2, activation='softmax'))
        return model

    def train_model(self, model, train_data, test_data):
        x_train, y_train = train_data
        x_test, y_test = test_data

        model.compile(optimizer='adam',
                      loss='categorical_crossentropy',
                      metrics=['accuracy'])

        history = model.fit(x_train, y_train,
                            epochs=self.num_epochs,
                            batch_size=self.batch_size,
                            validation_data=(x_test, y_test),
                            verbose=1)
        return history

    def plot_accuracy(self, history, title):
        plt.plot(history.history['accuracy'], label='Training Accuracy')
        plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.title(title)
        plt.legend()
        plt.show()


if __name__ == "__main__":
    dataset_path = ""
    settings = [
        (64, 75, 50), (64, 75, 75), (64, 75, 100),
        (64, 100, 50), (64, 100, 75), (64, 100, 100),
        (128, 75, 50), (128, 75, 75), (128, 75, 100),
        (128, 100, 50), (128, 100, 75), (128, 100, 100),
        (256, 75, 50), (256, 75, 75), (256, 75, 100),
        (256, 100, 50), (256, 100, 75), (256, 100, 100)
    ]

    trainer = ModelTrainer(dataset_path, max_phrase_length=70)

    # For each setting
    for lstm_units, embedding_dim, max_phrase_length in settings:
        print(f"Training with settings: LSTM_units={lstm_units}, embedding_dim={embedding_dim}, max_phrase_length={max_phrase_length}")

        # Load dataset
        (x_train, y_train), (x_test, y_test) = trainer.load_dataset()

        # Build model
        model = trainer.build_model(lstm_units=lstm_units, embedding_dim=embedding_dim, max_phrase_length=max_phrase_length)

        # Train model
        history = trainer.train_model(model, train_data=(x_train, y_train), test_data=(x_test, y_test))

        # Plot accuracy
        title = f"LSTM_units={lstm_units} and embedding_dim={embedding_dim} and max_phrase_length={max_phrase_length}"
        trainer.plot_accuracy(history, title)

        # Evaluate the model
        test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
        print('Test accuracy:', test_acc)
