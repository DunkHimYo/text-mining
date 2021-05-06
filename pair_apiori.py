import pandas as pd
apiori_result=(list(apriori(to_noun(all_title,slice(len(all_title))), min_support=0.003)))
pair_apiori=pd.DataFrame(apiori_result)
pair_apiori['len']=pair_apiori['items'].apply(lambda x:len(x))
pair_apiori=pair_apiori[(pair_apiori['len']>1)&(pair_apiori['len']<3)]

from networkx.drawing.nx_agraph import graphviz_layout
from networkx.drawing.layout import rescale_layout
import networkx as nx
import matplotlib.pyplot as plt
import platform
import numpy as np
from itertools import permutations
plt.rcParams["figure.figsize"] = (28,28)

# 글씨 선명하게 출력하는 설정
%config InlineBackend.figure_format = 'retina'

G=nx.Graph()

ar=list(pair_apiori['items'].apply(lambda x: [i for i in x]));


G.add_edges_from(list(ar))
pr=nx.pagerank(G)
nsize=np.array([v for v in pr.values()])
nsize=4000*(nsize-min(nsize))/(max(nsize)-min(nsize))
pos = graphviz_layout(G,prog='twopi')
nx.draw_networkx(G,font_family='Malgun Gothic',font_color='white',font_size=14,width=3, pos=pos,with_labels=True,edge_vmax=10e-30, 
                 node_color=list(pr.values()),node_size=nsize,alpha=0.7,edge_color='.5',cmap=sns.color_palette("Spectral", as_cmap=True))
#nx.draw_networkx_edge_labels(G, pos)

plt.tight_layout()
plt.show()
