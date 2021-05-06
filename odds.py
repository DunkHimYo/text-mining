class odds_compare():
    def __init__(self,title_data,slice_index1, slice_index2):
        
        fr_10 = FreqDist(np.hstack(to_noun(title_data,slice_index1)))
        fr_20 = FreqDist(np.hstack(to_noun(title_data,slice_index2)))

        noun_10 = pd.DataFrame(data=np.array([list(fr_10.keys()), list(fr_10.values())]).T, columns=['word', 'n'])
        noun_10['page']='a'
        noun_20 = pd.DataFrame(data=np.array([list(fr_20.keys()), list(fr_20.values())]).T, columns=['word', 'n'])
        noun_20['page']='b'
        data=pd.concat([noun_10,noun_20])
        data=data.pivot(index='word', columns='page', values='n').fillna(0)
        data['a']=data['a'].astype(int)
        data['b']=data['b'].astype(int)
        
        data['a_ratio']=data['a']+1/sum(data['a']+1)
        data['b_ratio']=data['b']+1/sum(data['b']+1)
        data['odds_ratio']=np.log(data['a_ratio']/data['b_ratio'])
        data=data.sort_values(by=['odds_ratio'], ascending=False)
        self.data=data.reset_index()
        self.a=self.data[self.data['odds_ratio']>0]
        self.b=self.data[self.data['odds_ratio']<0]
        self.b['odds_ratio']=self.b['odds_ratio']*-1
    
    def compare_show(self):
        sns.set_palette("hls", 8)
        plt.figure(figsize=(15,10))
        plt.subplot(1,2,1)
        sns.barplot(data=self.a[:10],x='odds_ratio',y='word')
        plt.subplot(1,2,2)
        sns.barplot(data=self.b.sort_values(['odds_ratio'],ascending=False)[:10],x='odds_ratio',y='word')
        plt.show()
        
odds=odds_compare(all_title,slice(0,50),slice(50,100))
print(odds.data)
odds.compare_show()
