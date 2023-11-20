import pandas as pd
from antifraud_homework.pyspark_utils import clean_data_with_pyspark


def test_clean_data_with_pyspark_success():
    
    file_inp = './tests/temp/test__clean_data_with_pyspark.csv'
    file_out = './tests/temp/test__clean_data_with_pyspark_processed'
    
    test_df_inp = pd.DataFrame([
        ["0", "2019-08-22 00:00:00", "0", "0", "100.00", "0", "0", "0", "0"],
        ["0", "2019-08-22 00:00:00", "0", "0", "100.00", "0", "0", "0", "0"],
        ["1", "2019-08-22 23:59:59", "0", "0", "100.00", "86399", "0", "0", "0"],
        ["2", "2019-08-22 24:00:00", "0", "0", "100.00", "86400", "0", "0", "0"],
        ["3", "2019-08-23 00:00:00", "-999999", "0", "100.00", "86400", "1", "0", "0"],
        ["4", "2019-08-23 00:00:00", "1", "Err", "100.00", "86400", "1", "0", "0"],
        ["5", "2019-08-23 00:00:00", "2", None, "100.00", "86400", "1", "0", "0"],
        ["6", "2019-08-23 00:00:00", "2", "22000", "100.00", "86400", "1", "0", "0"],
        ["7", "2019-08-31 24:00:00", "3", "2", "100.00", "864000", "9", "0", "0"],
        ["8", "2019-09-05 12:00:00", "4", "3", "100.00", "43200", "14", "0", "0"]], 
        columns=[
            'transaction_id', 'tx_datetime', 'customer_id', 'terminal_id',
            'tx_amount', 'tx_time_seconds', 'tx_time_days', 'tx_fraud',
            'tx_fraud_scenario']
        )
    
    test_df_inp.to_csv(file_inp, sep=',', index=False)

    status_code = clean_data_with_pyspark(file_inp, file_out)
    
    assert status_code == 0

    test_df_out = pd.DataFrame([
        ['0', '2019-08-22 00:00:00', '0', '0', '100.00', '0', '0', '0', '0'],
        ['1', '2019-08-22 23:59:59', '0', '0', '100.00', '86399', '0', '0', '0'],
        ['2', '2019-08-23 00:00:00', '0', '0', '100.00', '86400', '1', '0', '0'],
        ['7', '2019-09-01 00:00:00', '3', '2', '100.00', '864000', '10', '0', '0'],
        ['8', '2019-09-05 12:00:00', '4', '3', '100.00', '1252800', '14', '0', '0']], 
        columns=[
            'transaction_id', 'tx_datetime', 'customer_id', 'terminal_id',
            'tx_amount', 'tx_time_seconds', 'tx_time_days', 'tx_fraud', 
            'tx_fraud_scenario']
    )

    assert test_df_out.equals(
        pd.read_parquet(file_out)
        .sort_values(by=['transaction_id'])
        .reset_index(drop=True)
        .astype(str)
    )
