import sys
import typing as t


def small_visited_twice(visited: t.Dict[str, int]) -> bool:
    for node, visits in visited.items():
        if node not in {"start", "end"} and node.islower():
            if visits >= 2:
                return True
    return False


def can_visit_adjacent(visited: t.Dict[str, int], adjacent: str) -> bool:
    if adjacent.isupper():
        return True
    elif adjacent == "start":
        return False
    elif small_visited_twice(visited):
        return visited[adjacent] < 1
    else:
        return visited[adjacent] < 2


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
        self.dfs(start, end, {node: 0 for node in self.graph.keys()}, path, paths)
        return paths
    
    def dfs(self, current: str, destination: str, visited: t.Dict[str, int], path: t.List[str], paths: t.List[t.List[str]] ) -> None:
        visited[current] += 1
        path.append(current)
        if current == destination:
            paths.append(path.copy())
        else:
            for adjacent in self.graph[current]:
                if can_visit_adjacent(visited, adjacent):
                    self.dfs(adjacent, destination, visited, path, paths)
        path.pop()
        visited[current] -= 1


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
