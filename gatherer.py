import random
from collections import deque

# Tamanho do mundo
GRID_SIZE = 5

# Representações do mundo
EMPTY = '.'
ROBOT = 'R'
RESOURCE = 'O'
PIT = 'X'
LADDER = 'H'
CLEAR_PIT = 'C' 

class World:
    def __init__(self, size):
        self.size = size
        self.grid = [[EMPTY for _ in range(size)] for _ in range(size)]

        for _ in range(4):
            x, y = self.random_empty_cell()
            self.grid[y][x] = PIT

        for _ in range(4):
            x, y = self.random_empty_cell()
            self.grid[y][x] = RESOURCE
            
        x, y = self.random_empty_cell()
        self.grid[y][x] = LADDER

    def random_empty_cell(self):
        while True:
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)
            if (x, y) not in [(0,0), (0,1), (1,0)] and self.grid[y][x] == EMPTY:
                return x, y

    def display(self, agent):
        print("\nMapa de Raciocínio do Agente:")
        for y in range(self.size):
            row = ''
            for x in range(self.size):
                pos = (x, y)
                if pos == agent.pos:
                    row += 'R '
                elif pos == (0,0):
                    row += 'E '
                elif pos in agent.kb['visited']:
                    row += self.grid[y][x] + ' '
                elif pos in agent.kb['potential_pits']:
                    row += 'D '
                elif pos in agent.kb['safe']:
                    row += 'S '
                else:
                    row += '? '
            print(row)

    def get_cell(self, pos):
        return self.grid[pos[1]][pos[0]]
        
    def get_adjacent_cells(self, pos):
        x, y = pos
        adjacent = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                adjacent.append((nx, ny))
        return adjacent

    def sense_danger(self, pos):
        for adj_pos in self.get_adjacent_cells(pos):
            if self.get_cell(adj_pos) == PIT:
                return True
        return False

    def make_pit_safe(self, pos):
        original_content = self.get_cell(pos)
        self.grid[pos[1]][pos[0]] = CLEAR_PIT
        return original_content == PIT

class LogicalAgent:
    def __init__(self, world):
        self.world = world
        self.world_size = world.size
        self.pos = (0, 0)
        self.energy = 30
        self.resources_collected = 0
        self.has_ladder = False
        
        self.kb = {
            'visited': set(),
            'safe': {(0, 0)},
            'potential_pits': set()
        }

    def update_kb(self):
        self.kb['visited'].add(self.pos)
        is_danger = self.world.sense_danger(self.pos)
        
        if not is_danger:
            for adj_pos in self.world.get_adjacent_cells(self.pos):
                if adj_pos not in self.kb['safe']:
                    self.kb['safe'].add(adj_pos)
                    self.kb['potential_pits'].discard(adj_pos)
        else:
            print("⚠️ Alerta: perigo próximo!")
            for adj_pos in self.world.get_adjacent_cells(self.pos):
                if adj_pos not in self.kb['visited'] and adj_pos not in self.kb['safe']:
                    self.kb['potential_pits'].add(adj_pos)

    def bfs(self, start, goals):
        if start in goals: return [start]
        queue = deque([[start]])
        seen = {start}
        
        while queue:
            path = queue.popleft()
            x, y = path[-1]
            
            for adj_pos in self.world.get_adjacent_cells((x, y)):
                if adj_pos in self.kb['safe'] and adj_pos not in seen:
                    new_path = list(path)
                    new_path.append(adj_pos)
                    if adj_pos in goals: return new_path
                    queue.append(new_path)
                    seen.add(adj_pos)
        return None

    def choose_action(self):
        path_home = self.bfs(self.pos, {(0, 0)})
        cost_to_return = len(path_home) - 1 if path_home else float('inf')
        
        safety_margin = 3 

        if self.energy <= cost_to_return + safety_margin:
            print(f"⚠️ Energia baixa ({self.energy})! Custo para voltar: {cost_to_return}. Iniciando retorno à base.")
            return ('return_home', (0, 0))

        if self.has_ladder:
            for adj_pos in self.world.get_adjacent_cells(self.pos):
                if adj_pos in self.kb['potential_pits']:
                    return ('use_ladder', adj_pos)

        unvisited_safe_goals = self.kb['safe'] - self.kb['visited']
        if unvisited_safe_goals:
            path_to_goal = self.bfs(self.pos, unvisited_safe_goals)
            if path_to_goal and len(path_to_goal) > 1:
                return ('move', path_to_goal[1])

        return ('return_home', (0, 0))

    def execute_move(self, next_pos):
        self.pos = next_pos
        self.energy -= 1
        print(f"Movendo para {self.pos}...")

        cell_content = self.world.get_cell(self.pos)
        if cell_content == RESOURCE:
            self.resources_collected += 1
            self.world.grid[self.pos[1]][self.pos[0]] = EMPTY
            print(f"💎 Recurso coletado! Total: {self.resources_collected}")
        elif cell_content == LADDER:
            self.has_ladder = True
            self.world.grid[self.pos[1]][self.pos[0]] = EMPTY
            print("🪜 Escada encontrada!")
        elif cell_content == CLEAR_PIT:
            self.energy += 10
            print(f"🌟 Recompensa! Entrou em poço seguro. Energia +10. Total: {self.energy}")
        
        return self.energy > 0

