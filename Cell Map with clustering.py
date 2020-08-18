# -*- coding: utf-8 -*-
"""
Code developed in the laboratory of Cancer Cell Biology,
Engelhardt Institute of Molecular Biology, Moscow, Russia.
Not for commercial use.
If you have any questions about the code or its use contact:
lebedevtd@gmai.com
vr.elmira@gmail.com 
"""

import pandas as pd
import umap
import matplotlib.pyplot as plt
import seaborn as sns
import hdbscan
import os

os.chdir('C:\\Cell Map')
file_name= 'Sanger cluster1'
n=15
method='correlation'
groups = ['kidney', 'colon', 'NSCLC adeno', 'NSCLC other', 'SCLC', 'stomach']
df = pd.read_excel(file_name+'.xlsx')
embedding = umap.UMAP(n_neighbors=n, min_dist=0.0, metric=method).fit_transform(df.drop(['subgroup', 'cellline'], axis=1))
df1 = pd.DataFrame(embedding)
hdbscan_labels = hdbscan.HDBSCAN(min_samples=10, min_cluster_size=20).fit_predict(df1)
df1['cluster'] = hdbscan_labels
df_out= pd.concat([df['cellline'], df['subgroup'], df1], axis=1)
df_out.set_index('cellline', inplace=True)
df_out.to_excel(file_name+'_UMAP_clustering.xlsx')
sns.set(style='white', context='notebook', rc={'figure.figsize':(14,10)})
custom_color=['#323232', '#9F6DAC','#86BAE5', '#FBC570','#8AC7B9', '#301D5B']
custom_shapes= ['o', 'v', 's', '*']
for i in df_out.index:
    color=custom_color[df_out.at[i,'subgroup']]
    shape=custom_shapes[df_out.at[i,'cluster']]
    plt.scatter(df_out.at[i,0], df_out.at[i,1], c=color, marker=shape, s=40)
df_xy= df_out.drop(['subgroup', 'cluster'], axis=1)
A549 = list(df_xy.loc['a549'])
H1299 = list(df_xy.loc['nci-h1299'])
Calu3 = list(df_xy.loc['calu-3'])
plt.annotate('A549', A549, size=15)
plt.annotate('H1299', H1299, size=15)
plt.annotate('Calu-3', Calu3, size=15)
save_name=input('Figure name:')
plt.savefig(save_name+'.pdf')

