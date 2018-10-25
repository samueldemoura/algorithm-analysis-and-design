import sys
import numpy as np

def inform(value, name):
    '''Utility function.'''
    print('Better value found: {0} thanks to {1}'.format(value, name))

class TSP():
    '''Algorithm for the Travelling Salesman Problem.
    * Solution is a list of all the nodes the salesman will visit, with the return to the first
    city being IMPLIED (not explicitly appended to the end of the list).
    '''

    # TSPLIB header metadata
    dimension = None
    edge_weight_type = None
    edge_weight_format = None
    node_coord_section = None

    # Instance-related values
    weight_matrix = None

    #
    # Utility functions
    #

    def from_file(self, filepath):
        '''Parse data from a TSPLIB .tsp file.'''
        with open(filepath, 'r') as file:
            section = 'HEADER'

            for line in file:
                #
                # Parse section changes
                #

                if 'NODE_COORD_SECTION' in line:
                    section = 'NODE_COORD_SECTION'
                    self.node_coord_section = []
                    continue

                if 'EDGE_WEIGHT_SECTION' in line:
                    section = 'EDGE_WEIGHT_SECTION'
                    line_counter = 0
                    continue

                if 'DISPLAY_DATA_SECTION' in line:
                    section = 'DISPLAY_DATA_SECTION'
                    continue

                #
                # Parse sections
                #

                if section == 'HEADER':
                    # Parse attributes from header
                    if 'DIMENSION: ' in line:
                        self.dimension = int(line.split(' ')[1])
                        self.weight_matrix = np.full((self.dimension, self.dimension), np.nan)

                    if 'EDGE_WEIGHT_TYPE: ' in line:
                        self.edge_weight_type = line.split(' ')[1].strip()

                    if 'EDGE_WEIGHT_FORMAT: ' in line:
                        self.edge_weight_format = line.split(' ')[1].strip()

                elif section == 'NODE_COORD_SECTION':
                    # Parse NODE_COORD_SECTION into list
                    if 'EOF' in line:
                        break

                    aux = []
                    for value in line.split():
                        aux.append(float(value) if '.' in value else int(value))

                    self.node_coord_section.append(aux)

                elif section == 'EDGE_WEIGHT_SECTION':
                    if self.edge_weight_format == 'FULL_MATRIX':
                        aux = []
                        for i, value in enumerate(line.split()):
                            self.weight_matrix[line_counter, i] = \
                                float(value) if '.' in value else int(value)

                        line_counter += 1
                    else:
                        raise NotImplementedError

                elif section == 'DISPLAY_DATA_SECTION':
                    continue # Useless

                else:
                    raise NotImplementedError(section)

    def weight(self, node_from, node_to):
        '''Return weight between two nodes or False if nodes are not connected.'''
        value = self.weight_matrix[node_from, node_to]

        if not np.isnan(value):
            # Weight is already calculated, return it
            return value

        # Weight must be calculated
        if self.edge_weight_type == 'GEO':
            # TODO: Implement this (https://en.wikipedia.org/wiki/Geographical_distance) properly!
            # WARNING: This is currently (incorrectly) calculated as euclidian distance.
            # WARNING: Assuming nodes are always listed in ascending order in .tsp file!
            pos_a = self.node_coord_section[node_from][1:]
            pos_b = self.node_coord_section[node_to][1:]

            value = np.sqrt((pos_b[0] - pos_a[0])**2 + (pos_b[1] - pos_a[1])**2)

        elif self.edge_weight_type == 'EUC_2D':
            # WARNING: Assuming nodes are always listed in ascending order in .tsp file!
            pos_a = self.node_coord_section[node_from][1:]
            pos_b = self.node_coord_section[node_to][1:]

            value = np.sqrt((pos_b[0] - pos_a[0])**2 + (pos_b[1] - pos_a[1])**2)

        else:
            raise NotImplementedError

        # Save calculated value and return
        self.weight_matrix[node_from, node_to] = value
        return value

    def is_viable_solution(self, solution):
        '''Return if presented solution is viable.'''

        # Must contain all nodes
        if len(solution) != self.dimension:
            return False

        # Must not contain duplicates
        if len(solution) != len(set(solution)):
            return False

        # Must not travel through inexistent connections
        prev_node = solution[0]
        for cur_node in solution[1:]:
            if not self.weight(prev_node, cur_node):
                return False

        # Must be able to return to initial node
        if not self.weight(solution[-1], solution[0]):
            return False

        # Passed all checks!
        return True

    def sum(self, solution):
        '''Return sum of weights in presented solution.'''
        value = 0

        prev_node = solution[0]
        for cur_node in solution[1:]:
            value += self.weight(prev_node, cur_node)
        value += self.weight(solution[-1], solution[0]) # Back to the first city

        return value

    #
    # Construction heuristic
    #

    def build_initial_solution(self, starting_node=0):
        '''Build an initial (viable) solution using a greedy algortihm.'''
        solution = [starting_node]
        remaining = [i for i in range(0, self.dimension) if i != starting_node]

        # TODO: Treat cases where this builds an inviable solution (or breaks)
        while remaining:
            best_cost = None
            best_possibility = None

            for possibility in remaining:
                cost = self.weight(solution[-1], possibility)

                if not best_cost or (cost and cost < best_cost):
                    best_cost = cost
                    best_possibility = possibility

            solution.append(best_possibility)
            remaining.remove(best_possibility)

        return solution

    #
    # Neighbourhood movements: these take a viable solution and return a slightly modified one.
    #

    def swap(self, solution, pos_a, pos_b):
        sol = solution.copy()

        tmp = sol[pos_a]
        sol[pos_a] = sol[pos_b]
        sol[pos_b] = tmp

        return sol

    def two_opt(self, solution, position):
        return self.swap(solution, position, position + 1)

    def reinsert(self, solution, position):
        best_solution = solution
        best_value = self.sum(solution)

        new_sol = solution.copy()
        node = new_sol.pop(position)

        for i in range(0, self.dimension - 1):
            new_sol.insert(i, node)

            if self.sum(new_sol) < best_value:
                # Found better solution
                best_solution = new_sol.copy()
                best_value = self.sum(new_sol)
            else:
                # Found worse or equal solution, remove node to try again
                new_sol.pop(i)

        return best_solution

    #
    # Local search: these functions check all possible viable solutions that can be created by
    # the functions defined above, then return the best viable solution found.
    #

    def swap_search(self, solution):
        best_solution = solution.copy()

        for i in range(0, self.dimension - 1):
            for j in range(i + 1, self.dimension - 1):
                sol = self.swap(solution, i, j)
                if self.sum(sol) < self.sum(best_solution) and self.is_viable_solution(sol):
                    inform(self.sum(sol), 'swap_search')
                    best_solution = sol

        return best_solution

    def two_opt_search(self, solution):
        best_solution = solution.copy()

        for i in range(0, self.dimension - 2):
            sol = self.two_opt(solution, i)
            if self.sum(sol) < self.sum(best_solution) and self.is_viable_solution(sol):
                inform(self.sum(sol), 'two_opt_search')
                best_solution = sol

        return best_solution

    def reinsert_search(self, solution):
        best_solution = solution.copy()

        for i in range(0, self.dimension - 1):
            sol = self.reinsert(solution, i)
            if self.sum(sol) < self.sum(best_solution) and self.is_viable_solution(sol):
                inform(self.sum(sol), 'reinsert_search')
                best_solution = sol

        return best_solution

    #
    # Optimization algorithm
    #

    def vnd(self):
        '''Run the Variable Neighbourhood Descent algorithm.'''
        solution = self.build_initial_solution()
        search_functions = [self.swap_search, self.two_opt_search, self.reinsert_search]

        i = 0
        while i < len(search_functions):
            new_solution = search_functions[i](solution)
            i += 1

            if new_solution != solution:
                solution = new_solution
                i = 0

        return solution

#
# Program logic
#

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 tsp.py <input file>')
        quit()

    tsp = TSP()
    tsp.from_file(sys.argv[1])
    final_solution = tsp.vnd()
    print(final_solution)
    print(tsp.sum(final_solution))
