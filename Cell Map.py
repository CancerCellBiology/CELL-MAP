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
import numpy as np
import umap
import matplotlib.pyplot as plt
import seaborn as sns
import os
import matplotlib

os.chdir('C:\\Cell Map')
file_name= 'Sanger cluster1'
n=15
method='correlation'
groups = ['kidney', 'colon', 'NSCLC adeno', 'NSCLC other', 'SCLC', 'stomach']
df = pd.read_excel(file_name+'.xlsx')
embedding = umap.UMAP(n_neighbors=n, min_dist=0.0, metric=method).fit_transform(df.drop(['subgroup', 'cellline'], axis=1))
file_name= 'Sanger uMap Fibrotic Clusterresult_n=15_dist=0.0_correlation'
df1 = pd.DataFrame(embedding)
df_out= pd.concat([df['cellline'], df['subgroup'], df1], axis=1)
df_out.set_index('cellline', inplace=True)
df_out.to_excel(file_name+'_UMAP.xlsx')
sns.set(style='white', context='notebook', rc={'figure.figsize':(14,10)})
custom_color=['#323232', '#9F6DAC','#86BAE5', '#FBC570','#8AC7B9', '#301D5B']
cmap= matplotlib.colors.ListedColormap(custom_color)
plt.scatter(df1[0], df1[1], c=df.subgroup, cmap=cmap, s=20)
df_xy= df_out.drop(['subgroup'], axis=1)
A549 = list(df_xy.loc['a549'])
H1299 = list(df_xy.loc['nci-h1299'])
Calu3 = list(df_xy.loc['calu-3'])
plt.colorbar(boundaries=np.arange(7)-0.5, ticks=np.arange(6)).set_ticklabels(groups)
plt.annotate('A549', A549, size=15)
plt.annotate('H1299', H1299, size=15)
plt.annotate('Calu-3', Calu3, size=15)
save_name=input('Figure name:')
plt.savefig(save_name+'.pdf')