import pandas as pd
from sklearn.ensemble import IsolationForest


class AnomalyDetector:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df_spans = None
        self.anomaly_detector = None

    def load_data(self):
        self.df_spans = pd.read_csv(self.file_path)

        self.df_spans.drop(columns=['trace_id'], inplace=True)
        self.df_spans.drop(columns=['span_id'], inplace=True)

    def fit(self):
        self.anomaly_detector = IsolationForest(random_state=42)

        self.anomaly_detector.fit(self.df_spans)

    def detect_anomalies(self):
        if self.df_spans is None:
            raise ValueError("Data has not been loaded. Call load_data() first.")

        # Predict outliers (-1 for anomalies, 1 for inliers)
        anomalies = self.anomaly_detector.predict(self.df_spans)

        self.df_spans['anomaly'] = anomalies

        anomalous_indices = self.df_spans[self.df_spans['anomaly'] == -1].index

        # Load original traceID and span_id from CSV using anomalous indices
        anomalous_info = []
        with open(self.file_path, 'r') as f:
            lines = f.readlines()
            header = lines[0].strip().split(',')
            for idx in anomalous_indices:
                trace_id = lines[idx + 1].strip().split(',')[header.index('trace_id')]
                span_id = lines[idx + 1].strip().split(',')[header.index('span_id')]
                anomalous_info.append(f"traceID: {trace_id} ----> spanID: {span_id}")

        return anomalous_info


# Example usage:
if __name__ == "__main__":
    detector = AnomalyDetector(file_path='files/spans_features.csv')
    detector.load_data()
    detector.fit()
    anomalous_spans_info = detector.detect_anomalies()

    for info in anomalous_spans_info:
        print(info)
