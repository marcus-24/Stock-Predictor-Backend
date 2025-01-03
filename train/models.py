from keras import layers, models, optimizers, losses  # TODO: figure out pylance errors
import tensorflow as tf


def build_bidirec_lstm_model(
    data: tf.data.Dataset, n_past: int, n_features: int, batch_size: int
) -> models.Sequential:

    # TODO: Fine tune normalization layer. Performance is lower than scikit-learn standard scaler
    norm_layer = layers.Normalization()
    norm_layer.adapt(
        data.map(lambda x, _: x)
    )  # need to calculate the mean and variance for z-score (map used to extract only features and ignore labels)

    model = models.Sequential(
        [
            layers.InputLayer(shape=(n_past, n_features), batch_size=batch_size),
            norm_layer,  # plug in fitted normalization layer
            layers.Bidirectional(layers.LSTM(20, return_sequences=True)),
            layers.Bidirectional(layers.LSTM(20, return_sequences=True)),
            layers.Dense(n_features),
        ]
    )

    optimizer = optimizers.SGD(learning_rate=0.01, momentum=0.9)
    model.compile(loss=losses.Huber(), optimizer=optimizer, metrics=["mae"])
    model.summary()

    return model
