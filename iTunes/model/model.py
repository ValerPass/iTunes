import copy
import networkx as nx

from database.DAO import DAO

class Model:
    def __init__(self):
        self.graph = nx.Graph()
        self._idMap = {}

    def durataTot(self, setOfNodes):
        dtot = 0
        for n in setOfNodes:
            dtot += n.totD
        return toMinutes(dtot)

    def buildGraph(self, d):
        self.graph.clear()
        self.graph.add_nodes_from(DAO.getAlbums(toMillisec(d)))
        self._idMap = {a.AlbumId : a for a in self.graph.nodes}
        edges = DAO.getEdges(self._idMap)
        self.graph.add_edges_from(edges)


    def getConnessaDetails(self, v0):
        conn = nx.node_connected_component(self.graph, v0)
        durataTOT = 0
        for album in conn:
            durataTOT += toMinutes(album.totD)

        return len(conn), durataTOT

    def getGraphSize(self):
        return len(self.graph.nodes), len(self.graph.edges)

    def getNodes(self):
        return list(self.graph.nodes)

def toMillisec(d):
    return d*60*1000

def toMinutes(d):
    return d/1000/60