from pathlib import Path
import os
import pandas as pd

CONFIG_PATH = './config/'
DATA_PATH = './data/'

def main():
    db = DataBase('project')
    #db.create_table('CLIENTE', ['ID', 'NOME', 'CPF'])
    #db.drop_table('CLIENTE')
    #db.insert('CLIENTE', ['1', 'Martin', '480484840'])
    db.insert('CLIENTE', ['2', 'Karol', '025494'])
    db.insert('CLIENTE', ['3', 'Gustavo', '69'])
    db.insert('CLIENTE', ['4', 'Tesouro', '24'])
    #db.delete('CLIENTE', '1')
    #db.update('CLIENTE', '4', ['4', 'Tesouro', '99'])
    print(db.select_all('CLIENTE'))

class DataBase:
    db_name:str
    
    def __init__(self, name:str):
        self.db_name = name
        Path(DATA_PATH + self.db_name).mkdir(parents=True, exist_ok=True)

    def return_table_path(self, table_name:str):
        return DATA_PATH + self.db_name + '/' + table_name + '.parquet'

    def create_table(self, table_name:str, columns:list[str]):
        data_archive_path = self.return_table_path(table_name)
        p = Path(data_archive_path)

        if p.exists():
            raise Exception('ERR-0001 - Table already exists')

        df = pd.DataFrame(columns=columns)
        df.to_parquet(data_archive_path, index=False)
    
    def drop_table(self, table_name:str):
        data_archive_path = self.return_table_path(table_name)
        
        try:
            os.remove(data_archive_path)
        except FileNotFoundError as e:
            raise Exception("ERR-0002 - Table doesn't exist")

    def insert(self, table_name:str, col_values:list):
        data_archive_path = self.return_table_path(table_name)

        df_existing = pd.read_parquet(data_archive_path)
        
        new_row = pd.DataFrame([col_values], columns=df_existing.columns)
        
        df_final = pd.concat([df_existing, new_row], ignore_index=True)
        df_final.to_parquet(data_archive_path, index=False)

    def delete(self, table_name:str, id:str):
        data_archive_path = self.return_table_path(table_name)

        df = pd.read_parquet(data_archive_path)
        
        df = df[df['ID'].astype(str) != str(id)]

        df.to_parquet(data_archive_path, index=False)

    def update(self, table_name:str, id:str, new_values:list):
        self.delete(table_name, id)
        self.insert(table_name, new_values)
    
    def select_all(self, table_name:str) -> pd.DataFrame:
        data_archive_path = self.return_table_path(table_name)
        
        if not Path(data_archive_path).exists():
            raise Exception("ERR-0002 - Table doesn't exist")
        
        return pd.read_parquet(data_archive_path)
    
if __name__ == '__main__':
    main()