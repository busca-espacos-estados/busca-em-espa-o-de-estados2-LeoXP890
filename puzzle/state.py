from __future__ import annotations
from typing import List, Optional, Tuple


GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)

# Movimentos possíveis: índice do vizinho por posição do blank
# O blank pode se mover para: cima, baixo, esquerda, direita
# Grade 3x3:
#  0 1 2
#  3 4 5
#  6 7 8
MOVES = {
    0: [1, 3],
    1: [0, 2, 4],
    2: [1, 5],
    3: [0, 4, 6],
    4: [1, 3, 5, 7],
    5: [2, 4, 8],
    6: [3, 7],
    7: [4, 6, 8],
    8: [5, 7],
}

def _action_name(blank: int, target: int) -> str:
    """Retorna o nome da ação: direção em que o ESPAÇO se move."""
    diff = target - blank
    if diff == -3: return "UP"
    if diff ==  3: return "DOWN"
    if diff == -1: return "LEFT"
    if diff ==  1: return "RIGHT"
    return "?"


class State:
    """Representa um estado do 8-puzzle como tupla imutável de 9 inteiros (0 = espaço vazio)."""

    def __init__(self, tiles: Tuple[int, ...], parent: Optional["State"] = None, action: Optional[str] = None, cost: int = 0):
        if len(tiles) != 9 or set(tiles) != set(range(9)):
            raise ValueError("Estado inválido: deve conter exatamente os valores 0-8.")
        self.tiles = tiles
        self.parent = parent
        self.action = action
        self.cost = cost

    @property
    def is_goal(self) -> bool:
        return self.tiles == GOAL_STATE

    @property
    def blank_index(self) -> int:
        return self.tiles.index(0)

    def neighbors(self) -> List["State"]:
        """Retorna os estados filhos válidos a partir deste estado."""
        blank = self.blank_index
        result = []
        for target in MOVES[blank]:
            new_tiles = list(self.tiles)
            new_tiles[blank], new_tiles[target] = new_tiles[target], new_tiles[blank]
            action = _action_name(blank, target)
            result.append(State(tuple(new_tiles), parent=self, action=action, cost=self.cost + 1))
        return result

    def path(self) -> List["State"]:
        """Retorna a sequência de estados do estado inicial até este."""
        node, sequence = self, []
        while node is not None:
            sequence.append(node)
            node = node.parent
        return list(reversed(sequence))

    def actions(self) -> List[str]:
        """Retorna a sequência de ações do estado inicial até este."""
        return [s.action for s in self.path() if s.action is not None]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, State) and self.tiles == other.tiles

    def __hash__(self) -> int:
        return hash(self.tiles)

    def __lt__(self, other: "State") -> bool:
        return self.cost < other.cost

    def __repr__(self) -> str:
        t = self.tiles
        return (
            f"+-------+\n"
            f"| {t[0]} {t[1]} {t[2]} |\n"
            f"| {t[3]} {t[4]} {t[5]} |\n"
            f"| {t[6]} {t[7]} {t[8]} |\n"
            f"+-------+"
        ).replace("0", " ")
