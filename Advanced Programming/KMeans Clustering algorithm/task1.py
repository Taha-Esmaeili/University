import pandas as pd 

# Read dataset into python file
df = pd.read_csv('Dry_Bean.csv')

# Calculate summation row
sum_row = df.sum()

# Drop categorical feature
sum_row = sum_row.drop('Class')

# Get statistical parameters
describe_df = df.describe()

# Add summation row to the statistical table
describe_df.loc['sum'] = sum_row

print(describe_df)
