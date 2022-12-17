import tensorflow as tf

# Define the neural network
model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(units=16, activation='relu', input_shape=(10,)))
model.add(tf.keras.layers.Dense(units=1, activation='sigmoid'))

# Compile the model
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

# Train the model
model.fit(x_train, y_train, epochs=10)

# Evaluate the model
model.evaluate(x_test, y_test)
