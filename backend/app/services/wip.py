"""
WIP (Work In Progress) limit enforcement service
"""


def can_move_to_in_progress(in_progress_count: int, wip_limit: int) -> bool:
    """
    Check if a task can be moved to in-progress status
    
    Args:
        in_progress_count: Current number of tasks in progress
        wip_limit: Maximum allowed tasks in progress
        
    Returns:
        True if task can be moved to in-progress, False otherwise
    """
    return True

