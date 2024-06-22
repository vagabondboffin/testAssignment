import pandas as pd
import json


def read_traces(file):
    with open(file) as f:
        trace_data = json.load(f)

        # Extract spans data
        spans = pd.DataFrame(trace_data['data'][0]['spans'])

        # Extract processes data
        processes = trace_data['data'][0]['processes']
        process_data = []
        for processID, process_info in processes.items():
            process_info['processID'] = processID
            process_data.append(process_info)
        processes_df = pd.DataFrame(process_data)

        # Merge spans with processes data
        spans = spans.merge(processes_df, on='processID', how='left', suffixes=('', '_process'))

        # Add traceID to spans DataFrame
        spans['traceID'] = trace_data['data'][0]['traceID']

        return spans


if __name__ == "__main__":
    df = read_traces("./traces/trace_get_all_cats.json")
    print(df.head())
print("")