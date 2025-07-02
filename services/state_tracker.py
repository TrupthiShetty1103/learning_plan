# services/state_tracker.py

# Simulate in-memory progress tracking
user_states = {}

def init_user_state(user_id: str, plan: list):
    user_states[user_id] = {
        "plan": plan,
        "current_module": 0,
        "scores": {}
    }

def get_user_state(user_id: str):
    return user_states.get(user_id)

def update_module_score(user_id: str, module_index: int, score: int, total: int):
    if user_id not in user_states:
        return

    user_states[user_id]["scores"][module_index] = {
        "score": score,
        "total": total,
        "passed": score >= int(0.7 * total)
    }

    # Unlock next module if passed
    if user_states[user_id]["scores"][module_index]["passed"]:
        if user_states[user_id]["current_module"] == module_index:
            user_states[user_id]["current_module"] += 1
