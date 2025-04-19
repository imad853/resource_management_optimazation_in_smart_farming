
def main():
    # === Initial State ===
    print("Initializing the initial state with soil moisture, nutrients, and other factors...\n")
    
    # Defining the initial state of the farm
    initial_state = {
        'soil_moisture': 0.25,  # Initial soil moisture value (arbitrary value between 0 and 1)
        'N': 0.15,  # Initial nitrogen content
        'P': 0.10,  # Initial phosphorus content
        'K': 0.12,  # Initial potassium content
        'soil_type': '2',  # Soil type, representing specific characteristics of soil
        'temperature': 28,  # Current temperature in degrees Celsius
        'humidity': 45,  # Current humidity percentage
        'rainfall_forecast': 6,  # Expected rainfall forecast (in mm)
        'growth_stage': 2,  # Growth stage of the crop (vegetative stage)
        'water_availability': 0.5,  # Water availability for irrigation (on a scale from 0 to 1)
        'irrigation_system': 'drip',  # Type of irrigation system being used
        'water_used': 0.0,  # Amount of water used (initialized to zero)
        'fertilizer_used': 0.0  # Amount of fertilizer used (initialized to zero)
    }

    # === Create the optimization problem ===
    print("Creating the optimization problem with the initial state...\n")
    
    # Instantiate the optimization problem with the initial state
    farm_problem = optimazition_problem(initial_state)
    
    # Manually attaching parameters (temporary fix due to missing __init__ bindings)
    # Adding parameters to the farm_problem instance based on initial state values
    farm_problem.soil_type = initial_state['soil_type']
    farm_problem.temperature = initial_state['temperature']
    farm_problem.humidity = initial_state['humidity']
    farm_problem.rainfall_forecast = initial_state['rainfall_forecast']
    farm_problem.growth_stage = initial_state['growth_stage']
    farm_problem.soil_moisture = initial_state['soil_moisture']
    farm_problem.water_availability = initial_state['water_availability']
    farm_problem.irrigation_system = initial_state['irrigation_system']

    # Define optimal ranges for different parameters to keep them within acceptable limits
    farm_problem.optimal_ranges = {
        'soil_moisture': (0.3, 0.7),
        'N': (0.2, 0.6),
        'P': (0.1, 0.4),
        'K': (0.1, 0.5),
        'WUE': (0.3, 0.6)
    }
    
    # === Inject dummy priorities for testing ===
    # Temporary lambda function to simulate priorities for water, fertilizer, and irrigation frequency
    print("Injecting dummy priorities for testing purposes...\n")
    farm_problem.priorities = lambda: {
        'water_priority': 0.4,
        'fertilizer_priority': 0.4,
        'irrigation_frequency_priority': 0.2
    }

    # === Dummy get_actions function ===
    # Simulating possible actions that can be performed on the farm (adding water and fertilizer)
    print("Defining a dummy get_actions function to simulate available actions...\n")
    farm_problem.get_actions = lambda: [
        {'water_amount': 0.5, 'fertilizer_amount': 0.2},
        {'water_amount': 1.0, 'fertilizer_amount': 0.3},
        {'water_amount': 0.2, 'fertilizer_amount': 0.1},
    ]

    # === Define a minimal Node class ===
    # Creating a minimal Node class to represent a state and its associated costs
    print("Defining a simple Node class to represent a state and its associated costs...\n")
    class Node:
        def __init__(self, state, g=0):
            self.state = state  # The state of the farm
            self.g = g  # Cost to reach this state (g represents the cost)
            self.f = 0  # Total cost (f = g + h, where h is heuristic)
        
        # Function to create a copy of the current Node (important for tree search)
        def copy(self):
            return Node(self.state.copy(), self.g)

    # === 1. Create initial node ===
    print("1. Testing initial state:")
    root = Node(initial_state)  # Creating the root node with the initial state
    print(f"Initial state: {root.state}\n")

    # === 2. Test heuristic ===
    print("2. Heuristic value of initial state:")
    h = farm_problem.heuristic(root.state)  # Calculate heuristic for the initial state
    print(f"Heuristic h(s): {h}\n")

    # === .. Test cost ===
    print("3. Cost value of initial state:")
    g = farm_problem.cost(root.state)  # Calculate cost for the initial state
    print(f"Cost g(s): {g}\n")

    # === 4. Testing if the action is valid ===
    print("4. Testing if the action is valid:")
    
    # Assuming you have a method to get valid actions.
    valid_actions = farm_problem.get_valid_actions(root.state)

    # If no valid actions exist, print an appropriate message.
    if valid_actions:
        print("Valid actions are:")
        for action in valid_actions:
            print(f"Action: {action}")
    else:
        print("No valid actions available.\n")

    # === 5. Test apply_action ===
    print("5. Applying one action:")
    test_action = (0.5, 0.2)  # water amount = 0.5, fertilizer amount = 0.2
    new_state = farm_problem.apply_action(root.state.copy(), test_action)  # Apply the action to the state
    print(f"New state after action {test_action}: {new_state}\n")

    # === 6. Test expand_node ===
    print("6. Expanding node:")
    children = farm_problem.expand_node(root)  # Expand the node to generate child nodes
    for idx, child in enumerate(children):
        print(f"Child {idx+1}:")
        print(f"State: {child.state}")
        print(f"g: {child.g}, f: {child.f}")
        print()

    # === 7. Test goal ===
    print("7. Testing if it is a goal state:")

    # Perform goal test
    goal_state = farm_problem.goal_test(root.state)

    # Print whether the current state is a goal state
    if goal_state:
        print(f"The current state {root.state} is a goal state.")
    else:
        print(f"The current state {root.state} is NOT a goal state.\n")


# Check if this is the main program being executed
if __name__ == "__main__":
    main()  # Run the main function
