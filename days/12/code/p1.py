import sys
import typing as t


class Digraph(object):
    def __init__(self, edges: t.List[t.Tuple[str, str]]) -> None:
        self.graph: t.Dict[str, t.List[str]] = {}
        for anode, bnode in edges:
            if anode not in self.graph:
                self.graph[anode] = []
            if bnode not in self.graph:
                self.graph[bnode] = []
            self.graph[anode].append(bnode)
            self.graph[bnode].append(anode)
    
    def __str__(self) -> str:
        return str(self.graph)
    
    def travel(self, start: str = "start", end: str = "end") -> t.List[t.List[str]]:
        paths: t.List[t.List[str]] = []
        path: t.List[str] = []
        self.dfs(start, end, {node: False for node in self.graph.keys()}, path, paths)
        return paths
    
    def dfs(self, current: str, destination: str, visited: t.Dict[str, bool], path: t.List[str], paths: t.List[t.List[str]] ) -> None:
        visited[current] = True
        path.append(current)
        if current == destination:
            paths.append(path.copy())
        else:
            for adjacent in self.graph[current]:
                if not visited[adjacent] or adjacent.isupper():
                    self.dfs(adjacent, destination, visited, path, paths)
        path.pop()
        visited[current] = False


def main(filepath: str) -> int:
    fobj = open(filepath, "r")
    edges = []
    for line in fobj:
        edges.append(line.strip().split("-"))
    digraph = Digraph(edges)
    paths = digraph.travel()
    print(len(paths))
    return 0


main(sys.argv[1])
