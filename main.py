from graph import Graph
from mas import MAS
from policy import Policy



NUM_VERTICES = 300
NUM_EDGES = 1000
MAX_WEIGHT = 10
NUM_AGENTS = 1
POLICY_PARTICLES = 20
MAX_LEN = NUM_VERTICES
NUM_EPISODES = 10


main_graph = Graph(NUM_VERTICES, NUM_EDGES, MAX_WEIGHT)

main_policy = Policy()
main_mas = MAS(main_graph, NUM_AGENTS, main_policy)
main_mas.run_agents(MAX_LEN, NUM_EPISODES)
diffs, num_diffs, avg_loss, test_distances = main_mas.test_policy(MAX_LEN)

print(avg_loss)





