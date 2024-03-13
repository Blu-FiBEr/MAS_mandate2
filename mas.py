import threading
import random
from agent import Agent
from vertex import Vertex


class MAS:
    def __init__(self, graph, num_agents, policy = None):
        self.graph = graph
        self.max_heuristics = {vertex_name : (self.graph.num_vertices * self.graph.max_weight) for vertex_name in self.graph.vertices.keys()}
        self.num_agents = num_agents
        self.agents = []
        for _ in range(0, num_agents):
            self.agents.append(Agent(self))
        self.policy = policy

    def set_policy(self, policy):
        """
        Set the policy for the MAS.
        """
        self.policy = policy

    def run_agents(self, max_len, num_episodes):
        """
        Run each agent in a separate thread with their initial position.
        """
        threads = []
        for id, agent in enumerate(self.agents):
            thread = threading.Thread(target=self._run_agent, args=(agent, max_len, num_episodes, id))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

    def _run_agent(self, agent, max_len, num_episodes, id):
        """
        Internal method to run an agent with its initial position.
        """

        # run multiple episodes.
        # update after each episode ends.
        part_len = (self.graph.num_vertices) // self.num_agents
        for _ in range(0, num_episodes):
            if(id != self.num_agents - 1):
                agent.initial_position = random.choice(list(self.graph.vertices.keys())[id * part_len :(id + 1) * part_len])
            else:
                agent.initial_position = random.choice(list(self.graph.vertices.keys())[id * part_len:])
            # agent.initial_position = random.choice(list(self.graph.vertices.keys()))
            agent.current_position = Vertex(agent.initial_position)
            agent.episode(max_len)
            agent.update()
            # Implement agent behavior here based on policy
            # For example, choose an action based on policy and update agent's position
            # action = self.policy.choose_action(agent.current_position)
            # agent.update(action)
            # pass  # Placeholder implementation

    def add_agent(self, agent):
        """
        Add an agent to the MAS.
        """
        self.agents.append(agent)

    
    def test_policy(self, max_len):
        test_distances = {}
        test_distances[self.graph.goal_vertex.name] = 0
        for i in (self.graph.vertices):
            if(i == self.graph.goal_vertex.name): continue
            current_position = Vertex(i)
            trajectory = []
            total_dist = 0
            while (len(trajectory) < max_len and (len(trajectory) == 0 or trajectory[len(trajectory)-1][2] != None)):
                if current_position.name == self.graph.goal_vertex.name:
                    break  # Agent reached the goal

                # Sample action from random policy
                action = self.policy.choose_action(current_position, arg_max = 1)
                if (action == None):
                    trajectory.append(
                        (current_position, current_position, None))
                    total_dist = float('inf')
                    break
                next_state = Vertex(action)
                # Append (s, a, r) pair to trajectory
                trajectory.append(
                    (current_position, next_state, self.graph.get_edge_weight(current_position, next_state)))
                total_dist += self.graph.get_edge_weight(current_position, next_state)

                # Sample next state from transitions
                # Update current position
                current_position = next_state
            if(len(trajectory) >= max_len): total_dist = float('inf')
            test_distances[i] = total_dist
        
        differences = {}
        num_differences = 0
        abs_diff_sum = 0

        # Check keys in dict1
        for key in test_distances:
            # if key not in dict2:
            #     differences[key] = (dict1[key], None)
            #     num_differences += 1
            if test_distances[key] != self.graph.dijkstra_distances[key]:
                differences[key] = (test_distances[key], self.graph.dijkstra_distances[key])
                num_differences += 1
                margin = abs(test_distances[key] - self.graph.dijkstra_distances[key])
                if(margin == float('inf')): 
                    margin = 0
                    num_differences -= 1
                abs_diff_sum += margin
        avg_loss = 0
        if(num_differences != 0): avg_loss = (abs_diff_sum/num_differences)
        return differences, num_differences, avg_loss, test_distances
