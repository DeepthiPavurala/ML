import os
from tensorflow import keras
import matplotlib.pyplot as plt


class ModelTrainer:
    def __init__(self, dataset_path, img_size):
        self.dataset_path = dataset_path
        self.img_size = img_size
        self.num_epochs = 15
        self.batch_size = 160

    def load_dataset(self):
        train_datagen = keras.preprocessing.image.ImageDataGenerator(rescale=1. / 255)
        test_datagen = keras.preprocessing.image.ImageDataGenerator(rescale=1. / 255)

        train_generator = train_datagen.flow_from_directory(
            os.path.join(self.dataset_path, 'train'),
            target_size=(self.img_size, self.img_size),
            batch_size=self.batch_size,
            class_mode='sparse',
            shuffle=True  # Shuffle the data for each epoch
        )

        test_generator = test_datagen.flow_from_directory(
            os.path.join(self.dataset_path, 'test'),
            target_size=(self.img_size, self.img_size),
            batch_size=self.batch_size,
            class_mode='sparse',
            shuffle=False  # Do not shuffle the test data
        )

        return train_generator, test_generator

    def build_model(self, conv_layers, num_classes):
        model = keras.models.Sequential()
        model.add(keras.layers.Conv2D(filters=32, kernel_size=(3, 3), strides=(1, 1),
                                      padding='same', activation='relu',
                                      input_shape=(self.img_size, self.img_size, 3)))
        model.add(keras.layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same'))

        for _ in range(conv_layers - 1):
            model.add(keras.layers.Conv2D(filters=64, kernel_size=(3, 3), strides=(1, 1),
                                          padding='same', activation='relu'))
            model.add(keras.layers.MaxPooling2D(pool_size=(2, 2), strides=(2, 2), padding='same'))

        model.add(keras.layers.Flatten())
        model.add(keras.layers.Dense(units=64, activation='relu'))
        model.add(keras.layers.Dense(units=num_classes, activation='softmax'))
        return model

    def train_model(self, model, train_generator, test_generator):
        model.compile(optimizer='adam',
                      loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                      metrics=['accuracy'])

        history = model.fit(train_generator,
                            epochs=self.num_epochs,
                            validation_data=test_generator,
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


#  usage:
if __name__ == "__main__":
    dataset1_path = "Visual_Domain_Decathlon"
    dataset2_path = "Cat-Dog"

    settings = [
        (1, 32), (1, 64), (1, 112),
        (2, 32), (2, 64), (2, 112),
        (3, 32), (3, 64), (3, 112)
    ]

    # For dataset 1
    for conv_layers, img_size in settings:
        trainer1 = ModelTrainer(dataset1_path, img_size)
        train_generator1, test_generator1 = trainer1.load_dataset()
        model = trainer1.build_model(conv_layers=conv_layers, num_classes=10)
        history = trainer1.train_model(model, train_generator1, test_generator1)
        dataset1_name = "Visual Domain Decathlon dataset"
        title = f"{dataset1_name} \n Number of convolutional layers = {conv_layers} and img_size =  {img_size}"
        trainer1.plot_accuracy(history, title)

        # Evaluate the model
        test_loss, test_acc = model.evaluate(test_generator1, verbose=2)
        print('Test accuracy for  Visual Domain Decathlon dataset is:', test_acc)

    # For dataset 2
    for conv_layers, img_size in settings:
        trainer2 = ModelTrainer(dataset2_path, img_size)
        train_generator2, test_generator2 = trainer2.load_dataset()
        model = trainer2.build_model(conv_layers=conv_layers, num_classes=2)
        history = trainer2.train_model(model, train_generator2, test_generator2)
        dataset2_name = "Cat‐Dog dataset"
        title = f"{dataset2_name} \n Number of convolutional layers = {conv_layers} and img_size =  {img_size})"
        trainer2.plot_accuracy(history, title)

        # Evaluate the model
        test_loss, test_acc = model.evaluate(test_generator2, verbose=2)
        print('Test accuracy for Cat‐Dog  dataset is:', test_acc)
