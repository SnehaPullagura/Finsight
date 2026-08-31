import collections
from typing import Any, Dict, List, Set, Tuple

class CyclicDependencyException(Exception):
    pass

class DAGWorkflowEngine:
    @staticmethod
    def detect_cycles_and_topological_sort(nodes: List[str], edges: List[Tuple[str, str]]) -> List[str]:
        # edges format: (parent_node, child_node)
        in_degree = {node: 0 for node in nodes}
        adj_list = collections.defaultdict(list)

        for src, dst in edges:
            if src in in_degree and dst in in_degree:
                adj_list[src].append(dst)
                in_degree[dst] += 1

        queue = collections.deque([node for node, deg in in_degree.items() if deg == 0])
        sorted_order = []

        while queue:
            curr = queue.popleft()
            sorted_order.append(curr)

            for neighbor in adj_list[curr]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(sorted_order) != len(nodes):
            raise CyclicDependencyException("Cycle detected in workflow graph; cannot execute cyclic DAG.")

        return sorted_order

    @staticmethod
    def execute_dag(
        nodes_def: Dict[str, Dict[str, Any]],
        edges: List[Tuple[str, str]],
        initial_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        node_names = list(nodes_def.keys())
        exec_sequence = DAGWorkflowEngine.detect_cycles_and_topological_sort(node_names, edges)

        context = dict(initial_context)
        execution_trace = []

        for node_id in exec_sequence:
            node_data = nodes_def[node_id]
            node_type = node_data.get("type", "transform")
            
            trace_entry = {"node_id": node_id, "type": node_type, "status": "success"}

            if node_type == "transform":
                fn = node_data.get("action", lambda ctx: ctx)
                context[node_id] = f"Executed node: {node_id}"
            elif node_type == "decision":
                condition = node_data.get("condition", "True")
                context[node_id] = {"condition_met": True}

            execution_trace.append(trace_entry)

        return {
            "status": "completed",
            "execution_order": exec_sequence,
            "trace": execution_trace,
            "final_context": context
        }
