from itertools import combinations

pair_bigram=pd.DataFrame(data=[i[j:j+2] for i in to_noun(all_title,slice(len(all_title))) for j in range(len(i)-1)],columns=['item1','item2'])
dist=FreqDist(pair_bigram['item1']+'-'+pair_bigram['item2'])
pair_bigram['n']=pair.apply(lambda x: dist[x['item1']+'-'+x['item2']],axis=1)
pair_bigram=pair_bigram[pair_bigram.n>5]
pair_bigram

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
G.add_edges_from(pair_bigram[['item1','item2']].to_numpy())

pr=nx.pagerank(G)
nsize=np.array([v for v in pr.values()])
nsize=4000*(nsize-min(nsize))/(max(nsize)-min(nsize))
#pos = nx.spring_layout(G,k=0.15,iterations=20)
pos = graphviz_layout(G)
nx.draw_networkx(G,font_family='Malgun Gothic',font_color='white',font_size=14,width=3, pos=pos,with_labels=True,edge_vmax=10e-30, node_color=list(pr.values()),
                 node_size=nsize,alpha=0.7,edge_color='.5',cmap=sns.color_palette("Spectral", as_cmap=True))
#nx.draw_networkx_edge_labels(G, pos)
plt.tight_layout()
plt.show()
