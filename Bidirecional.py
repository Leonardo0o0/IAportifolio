from collections import deque

def bidirectional_search(graph, start, goal):

    if start == goal:
        return [start]

    front_paths = {start: [start]}
    back_paths = {goal: [goal]}

    front_queue = deque([start])
    back_queue = deque([goal])

    while front_queue and back_queue:

        current_front = front_queue.popleft()
        for neighbor in graph.get(current_front, []):
            if neighbor not in front_paths:
                front_paths[neighbor] = front_paths[current_front] + [neighbor]
                front_queue.append(neighbor)
                if neighbor in back_paths:
                    # Encontrou interseção
                    return front_paths[neighbor] + back_paths[neighbor][::-1][1:]

        current_back = back_queue.popleft()
        for neighbor in graph.get(current_back, []):
            if neighbor not in back_paths:
                back_paths[neighbor] = back_paths[current_back] + [neighbor]
                back_queue.append(neighbor)
                if neighbor in front_paths:
                    # Encontrou interseção
                    return front_paths[neighbor] + back_paths[neighbor][::-1][1:]

    return None  # Caminho não encontrado


graph = {
    'A': ['B', 'C', 'D'],
    'B': ['D','E','A'],
    'C': ['F','G','A'],
    'D': ['H','B','A'],
    'E': ['I','B'],
    'F': ['J','C'],
    'G': ['J','C'],
    'H':['J','D'],
    'I':['J','E','K'],
    'J':['I','F','G','H','K'],
    'K':['I','J']
}

path = bidirectional_search(graph, 'A', 'K')

if path:
    print(f"Caminho encontrado: {' -> '.join(caminho)}")
else:
    print("Nenhum caminho encontrado.")