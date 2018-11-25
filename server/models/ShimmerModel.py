from server.models.ShimmerImage import ShimmerImage
from server.models.ShimmerTarget import ShimmerTarget

class ShimmerModel():
    """
    Queues of images for Shimmer

    Arguments:
        queue: The underlying ImageQueue
    """

    def __init__(self, queue):
        self.queue = queue
        self.replay_pos = 0
        self.image_ids = []
        self.images = {}
        # Load all images already in the queue
        image = self.queue.get_next_image()
        while image is not None:
            img = ShimmerImage(image, self.queue.flight)
            self.images[img.id] = img
            self.image_ids.append(img.id)
            image = self.queue.get_next_image()

    def img(self, idx):
        """
        Get image data at index idx

        Arguments:
            idx: the index to get data at
        """
        return self.images[idx]

    def get_image(self, id):
        return self.img(id)

    def tgt(self, id):
        """
        Get the target with id

        Arguments:
            id: the target id to get
        """
        return self.queue.flight.target(id)

    def get_target(self, id):
        return self.tgt(id)

    def get_next_image(self):
        """
        Retrieves the next image out of the queue
        """
        next_img = self.queue.get_next_image()
        if next_img is None:
            # No more images in the queue.
            return self.get_replay_image()

        img = ShimmerImage(next_img, self.queue.flight)
        self.images[img.id] = img
        return img

    def get_replay_image(self):
        """
        Replays images in a loop
        """
        if self.replay_pos >= len(self.image_ids):
            self.replay_pos = 0
        img = self.images[self.image_ids[self.replay_pos]]
        self.replay_pos += 1
        return img

    def get_all_targets(self):
        """
        Get all targets from a flight
        """
        return [ ShimmerTarget(target) for target in self.queue.flight.all_targets() ]