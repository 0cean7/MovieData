# Script By Christopher Gordon
import numpy as np
import pandas as pd

df = pd.read_csv('movies.csv')
pd.options.display.width = None
pd.options.display.max_columns = None
pd.set_option('display.max_rows', 3000)
pd.set_option('display.max_columns', 3000)


# function returns 1 if genre is in that row, 0 if not
def genre_column(row, genre):
    if genre in row['GENRE']:
        return 1
    return 0


# function returns unique list of a unique genre's from the genre column
def genre_list():
    unique_list = []
    df['GENRE'] = df.GENRE.str.replace(' ', '')
    df['GENRE'] = df.GENRE.str.replace('\n', '')
    for index, row in df.iterrows():
        hold = row['GENRE'].split(',')
        for x in hold:
            if x not in unique_list:
                unique_list.append(x)
    unique_list.remove('')
    return unique_list


# main program
def process():
    # Splitting start and end dates
    df['Start_Date'] = df.YEAR.str.split('–', expand=True)[0]
    df['End_Date'] = df.YEAR.str.split('–', expand=True)[1]
    # clean columns so only the digits remain
    df['Start_Date'] = df['Start_Date'].str.replace(r'\D+', '', regex=True).astype('str')
    df['End_Date'] = df['End_Date'].str.replace(r'\D+', '', regex=True).astype('str')
    # fills empty rows in end_date with NaN, so it is standardized
    df['Start_Date'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
    df['Start_Date'].fillna(value=np.nan, inplace=True)
    df['Start_Date'].replace('None', np.nan, inplace=True)
    df['End_Date'].replace(r'^\s*$', np.nan, regex=True, inplace=True)
    df['End_Date'].fillna(value=np.nan, inplace=True)
    df['End_Date'].replace('None', np.nan, inplace=True)
    df.GENRE = df.GENRE.fillna('')  # so we can iterate through GENRE
    glist = genre_list()
    for y in glist:
        df[y] = df.apply(lambda row: genre_column(row, y), axis=1)
    # commented out lines were for debugging purposes
    # print(glist)
    # print(df.head(300))
    df.to_csv('final_movies.csv', encoding='utf-8', index=False)


if __name__ == '__main__':
    process()
