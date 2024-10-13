# pylint: disable=trailing-whitespace, missing-function-docstring, wrong-import-order
import pandas as pd
import re
import argparse

def clean_data(country_code="PT"):
    # Load the data
    df = pd.read_csv('life_expectancy/data/eu_life_expectancy_raw.tsv', sep='\t')
    print("After loading:", df.shape)

    # Unpivot to long format
    df = df.melt(id_vars=['unit,sex,age,geo\\time'], var_name='year', value_name='value')
    print("After melting:", df.shape)

    # Split the composed column into separate columns
    df[['unit', 'sex', 'age', 'region']] = df['unit,sex,age,geo\\time'].str.split(',', expand=True)
    df.drop(columns=['unit,sex,age,geo\\time'], inplace=True)
    print("After splitting:", df.shape)

    # Convert `year` to integer
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    print("After year conversion:", df.shape)

    # Remove non-numeric characters in `value`, keeping only numbers and decimals
    df['value'] = df['value'].apply(lambda x: re.sub(r'[^0-9.]', '', str(x)))

    # Convert `value` to numeric (float) after cleaning
    df['value'] = pd.to_numeric(df['value'], errors='coerce')

    # Drop rows where `value` became `NaN` after removing non-numeric characters
    df.dropna(subset=['value'], inplace=True)   
    print("After cleaning value column:", df.shape)

    # Filter for the specified region
    df = df[df['region'] == country_code]
    print("After region filtering:", df.shape)

    # Enforce correct column order immediately before saving
    column_order = ['unit', 'sex', 'age', 'region', 'year', 'value']
    df = df[column_order]  # This ensures the correct order is saved

    # Save the cleaned data to a CSV file
    df.to_csv('life_expectancy/data/pt_life_expectancy.csv', index=False)

if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser(description="Clean life expectancy data for a specific country")
    parser.add_argument('--country', default='PT', help='Country code to filter by (default: PT)')
    args = parser.parse_args()
    clean_data(args.country)
