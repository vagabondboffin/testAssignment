import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, LSTM, RepeatVector, TimeDistributed, Dense


class LSTMAutoencoderAnomalyDetector:
    def __init__(self, sequence_length=10, lstm_units=64, epochs=50, batch_size=32, validation_split=0.1,
                 threshold_percentile=95):
        self.sequence_length = sequence_length
        self.lstm_units = lstm_units
        self.epochs = epochs
        self.batch_size = batch_size
        self.validation_split = validation_split
        self.threshold_percentile = threshold_percentile
        self.scaler = MinMaxScaler()
        self.autoencoder = None

    def build_model(self, input_dim, timesteps):
        inputs = Input(shape=(timesteps, input_dim))
        encoded = LSTM(self.lstm_units, activation='relu', return_sequences=False)(inputs)
        encoded = RepeatVector(timesteps)(encoded)
        decoded = LSTM(self.lstm_units, activation='relu', return_sequences=True)(encoded)
        outputs = TimeDistributed(Dense(input_dim))(decoded)

        self.autoencoder = Model(inputs, outputs)
        self.autoencoder.compile(optimizer='adam', loss='mse')

    def preprocess_data(self, data):
        data = data.sort_values(by='start_time')
        features = data.drop(columns=['span_id', 'trace_id', 'start_time'])
        scaled_features = self.scaler.fit_transform(features)

        sequences = []
        for i in range(len(scaled_features) - self.sequence_length + 1):
            sequences.append(scaled_features[i:i + self.sequence_length])

        data_with_sequences = data.iloc[self.sequence_length - 1:].reset_index(drop=True)

        return np.array(sequences), data_with_sequences

    def fit(self, file_path):
        data = pd.read_csv(file_path)
        sequences, data_with_sequences = self.preprocess_data(data)
        input_dim = sequences.shape[2]
        timesteps = sequences.shape[1]

        self.build_model(input_dim, timesteps)
        self.autoencoder.fit(sequences, sequences, epochs=self.epochs, batch_size=self.batch_size,
                             validation_split=self.validation_split, shuffle=False)
        return data_with_sequences

    def detect_anomalies(self, data_with_sequences):
        sequences, _ = self.preprocess_data(data_with_sequences)
        reconstructed_sequences = self.autoencoder.predict(sequences)
        reconstruction_error = np.mean(np.abs(reconstructed_sequences - sequences), axis=(1, 2))
        threshold = np.percentile(reconstruction_error, self.threshold_percentile)
        anomalies = reconstruction_error > threshold
        anomalous_spans = data_with_sequences.iloc[anomalies.nonzero()[0]]

        return anomalous_spans

    def print_anomalies(self, anomalous_spans):
        for index, row in anomalous_spans.iterrows():
            print(f"traceID: {row['trace_id']} ----> spanID: {row['span_id']}")


# Usage
detector = LSTMAutoencoderAnomalyDetector(sequence_length=10, lstm_units=64, epochs=50, batch_size=32,
                                          validation_split=0.1, threshold_percentile=95)
data_with_sequences = detector.fit('files/spans_features.csv')
anomalous_spans = detector.detect_anomalies(data_with_sequences)
detector.print_anomalies(anomalous_spans)
