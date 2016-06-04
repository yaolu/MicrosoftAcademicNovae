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

	def all_author_list(self,filename):
		authorlist = []
		with open(filename,'r') as fs:
			for line in fs:
				authorlist.append(line.strip('\n'))
		return authorlist



class AuthorGraph:
	_graph = None;
	_dict = {};

	def pair_to_net(self,filename):
		with open(filename,'r') as fs:
			self._graph = igraph.Graph.Read_Ncol(fs ,directed=False)

	def load_id_citenum(self,filename):
		with open(filename,'r') as fs:
			for line in fs:
				(AuId,cite_num,pub_year) = line.split()
				if AuId != None:
					self._dict[AuId] = int(cite_num)

	def get_id_citenum(self,AuId):
		try:
			neighbor = list(set(self._graph.vs[self._graph.neighbors(AuId)]["name"]))

			neighbor.append(AuId)
			neighbors_cite_map = {}
			for author in neighbor:
				try:
					neighbors_cite_map.update({author:self._dict[author]})
				except KeyError, e:
					neighbors_cite_map.update({author:None})
					#pass
			return neighbors_cite_map
		except ValueError as v:
			return None


		#[self._graph.neighbors(AuId)]["name"]))
		


if __name__ == '__main__':
	api=apiDataProcess()
	authors_id = api.all_author_list('../data/all_author.txt')
	
	#print len(ss)

	ag = AuthorGraph()
	ag.pair_to_net('../data/ncols.txt')
	ag.load_id_citenum('../data/AuId_CC_Y.txt')
	for author in authors_id:
		author_neigh_dict = ag.get_id_citenum(author)
		neigh_count = 0
		neigh_val = 0
		if author_neigh_dict != None:
			if author_neigh_dict[author] != None:
				for key in author_neigh_dict:
					if author_neigh_dict[key] != None:
						neigh_count += 1
						neigh_val += author_neigh_dict[key] 
				local_network_outlier = (1.0*neigh_val/neigh_count)/(1+author_neigh_dict[author])
				with open('../result/loss.txt','a+') as fs:
					fs.write(author+'\t'+str(local_network_outlier)+'\n')


	#print ag.get_id_citenum('2105607418')
	#print ag.get_id_citenum('2137977702')
	#ag.pair_to_net('../data/ncols.txt')




