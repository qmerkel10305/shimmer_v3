import json
# Queue of images that are ready to
# have their target's classified
from ImageQueue import ImageQueue

class ShimmerQueue(ImageQueue):
    """
    Queues of images for Shimmer

    Arguments:
        queue: The underlying ImageQueue
        queue_arg: The argument for the queue class
    """

    def __init__(self, queue):
        super(ShimmerQueue, self).__init__()
        self.images = queue
        self.next_id = 0
        self.replay_pos = 0
        self.targets = []

    def get_next_image(self):
        """
        Retrieves the next image out of the queue
        """
        next_img = self.images.get_next_image()
        if not next_img:
            # No more images in the queue.
            return self.get_replay_image()
        tgt = {
            "id": self.next_id,
            "image": "image/" + next_img,
            "targets": []
        }
        self.targets.append(tgt)
        self.next_id += 1
        return tgt

    def get_image_at(self, idx):
        return self.images[idx]

    def get_replay_image(self):
        """
        Replays images in a loop
        """
        if self.replay_pos == len(self.targets):
            self.replay_pos = 0
        img = self.targets[self.replay_pos]
        self.replay_pos += 1
        return img