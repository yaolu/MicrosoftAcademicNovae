import igraph

class AuthorGraph:
  _graph = None;
  _dict = {};


  def load_author_net(self, filename):
    with open(filename) as f:
      self._graph = igraph.Graph.Read_Ncol(f ,directed=False)

  def load_id_citenum(self, filename):
    with open(filename) as f:
      for line in f:
          (key, val) = line.split()
          if key != None:
            self._dict[key] = val

  def get_neighbor_citenum(self, author):
    neighbor = list(set(self._graph.vs[self._graph.neighbors(author)]["name"]))
    neighbor.append(author)
    return {author:self._dict[author] for author in neighbor}


def main():
  ag = AuthorGraph()
  ag.load_author_net('author_net.txt')
  ag.load_id_citenum('id_citenum.txt')
  f=open('id_citenum.txt').readlines()
  all_node = [elem.strip('\n').split('\t')[0] for elem in f]
  for elem in all_node:
  	print ag.get_neighbor_citenum(elem)

if __name__ == '__main__':
  main()