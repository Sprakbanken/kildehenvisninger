from typing import Dict, List, Optional, Union
import prodigy

from prodigy.core import Controller


def custom_task_router(ctrl: Controller, session_id: str, item: Dict) -> List[str]:
    # Define how many annotators need to see each example
    N_ANNOT=2

    # Fetch all available ids to pick from
    id_pool = ctrl.session_ids

    # Use the hashing trick to allocate tasks to annotators
    task_hash = item["_task_hash"]
    idx = task_hash % len(id_pool)
    selected_annotators = [id_pool.pop(idx)]
    while len(selected_annotators) < N_ANNOT:
        # if the pool is empty, return the selected annotators
        if len(id_pool) == 0:
            return selected_annotators
        idx = task_hash % len(id_pool)
        selected_annotators.append(id_pool.pop(idx))
    console.print(f"About to route [bold]{item['text'][:10]}...[/bold] to {selected_annotators}")
    return selected_annotators
