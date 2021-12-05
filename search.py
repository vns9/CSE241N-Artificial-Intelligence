import math
import heapq
"""
search.py: Search algorithms on grid.
"""


def heuristic(a, b):
	"""
	Calculate the heuristic distance between two points.

	For a grid with only up/down/left/right movements, a
	good heuristic is manhattan distance.
	"""

	# BEGIN HERE #
	# Manhattan distance is chosen here as heuristic.

	return abs(b[0]-a[0])+abs(b[1]-a[1])

	# END HERE #


def searchHillClimbing(graph, start, goal):
	"""
	Perform hill climbing search on the graph.

	Find the path from start to goal.

	@graph: The graph to search on.
	@start: Start state.
	@goal: Goal state.

	returns: A dictionary which has the information of the path taken.
			 Ex. if your path contains and edge from A to B, then in
			 that dictionary, d[B] = A. This means that by checking
			 d[goal], we obtain the node just before the goal and so on.

			 We have called this dictionary, the "came_from" dictionary.
	"""

	# Initialise the came_from dictionary
	came_from = {}
	came_from[start] = None

	# BEGIN HERE #
	# When initial state itself is the goal state
	if start == goal:
		return came_from
	current_state = None
	visited_states = dict()
	parent_states = dict()
	temporary_stack = list()

	temporary_stack.append(start)
	visited_states[start] = 1
	while(temporary_stack):
		# Check if we reached the goal
		next_state = temporary_stack.pop()
		if next_state == goal:
			break
		current_state = next_state
		# Greedy
		neighbour_states = sorted([[heuristic(state, goal), state] for state in graph.neighboursOf(current_state)], reverse = True)
		for h, neighbour in neighbour_states:
			if neighbour == goal:
				parent_states[neighbour] = current_state
			if not visited_states.get(neighbour, 0):
				visited_states[neighbour] = 1
				parent_states[neighbour] = current_state
				temporary_stack.append(neighbour)
	
	# When goal is not found in the graph at all
	if goal not in parent_states.keys():
		return came_from

	# When the goal is in graph
	temp_state = goal
	while(True):
		came_from[temp_state] = parent_states[temp_state]
		temp_state = parent_states[temp_state]
		if temp_state == start:
			return came_from

	# END HERE #

	return came_from




def searchBestFirst(graph, start, goal):
	"""
	Perform best first search on the graph.

	Find the path from start to goal.

	@graph: The graph to search on.
	@start: Start state.
	@goal: Goal state.

	returns: A dictionary which has the information of the path taken.
			 Ex. if your path contains and edge from A to B, then in
			 that dictionary, d[B] = A. This means that by checking
			 d[goal], we obtain the node just before the goal and so on.

			 We have called this dictionary, the "came_from" dictionary.
	"""


	# Initialise the came_from dictionary
	came_from = {}
	came_from[start] = None



	# BEGIN HERE #
	# When initial state itself is the goal state
	if start == goal:
		return came_from
	parent_states = dict()
	visited_states = dict()
	temporary_heap = list()
	current_state = None

	temporary_heap.append((heuristic(start, goal), start))
	visited_states[start] = 1
	heapq.heapify(temporary_heap)

	while(len(temporary_heap)):
		# Check if we reached the goal
		next_state = heapq.heappop(temporary_heap)[1]
		if next_state == goal:
			break
		current_state = next_state
		neighbour_states = graph.neighboursOf(current_state)
		# Looping through neighbours
		for neighbour in neighbour_states:
			# Checking for non-visited neighbours
			if not visited_states.get(neighbour, 0):
				visited_states[neighbour] = 1
				parent_states[neighbour] = current_state
				heapq.heappush(temporary_heap, (heuristic(neighbour, goal), neighbour))
		
	# When goal is not found in the graph at all
	if goal not in parent_states.keys():
		return came_from

	# When the goal is in graph
	temp_state = goal
	while(True):
		came_from[temp_state] = parent_states[temp_state]
		temp_state = parent_states[temp_state]
		if temp_state == start:
			return came_from
	# END HERE #

	return came_from



def searchBeam(graph, start, goal, beam_length=3):
	"""
	Perform beam search on the graph.

	Find the path from start to goal.

	@graph: The graph to search on.
	@start: Start state.
	@goal: Goal state.

	returns: A dictionary which has the information of the path taken.
			 Ex. if your path contains and edge from A to B, then in
			 that dictionary, d[B] = A. This means that by checking
			 d[goal], we obtain the node just before the goal and so on.

			 We have called this dictionary, the "came_from" dictionary.
	"""

	# Initialise the came_from dictionary
	came_from = {}
	came_from[start] = None

	# BEGIN HERE #
	# When initial state itself is the goal state
	if start == goal:
		return came_from
	parent_states = dict()
	visited_states = dict()
	current = list()

	visited_states[start] = 1
	current.append([heuristic(start, goal), start])
	while(current):
		# Initialize an empty set for beam
		beam = set()
		for h, state in current:
			# Looping through neighbours
			for neighbour in graph.neighboursOf(state):
				# Visiting only non visited neighbours
				if not visited_states.get(neighbour, 0):
					parent_states[neighbour] = state
					beam.add((heuristic(neighbour, goal), neighbour))
		beam = sorted(list(beam))
		beam = beam[:min(len(beam), beam_length)]
		for h, state in beam:
			visited_states[state] = 1
		current = beam

	# When goal is not found in the graph at all
	if goal not in parent_states.keys():
		return came_from

	# When the goal is in graph
	temp_state = goal
	while(True):
		came_from[temp_state] = parent_states[temp_state]
		temp_state = parent_states[temp_state]
		if temp_state == start:
			return came_from
# END HERE #

	return came_from


def searchAStar(graph, start, goal):
	"""
	Perform A* search on the graph.

	Find the path from start to goal.

	@graph: The graph to search on.
	@start: Start state.
	@goal: Goal state.

	returns: A dictionary which has the information of the path taken.
			 Ex. if your path contains and edge from A to B, then in
			 that dictionary, d[B] = A. This means that by checking
			 d[goal], we obtain the node just before the goal and so on.

			 We have called this dictionary, the "came_from" dictionary.
	"""

	# Initialise the came_from dictionary
	came_from = {}
	came_from[start] = None

	# BEGIN HERE #
	# When initial state itself is the goal state
	if start == goal:
		return came_from
	
	var = 0
	parent_states = dict()
	visited_states = dict()
	temporary_heap = list()
	current_state = None 

	temporary_heap.append((heuristic(start, goal), start))
	heapq.heapify(temporary_heap)
	visited_states[start] = 1
	while(len(temporary_heap)):
		# Check if we reached the goal
		h, next_state = heapq.heappop(temporary_heap)
		if next_state == goal:
			break
		current_state = next_state
		neighbours = graph.neighboursOf(current_state)
		# Looping through neighbours
		for neighbour in neighbours:
			if neighbour == goal:
				parent_states[neighbour] = current_state
			# Checking for nodes which are not visited
			if not visited_states.get(neighbour, 0):
				var = h - heuristic(current_state, goal) + 1
				parent_states[neighbour] = current_state
				visited_states[neighbour] = 1
				heapq.heappush(temporary_heap,(var+heuristic(neighbour, goal), neighbour))

	# When goal is not found in the graph at all
	if goal not in parent_states.keys():
		return came_from

	# When the goal is in graph
	temp_state = goal
	while(True):
		came_from[temp_state] = parent_states[temp_state]
		temp_state = parent_states[temp_state]
		if temp_state == start:
			return came_from
	# END HERE #

	return came_from

