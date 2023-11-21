from antifraud_homework.pyspark_utils import clean_data_with_pyspark
import subprocess


if __name__ == '__main__':
    # Запускаем команду s3cmd
    command = 's3cmd ls s3://otus-mlops-bucket-bvo/fraud-data/'
    output = subprocess.check_output(command, shell=True)
    
    # Обрабатываем вывод команды
    files = output.decode().splitlines()
    
    for file in files:
        file = file.split()[-1].split('/')[-1].split('.')[0]
        s3path_inp = f's3a://otus-mlops-bucket-bvo/fraud-data/{file}.txt'
        s3path_out = f's3a://otus-mlops-bucket-bvo-processed/fraud-data/{file}.parquet'
        clean_data_with_pyspark(s3path_inp, s3path_out)

