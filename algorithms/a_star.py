import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

GOAL_POSITIONS = {val: idx for idx, val in enumerate((1, 2, 3, 4, 5, 6, 7, 8, 0))}


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        """Distância de Manhattan: soma das distâncias de cada peça à sua posição objetivo."""
        distance = 0
        for idx, val in enumerate(state.tiles):
            if val == 0:
                continue
            goal_idx = GOAL_POSITIONS[val]
            distance += abs(idx // 3 - goal_idx // 3) + abs(idx % 3 - goal_idx % 3)
        return distance

    def search(self, initial: State) -> SearchResult:
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        # heap: (f, contador, estado)  — contador desempata quando f é igual
        counter = 0
        heap = [(self.heuristic(initial), counter, initial)]
        explored = {}  # tiles -> menor g encontrado

        while heap:
            max_frontier_size = max(max_frontier_size, len(heap))
            f, _, node = heapq.heappop(heap)

            if node.is_goal:
                return SearchResult(
                    solution=node,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=node.cost,
                )

            # Descarta se já expandimos esse estado com custo menor
            if node.tiles in explored and explored[node.tiles] < node.cost:
                continue

            explored[node.tiles] = node.cost
            nodes_expanded += 1

            for child in node.neighbors():
                nodes_generated += 1
                if child.tiles in explored and explored[child.tiles] <= child.cost:
                    continue
                counter += 1
                h = self.heuristic(child)
                heapq.heappush(heap, (child.cost + h, counter, child))

        return SearchResult(solution=None, nodes_expanded=nodes_expanded, nodes_generated=nodes_generated, max_frontier_size=max_frontier_size)
