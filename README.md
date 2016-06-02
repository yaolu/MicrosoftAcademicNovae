#Microsoft Academic Supernovae

这个项目将会基于微软学术图谱，通过对学者的各类数据的分析，来尝试评价一个年轻学者的发展潜力，作为一种新的学术评价指标。

##Dataset
我们定义一个学者第一次发表论文的年份为他的学术生涯的开始。在我们数据集中，我们选取1995-2000年5年的时间窗口内的研究员作为样本，以2005年数据作为基准（即学术生涯后开始5-10年的数据），建立关系网络和学术质量评价网络。

PS: 以下所有数据，都是截止2005年的数据 

- AuId 对应的 每一篇 paperId 在 2005年 的 引用量
- AuId 对应的 每一篇 paperId 的 发表会议
- 截止到 2005年 每个AuId 的 合作AuId 以及 合作次数 
- 截止到 2005年 网络中 每个AuId 的 总被引用次数


##Sub-network Evaluation

### Academic Cooperation Network
>
THREE BASELINE METHODS

- Page Rank
- GLODA(Global Outlier Detection Algorithm)
- DNODA(Dircet Neighborhood Detection Algorithm)


### Academic Quality Network

