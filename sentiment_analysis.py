class sentiment_sentence_analysis:
    def __init__(self,sentiment_dic_path,title_data,slice_index:slice):
        self.sentiment_dic=pd.read_csv(sentiment_dic_path)
        
        stock_data=pd.DataFrame(data=to_noun(title_data,slice_index),index=np.concatenate(title_data[slice_index]))
        stock_data=stock_data.stack()
        self.stock=pd.DataFrame(stock_data,columns=['word'])
        self.stock['sentence']=[i[0] for i in self.stock.index]
        self.stock.index=range(len(self.stock.index))
        self._stock_sentiment_match()
    
    def _stock_sentiment_match(self):
        self.stock_sentiment=pd.merge(self.stock,self.sentiment_dic,on='word',how='left').fillna(0)
        self.stock_sentiment['sentiment']=self.stock_sentiment.apply(lambda x: 'pos' if x['polarity']>1 else 'neg' if x['polarity']<-1 else 'neu',axis=1)
        word_sentiment=self.stock_sentiment.groupby(['sentiment','word']).size().sort_values(ascending=False)
        self.word_sentiment=word_sentiment.reset_index(name='n')
        
    def sentiment_bar_plot(self,title):
        self._stock_sentiment_match()
        sns.set_style("darkgrid", {'font.family':'Malgun Gothic',"axes.facecolor": ".40"})
        plt.figure(figsize=(15,10))
        plt.suptitle(title,fontsize=20)
        plt.subplot(1,2,1)
        plt.title('pos')
        sns.barplot(data=self.word_sentiment[self.word_sentiment.sentiment=='pos'],x='n',y='word')
        plt.subplot(1,2,2)
        plt.title('neg')
        sns.barplot(data=self.word_sentiment[self.word_sentiment.sentiment=='neg'],x='n',y='word')
        plt.show()

    
st=sentiment_sentence_analysis('knu_sentiment_lexicon.csv',all_title,slice(len(all_title)))

st.sentiment_bar_plot('before')
st.sentiment_dic=pd.concat([st.sentiment_dic,pd.DataFrame(data=[['강세',2],['증가',2],['급등세',2],['공매도',-2],['상승',2],['하락',-2],['파업',-1],['노조',-1],['구조조정',-2],['껑충',2],['저평가',1],['갑질',-1],['반토막',-2]],columns=['word','polarity'])])
st.sentiment_bar_plot('after')
plt.figure(figsize=(10,5))
st.stock_sentiment.groupby('sentiment').size().plot.bar(logy=True,colormap=sns.color_palette("Spectral", as_cmap=True))

