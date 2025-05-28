from collections import deque

graph = {
    'S': ['A', 'B'],
    'A': ['C', 'D'],
    'B': ['E', 'F'],
    'C': ['G'],
    'D': ['H', 'I'],
    'E': ['J'],
    'F': ['K', 'L'],
    'G': ['M'],
    'H': [],
    'I': ['N'],
    'J': ['O'],
    'K': [],
    'L': [],
    'M': [],
    'N': ['P'],
    'O': ['Q'],
    'P': ['R'],
    'Q': [],
    'R': ['T'],
    'T': [],
    'Z': []
}


heuristic = {
    'S': 9,  'A': 8,  'B': 8,
    'C': 7,  'D': 6,  'E': 6,  'F': 6,
    'G': 6,  'H': 5,  'I': 4,  'J': 5,
    'K': 5,  'L': 4,  'M': 4,  'N': 3,
    'O': 4,  'P': 2,  'Q': 2,  'R': 1,
    'T': 0, 'Z': 0
}

def beam_search(start, goal, beam_width):
    queue = deque([[start]])
    step = 1

    while queue:
        all_paths = []
        while queue:
            path = queue.popleft()
            node = path[-1]

            if node == goal:
                print(f"Objetivo '{goal}' encontrado! Caminho: {path}")
                return path

            for neighbor in graph.get(node, []):
                new_path = path + [neighbor]
                all_paths.append(new_path)

        # Ordena todos os caminhos
        all_paths.sort(key=lambda p: heuristic.get(p[-1], float('inf')))

        # Mantém apenas os melhores k caminhos
        queue = deque(all_paths[:beam_width])
        step += 1

    print("Nenhum caminho encontrado até o objetivo.")
    return None

beam_search('S', 'T', beam_width=2)