def display_final_results(agent, reason):
    # --- Exibe o resumo final da missão do agente ---
    print("\n" + "="*25)
    print("--- MISSÃO FINALIZADA ---")
    print(f"Razão: {reason}")
    print("-" * 25)
    print(f"Recursos Coletados: {agent.resources_collected} de 4")
    print(f"Energia Restante: {agent.energy}")
    print(f"Posição Final: {agent.pos}")

    if agent.pos == (0,0):
        print("Retorno à Base: SUCESSO")
    else:
        print("Retorno à Base: FALHA")

    if agent.resources_collected >= 4:
        print("Status da Missão: SUCESSO!")
    else:
        print("Status da Missão: INCOMPLETA")
    print("="*25)

# --- Execução Principal ---
def run_simulation():
    world = World(GRID_SIZE)
    agent = LogicalAgent(world)
    final_reason = "Limite de passos atingido."

    for step in range(50): 
        world.display(agent)
        print(f"Passo: {step+1} | Posição: {agent.pos} | Energia: {agent.energy} | Recursos: {agent.resources_collected} | Escada: {agent.has_ladder}")
        
        agent.update_kb()
        
        action_type, target = agent.choose_action()

        if action_type == 'move':
            if not agent.execute_move(target):
                final_reason = "A energia acabou durante o movimento!"
                break
        elif action_type == 'use_ladder':
            agent.energy -= 2
            was_pit = world.make_pit_safe(target)
            if was_pit:
                agent.has_ladder = False
                agent.kb['safe'].add(target)
                agent.kb['potential_pits'].discard(target)
                print(f"🪜 Escada usada em {target}! O poço agora é seguro.")
            else:
                print(f"🤔 Tentou usar a escada em {target}, mas não era um poço.")

        elif action_type == 'return_home':
            print("Plano: Retornar à base...")
            path_home = agent.bfs(agent.pos, {target})
            if path_home and agent.pos != (0,0):
                # Executa apenas o próximo passo do caminho de volta
                if not agent.execute_move(path_home[1]):
                    final_reason = "A energia acabou ao tentar retornar."
                    break
            else:
                final_reason = "Agente na base ou sem caminho de volta."
                break

        if agent.resources_collected >= 4:
            final_reason = "Todos os recursos foram coletados!"
            break
        if agent.energy <= 0:
            final_reason = "A energia acabou!"
            break
    
    display_final_results(agent, final_reason)

if __name__ == "__main__":
    run_simulation()