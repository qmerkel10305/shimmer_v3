from ShimmerImage import ShimmerImage

class ShimmerModel():
    """
    Queues of images for Shimmer

    Arguments:
        queue: The underlying ImageQueue
    """

    def __init__(self, queue):
        self.queue = queue
        self.replay_pos = 0
        self.images = []
        self.targets = {}

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
        next_img = self.queue.get_next_image()
        if next_img is None:
            # No more images in the queue.
            return self.get_replay_image()

        tgt = ShimmerImage(next_img, self.queue.flight)
        self.images.append(tgt)
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

    def delete_target(self, id):
        self.targets[id].valid = False

    def update_targets(self, id, targets):
        """
        Updates the targets associated with an image

        Arguments:
            id: the id of the image to update
            targets: the updated target data to add

        Returns: true if successful
        """
        new_targets, deleted_targets = self.images[id].update_targets(targets)
        for tgt in new_targets:
            self.targets[tgt.id] = tgt

        for tgt in self.targets.values():
            if tgt.id in deleted_targets:
                tgt.valid = False
