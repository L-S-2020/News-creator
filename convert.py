import pandas

# Read the Excel file
df = pandas.read_excel('output.xlsx')

# Write the Parquet file
df.to_csv('my_data.csv')