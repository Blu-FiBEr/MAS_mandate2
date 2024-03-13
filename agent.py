import random
from vertex import Vertex


class Agent:
    def __init__(self, mas, initial_position = None):
        self.initial_position = initial_position
        self.current_position = initial_position
        self.mas = mas
        self.trajectory = []

    def episode(self, max_len,  policy = None):
        """
        Perform an episode for the agent until it reaches the goal or maximum length is reached.
        """
        if(policy == None):
            policy = self.mas.policy
        self.trajectory = []
        while (len(self.trajectory) < max_len and (len(self.trajectory) == 0 or self.trajectory[len(self.trajectory)-1][2] != None)):
            if self.current_position.name == self.mas.graph.goal_vertex.name:
                break  # Agent reached the goal

            # Sample action from random policy
            action = policy.choose_action(self.current_position)
            if(action == None):
                self.trajectory.append(
                    (self.current_position, self.current_position, None))
                # print(self.current_position.name)
                break
            next_state = Vertex(action)
            # Append (s, a, r) pair to trajectory
            self.trajectory.append(
                (self.current_position, next_state, self.mas.graph.get_edge_weight(self.current_position, next_state)))

            # Sample next state from transitions
            # Update current position
            self.current_position = next_state

        # Perform update for all agents that have not reached but max_len reached
        # self.update()



    def update(self, payoff_constant = 5, neg_payoff = 0.7):
        """
        Update policy using trajectory
        """
        traj = self.trajectory
        # if(len(traj) > 1): print(len(traj))

        if(len(traj) == 0 and self.current_position.name == self.mas.graph.goal_vertex.name):
            return
        # print(self.initial_position + "--" + self.mas.graph.goal_vertex.name + "--" + traj[len(traj) - 1][1].name)
        if (traj[len(traj) - 1][1].name == self.mas.graph.goal_vertex.name):
            # print("snacd,")
            path_len = 0
            for i in reversed(range(len(traj))):
                path_len += traj[i][2]
                prev_best = self.mas.max_heuristics[traj[i][0].name]
                # print("cbjs")
                if(path_len <= prev_best):
                    payoff = (prev_best + payoff_constant - path_len)/(prev_best + payoff_constant - self.mas.graph.heuristic[traj[i][0].name])
                    self.mas.max_heuristics[traj[i][0].name] = path_len
                    self.mas.policy.update(traj[i][0], traj[i][1], payoff)
            
        else:
            for i in (range(len(traj))):
                self.mas.policy.update(traj[i][0], traj[i][1], neg_payoff)

        return

         # pass  # This method will be implemented later
