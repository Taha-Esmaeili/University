import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt

# Read dataset
initial_df = pd.read_csv('Dry_Bean.csv')

# Drop categorical feature
df = initial_df.drop('Class',axis=1,inplace=False)

# Get corr table
corr_matrix = df.corr()

# Filter table
selected = (corr_matrix>0.8)&(corr_matrix!=1)

# Get filtered rows
high_corr_feature=corr_matrix[selected]

# Create final table
high_corr_feature_df=high_corr_feature.reset_index().rename(columns={'index':'feature_1'})
high_corr_feat_tidy=pd.melt(high_corr_feature_df,id_vars=['feature_1'],var_name='feature_2',value_name='correlation_coefficient')

# Plotting the final corr matrix
sns.heatmap(data = corr_matrix)
plt.show()
