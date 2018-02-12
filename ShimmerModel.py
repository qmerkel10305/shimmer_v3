import json

class ShimmerModel():
    """
    Queues of images for Shimmer

    Arguments:
        queue: The underlying ImageQueue
    """

    def __init__(self, queue):
        self.images = queue
        self.next_id = 0
        self.replay_pos = 0
        self.targets = []

    def img(self, idx):
        """
        Get image data at index idx

        Arguments:
            idx: the index to get data at
        """
        return self.targets[idx]

    def get_next_image(self):
        """
        Retrieves the next image out of the queue
        """
        next_img = self.images.get_next_image()
        if next_img is None:
            # No more images in the queue.
            return self.get_replay_image()

        # Each images gets a serial id that shimmer uses to track it within this session
        tgt = {
            "id": self.next_id,
            "image": "image/" + str(self.next_id),
            "targets": [],
            "path": next_img,
            "flight": self.images.get_flight_id()
        }
        self.targets.append(tgt)
        self.next_id += 1
        return tgt

    def get_replay_image(self):
        """
        Replays images in a loop
        """
        if self.replay_pos == len(self.targets):
            self.replay_pos = 0
        img = self.targets[self.replay_pos]
        self.replay_pos += 1
        return img

    def update_targets(self, id, targets):
        """
        Updates the targets associated with an image

        Arguments:
            id: the id of the image to update
            targets: the updated target data to add

        Returns: true if successful
        """
        self.targets[id]["targets"] = targets