from typing import Any
from queue import Queue


class CSP:
    def __init__(
        self,
        variables: list[str],
        domains: dict[str, set],
        edges: list[tuple[str, str]],
    ):
        """Constructs a CSP instance with the given variables, domains and edges.
        
        Parameters
        ----------
        variables : list[str]
            The variables for the CSP
        domains : dict[str, set]
            The domains of the variables
        edges : list[tuple[str, str]]
            Pairs of variables that must not be assigned the same value
        """
        self.variables = variables
        self.domains = domains
        self.backtrack_counter = 0
        self.fail_counter = 0

        # Binary constraints as a dictionary mapping variable pairs to a set of value pairs.
        #
        # To check if variable1=value1, variable2=value2 is in violation of a binary constraint:
        # if (
        #     (variable1, variable2) in self.binary_constraints and
        #     (value1, value2) not in self.binary_constraints[(variable1, variable2)]
        # ) or (
        #     (variable2, variable1) in self.binary_constraints and
        #     (value1, value2) not in self.binary_constraints[(variable2, variable1)]
        # ):
        #     Violates a binary constraint
        self.binary_constraints: dict[tuple[str, str], set] = {}
        for variable1, variable2 in edges:
            self.binary_constraints[(variable1, variable2)] = set()
            for value1 in self.domains[variable1]:
                for value2 in self.domains[variable2]:
                    if value1 != value2:
                        self.binary_constraints[(variable1, variable2)].add((value1, value2))
                        self.binary_constraints[(variable1, variable2)].add((value2, value1))

    def ac_3(self) -> bool:
        """Performs AC-3 on the CSP.
        Meant to be run prior to calling backtracking_search() to reduce the search for some problems.
        
        Returns
        -------
        bool
            False if a domain becomes empty, otherwise True
        """

        # Initialize the queue with all arcs in the csp (all pairs of variables with binary constraints)
        queue = Queue()
        for Xi in self.variables:
            for Xj in self.variables:
                if (Xi, Xj) in self.binary_constraints:
                    queue.put((Xi, Xj))

        while not queue.empty():
            Xi, Xj = queue.get()  # Pop the first arc from the queue
            if self.revise(Xi, Xj):  # Revise the domain of Xi based on the constraint with Xj
                if len(self.domains[Xi]) == 0:  # If Xi's domain is empty, return False (unsolvable)
                    return False
                # If revision was made, add all neighbors of Xi (excluding Xj) back into the queue
                for Xk in self.variables:
                    if Xk != Xj and (Xk, Xi) in self.binary_constraints:
                        queue.put((Xk, Xi))

        return True  # The CSP is arc-consistent

    
    def revise(self, Xi: str, Xj: str) -> bool:
        revised = False
        for x in set(self.domains[Xi]):
            # Check if there is any value in Xj's domain that satisfies the constraint with x
            if not any((x, y) in self.binary_constraints.get((Xi, Xj), set()) for y in self.domains[Xj]):
                # If no such value y exists, remove x from Xi's domain
                self.domains[Xi].remove(x)
                revised = True

        return revised


    def backtracking_search(self) -> None | dict[str, Any]:
        """Performs backtracking search on the CSP.
        
        Returns
        -------
        None | dict[str, Any]
            A solution if any exists, otherwise None
        """
        def backtrack(assignment: dict[str, Any]):
            self.backtrack_counter += 1
            if self.is_complete(assignment):  # Check if the assignment is complete
                return assignment  # Return the final solution
            
            var = self.select_unassigned_variable(assignment)  # Select a variable
            for value in self.order_domain_values(var):  # Loop over values
                if self.is_consistent(value, var, assignment):  # Check consistency
                    assignment[var] = value  # Assign value to the variable

                    result = backtrack(assignment)  # Call the backtrack function recursively
                    if result is not None:  # If a solution is found
                        return result

                    del assignment[var]  # Remove the assignment if it failed

            self.fail_counter += 1
            return None  # Failure if no valid solution


        return backtrack({})
    
    def is_complete(self, assignment: dict[str, Any]): # Checks if all csp variables have been added to the assignment dictionary
        for var in self.variables:
            if var not in assignment:
                return False
        return True
    
    def select_unassigned_variable(self, assignment: dict[str, Any]): # Returns the first unassigned variable
        for var in self.variables:
            if var not in assignment:
                return var
            
    def order_domain_values(self, var): # Returns the domain of the variable without reordering
        return self.domains[var]
         
    def is_consistent(self, value, var, assignment: dict[str, Any]): # Checks if there are any constraint violations
        for neighbor in self.variables: # Check against all variables assigned so far in the assignment
            if neighbor in assignment:
                neighbor_value = assignment[neighbor]
                # Check if the assignment violates a binary constraint
                if (
                    (var, neighbor) in self.binary_constraints and
                    (value, neighbor_value) not in self.binary_constraints[(var, neighbor)]
                ) or (
                    (neighbor, var) in self.binary_constraints and
                    (neighbor_value, value) not in self.binary_constraints[(neighbor, var)]
                ):
                    return False  # Violates a constraint
        return True  # No violations



def alldiff(variables: list[str]) -> list[tuple[str, str]]:
    """Returns a list of edges interconnecting all of the input variables
    
    Parameters
    ----------
    variables : list[str]
        The variables that all must be different

    Returns
    -------
    list[tuple[str, str]]
        List of edges in the form (a, b)
    """
    return [(variables[i], variables[j]) for i in range(len(variables) - 1) for j in range(i + 1, len(variables))]
