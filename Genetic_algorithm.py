import random
import copy

GRID_SIZE = 10
POP_SIZE = 20
GENERATIONS = 250
MUTATION_RATE = 0.07
TOKENS = ['T', 'A'] 

def create_grid():
    """Cria um mapa (indivíduo) aleatório."""
    return [[random.choice(TOKENS) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def calculate_fitness(grid):
    """Calcula a 'qualidade' (fitness) de um mapa."""
    fitness, center_bonus, inland_bonus, small_group_penalty, coastal_bonus = 0,0,0,0,0
    margin = GRID_SIZE // 4

    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            tile = grid[r][c]

            if margin <= r < GRID_SIZE-margin and margin <= c < GRID_SIZE-margin and tile=='T':
                center_bonus += 3
            
            for dr, dc in [(0,1), (1,0)]: 
                nr, nc = r + dr, c + dc
                if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                    if tile == grid[nr][nc]: fitness += 3 if tile == 'A' else 2
                    else: fitness += 1
            
            if tile == 'A':
                land_coords = []
                for dr_n, dc_n in [(0,1),(0,-1),(1,0),(-1,0)]:
                    nr_n, nc_n = r + dr_n, c + dc_n
                    if 0 <= nr_n<GRID_SIZE and 0 <= nc_n<GRID_SIZE and grid[nr_n][nc_n]=='T':
                        land_coords.append((dr_n, dc_n))
                num_ln = len(land_coords)
                if num_ln >= 3: inland_bonus += 5
                elif num_ln == 2 and (land_coords[0][0]==-land_coords[1][0] and \
                                      land_coords[0][1]==-land_coords[1][1]):
                    inland_bonus += 3
                
                if (r == 0 or r == GRID_SIZE - 1 or c == 0 or c == GRID_SIZE - 1):
                    water_edge = 0 
                    for dr_b, dc_b in [(0,1),(0,-1),(1,0),(-1,0)]:
                        if 0<=r+dr_b<GRID_SIZE and 0<=c+dc_b<GRID_SIZE and grid[r+dr_b][c+dc_b]=='A':
                            water_edge += 1
                    if water_edge <= 1: coastal_bonus += 2
            
            num_neighbors = 0
            for dr_sg, dc_sg in [(0,1),(0,-1),(1,0),(-1,0)]:
                nr_sg, nc_sg = r + dr_sg, c + dc_sg
                if 0 <= nr_sg < GRID_SIZE and 0 <= nc_sg < GRID_SIZE:
                    if grid[nr_sg][nc_sg] == tile:
                        num_neighbors += 1
            
            if num_neighbors == 0: small_group_penalty -= 10
            elif num_neighbors == 1: small_group_penalty -= 5
            
    return fitness + center_bonus + inland_bonus + small_group_penalty + coastal_bonus

def selection(pop_w_f):
    p1_i, p2_i = random.randrange(len(pop_w_f)), random.randrange(len(pop_w_f))
    ind1, ind2 = pop_w_f[p1_i], pop_w_f[p2_i]
    return ind1[0] if ind1[1] > ind2[1] else ind2[0]

def crossover(p1, p2):
    return [[(p2[r][c] if random.random()<0.5 else p1[r][c]) for c in range(GRID_SIZE)] for r in range(GRID_SIZE)]

def mutate(grid_in):
    return [[(random.choice(TOKENS) if random.random()<MUTATION_RATE else tile) for tile in row] for row in grid_in]

population = [create_grid() for _ in range(POP_SIZE)]
for generation in range(GENERATIONS):
    pop_with_fitness = [(m,calculate_fitness(m)) for m in population]
    pop_with_fitness.sort(key=lambda x: x[1], reverse=True)
    next_gen_pop = [copy.deepcopy(pop_with_fitness[0][0])] 
    while len(next_gen_pop) < POP_SIZE:
        parent1, parent2 = selection(pop_with_fitness), selection(pop_with_fitness)
        next_gen_pop.append(mutate(crossover(parent1, parent2)))
    population = next_gen_pop

# individuo final
final_eval = sorted([(m,calculate_fitness(m)) for m in population],key=lambda x:x[1],reverse=True)
best_map_grid, best_map_fitness = final_eval[0]

print(f"\nMelhor mapa gerado (Fitness: {best_map_fitness:.0f}):")
for r_idx in range(GRID_SIZE):
    print(" ".join(best_map_grid[r_idx])) # Impressão do individuo final