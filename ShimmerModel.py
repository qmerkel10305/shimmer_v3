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
        self.image_ids = []
        self.images = {}
        self.targets = {}
        # Load all images already in the queue
        image = self.queue.get_next_image()
        while image is not None:
            img = ShimmerImage(image, self.queue.flight)
            self.images[img.id] = img
            self.image_ids.append(img.id)
            for target in img.targets:
                self.targets[target.id] = target
            image = self.queue.get_next_image()

    def img(self, idx):
        """
        Get image data at index idx

        Arguments:
            idx: the index to get data at
        """
        return self.images[idx]

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

    def delete_target(self, id):
        self.targets[id].valid = False

    def get_all_targets(self):
        arc_targets = {}
        for target in self.targets.values():
            arc_targets[target.target_region.target.target_id] = target
        return list(arc_targets.values())

    def get_target(self, id):
        return self.targets[id]

    def merge_targets(self, ids):
        targets = [self.targets[int(id)] for id in ids]
        arc_target = targets[0].target_region.target
        for target in targets[1:]:
            old_target = target.target_region.target
            arc_target.absorb_target(old_target)

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
