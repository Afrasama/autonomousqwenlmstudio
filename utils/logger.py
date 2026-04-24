import json
import os
from datetime import datetime, timezone
from typing import Any, Dict


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAILURE_LOG_PATH = os.path.join(PROJECT_ROOT, "data", "failure_log.jsonl")


def log_failure(
    failure_type: str,
    robot_state: Dict[str, Any],
    llm_response: Any,
    strategy_chosen: str,
) -> None:
    """
    Append a structured failure/recovery record to the JSONL log.
    """
    os.makedirs(os.path.dirname(FAILURE_LOG_PATH), exist_ok=True)

    record = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "failure_type": failure_type,
        "robot_state": robot_state,
        "llm_response": llm_response,
        "strategy_chosen": strategy_chosen,
    }

    with open(FAILURE_LOG_PATH, "a", encoding="utf-8") as file_obj:
        file_obj.write(json.dumps(record, ensure_ascii=True) + "\n")
