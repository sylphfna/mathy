import tensorflow as tf


class ActorCriticModel(tf.keras.Model):
    def __init__(self, units=128, predictions=2, shared_layers=None):
        super(ActorCriticModel, self).__init__()
        self.predictions = predictions
        self.shared_layers = shared_layers
        self.in_dense = tf.keras.layers.Dense(units)
        self.value_dense = tf.keras.layers.Dense(units)
        self.pi_logits = tf.keras.layers.Dense(predictions)
        self.value_logits = tf.keras.layers.Dense(1)

    def call(self, inputs):
        inputs = self.in_dense(inputs)
        if self.shared_layers is not None:
            for layer in self.shared_layers:
                inputs = layer(inputs)
        logits = self.pi_logits(inputs)
        values = self.value_logits(self.value_dense(inputs))
        return logits, values
