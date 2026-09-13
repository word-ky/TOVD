"""T013-OPS2: pure scalar health reporting; no filesystem/process actions."""

TOTAL_IMAGES = 1000
P95_BYTES = 16_355_328
RESERVE_BYTES = 8 * 1024**3


def storage_guard(closed_image_count, free_bytes):
    if type(closed_image_count) is not int or not 0 <= closed_image_count <= TOTAL_IMAGES:
        raise ValueError("closed_image_count must be an integer in [0, 1000]")
    if type(free_bytes) is not int or free_bytes < 0:
        raise ValueError("free_bytes must be a nonnegative integer")
    remaining = TOTAL_IMAGES - closed_image_count
    projected = P95_BYTES * remaining
    # ceil(6 * projected / 5 + integer reserve), without floating-point rounding.
    required = (6 * projected + 4) // 5 + RESERVE_BYTES
    margin = free_bytes - required
    return {
        "closed_image_count": closed_image_count,
        "free_bytes": free_bytes,
        "remaining": remaining,
        "projected_remaining": projected,
        "required_free": required,
        "margin": margin,
        "status": "SAFE" if margin >= 0 else "STORAGE_RISK_RETURN_TO_LEAD",
    }


def health_guard(closed_image_count, free_bytes, *, writer_alive, tmux_alive,
                 wrapper_exit_code=None):
    """None means no wrapper exit marker; invalid metadata raises, never SAFE."""
    if type(writer_alive) is not bool or type(tmux_alive) is not bool:
        raise ValueError("writer_alive and tmux_alive must be booleans")
    if wrapper_exit_code is not None and type(wrapper_exit_code) is not int:
        raise ValueError("wrapper_exit_code must be an integer or None")
    if wrapper_exit_code is not None and wrapper_exit_code != 0:
        process_status = "PRIMARY_FAILED_RETURN_TO_LEAD"
    elif wrapper_exit_code == 0 and not writer_alive and not tmux_alive:
        process_status = "PRIMARY_COMPLETE_UNVERIFIED"
    elif wrapper_exit_code is None and writer_alive and tmux_alive:
        process_status = "PRIMARY_RUNNING"
    else:
        process_status = "PROCESS_STATE_AMBIGUOUS_RETURN_TO_LEAD"
    storage = storage_guard(closed_image_count, free_bytes)
    return {
        "status": process_status if process_status.endswith("RETURN_TO_LEAD") else storage["status"],
        "process_status": process_status,
        "storage": storage,
        "writer_alive": writer_alive,
        "tmux_alive": tmux_alive,
        "wrapper_exit_code": wrapper_exit_code,
    }
