from server.models.ShimmerModel import ShimmerModel
from server.models.ARCImageQueue import ARCImageQueue

model = None

def init_model(flight_id):
    """
    Initialize the model with flight_id
    """
    global model
    if model is not None:
        raise ValueError("Model has already been initialized")

    queue = ARCImageQueue(flight_id)
    model = ShimmerModel(queue)

def get_model():
    """
    Returns the global model instance
    """
    if model is None:
        raise ValueError("Model has not been initialized")

    return model