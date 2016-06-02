import igraph

class apiDataProcess:

	def authorlist_to_pair(self,filename):
		'''
		File format: AuId1\tAuId2\t....AuIdx\n
		Return: [[AuId,AuId],[AuId,AuId],...,[AuId,AuId]]
		'''
		data = []
		with open(filename) as fs:
			for line in fs:
				data.append(line.strip('\n').split('\t'))
		pairs = []
		for single_paper in data:
			for single_author in single_paper[1:]:
				pairs.append([single_paper[0],single_author])
		return pairs



class AuthorGraph:
	_graph = None;
	_dict = {};

	def pair_to_net(self,filename):
		with open(filename) as fs:
			self._graph = igraph.Graph.Read_Ncol(fs ,directed=False)
		#print self._graph
	

	#def 



if __name__ == '__main__':
	a=apiDataProcess()
	ss = a.authorlist_to_pair('../data/AuId_AuId.txt')
	
	print len(ss)

	#ag = AuthorGraph()
	#ag.pair_to_net('../data/ncols.txt')




