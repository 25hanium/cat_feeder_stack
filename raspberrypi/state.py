from .client import post

def report_left_amount(hopper_left_g):
    return post("/api/feeder-state", {"left_amount": int(hopper_left_g)})
