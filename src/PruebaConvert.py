import tensorflow as tf
import h5py

with h5py.File('model.h5', 'r') as f:
    print(f.keys())

model = tf.keras.models.load_model('model.h5')

# Convert the model
converter = tf.lite.TFLiteConverter.from_saved_model('model.h5') # path to the SavedModel directory
tflite_model = converter.convert()

# Save the model
with open('model.tflite', 'wb') as f:
    f.write(tflite_model)

