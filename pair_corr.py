from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

vec = TfidfVectorizer()
vector_pos_review = vec.fit_transform([' '.join(i) for i in to_noun(all_title,slice(10))])

vector_pos_review
A = vector_pos_review.toarray()

A=A.transpose()
pd.DataFrame(A)
A_sparse = sparse.csr_matrix(A) # A를 다시 희소행렬로 변환
similarities_sparse = cosine_similarity(A_sparse, dense_output=False)

item_dict=dict(zip(vec.vocabulary_.values(),vec.vocabulary_.keys()))

pair_corr=pd.DataFrame(similarities_sparse.todok().keys(),columns=['item1','item2'])
pair_corr['correlation']=similarities_sparse.todok().values()
pair_corr['item1']=pair_corr.apply(lambda x: item_dict[x['item1']],axis=1)
pair_corr['item2']=pair_corr.apply(lambda x: item_dict[x['item2']],axis=1)
pair_corr=pair_corr[(pair_corr.correlation>0.7) &(pair_corr.correlation<0.99999999)]
pair_corr

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
G.add_edges_from(pare[['item1','item2']].to_numpy())

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
