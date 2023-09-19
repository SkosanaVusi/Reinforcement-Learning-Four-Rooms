import os
from FourRooms import FourRooms
import numpy as np
import random

# Constants
num_epochs = 5000
epsilon_greedy = 0.5
decay_rate = 0.6  
discount_factor = 0.9

Q_values = np.zeros((169, 4))
rewards = np.zeros((169, 4))

def main():
    # Create a FourRooms object
    four_rooms_object = FourRooms('simple')

    # Define the action sequence to follow
    action_sequence = [
        FourRooms.LEFT, FourRooms.LEFT, FourRooms.LEFT,
        FourRooms.UP, FourRooms.UP, FourRooms.UP,
        FourRooms.RIGHT, FourRooms.RIGHT, FourRooms.RIGHT,
        FourRooms.DOWN, FourRooms.DOWN, FourRooms.DOWN
    ]
	#
    action_types = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    grid_types = ['EMPTY', 'RED', 'GREEN', 'BLUE']

    print('....Starting Simulation for agent....')
    print('....Agent starts at',four_rooms_object.getPosition() )
    

    for action in action_sequence:
        grid_type_new, new_position, remaining_packages, isTerminal = four_rooms_object.takeAction(action)
        if isTerminal:
            break

    for epoch in range(num_epochs):

        four_rooms_object.newEpoch()
        previous_position = four_rooms_object.getPosition()

        visited = np.zeros((169, 4), dtype=int)
        exploration_rate = epsilon_greedy
        print(f"Training... Epoch {epoch+1}/{num_epochs}")

        while not four_rooms_object.isTerminal():
            index = previous_position[0] + previous_position[1] * 13

            if random.random() < exploration_rate:
                action = random.choice(np.where(rewards[index] >= 0)[0])
            else:
                max_q_value = np.max(Q_values[index])
                choices = np.where(Q_values[index] == max_q_value)[0]
                action = random.choice(choices)

            visited[index][action] += 1
            four_rooms_object.takeAction(action)

            x, y = previous_position

            index = x + y * 13

            if previous_position == four_rooms_object.getPosition():
                rewards[index][action] = rewards[index][action] - 1

            elif four_rooms_object.getPackagesRemaining() == 0:
                rewards[index][action] = 100

            index = previous_position[1] * 13 + previous_position[0]
            learning_rate = 1 / (1 + 0.3 * visited[index][action])

            max_next_q_value = max(Q_values[four_rooms_object.getPosition()[0] + four_rooms_object.getPosition()[1] * 13])
            Q_values[index][action] += learning_rate * (
                rewards[index][action] + discount_factor * max_next_q_value - Q_values[index][action]
            )

            previous_position = four_rooms_object.getPosition()
            
            exploration_rate = exploration_rate * decay_rate
    

    print()
    print('....Training done.....')
    print('....Showing path......')
    four_rooms_object.showPath(-1)


if __name__ == "__main__":
    main()

