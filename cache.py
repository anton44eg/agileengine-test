from collections import defaultdict

class Cache:
    def __init__(self):
        self.images = {}
        self.author_to_images = defaultdict(set)
        self.camera_to_images = defaultdict(set)
        self.tag_to_images = defaultdict(set)

    def store(self, images: list):
        for image in images:
            self.store_one(image)

    def store_one(self, image: dict):
        self.images[image["id"]] = {"cropped_picture": image["cropped_picture"], "full_picture": image["full_picture"]}
        self.author_to_images[image["author"]].add(image["id"])
        if "camera" in image:
            self.camera_to_images[image["camera"]].add(image["id"])
        tags = image["tags"].split(" ")
        for tag in tags:
            self.tag_to_images[tag.lstrip("#")].add(image["id"])

    def clear(self):
        self.images = {}
        self.author_to_images = defaultdict(set)
        self.camera_to_images = defaultdict(set)
        self.tag_to_images = defaultdict(set)

    def search(self, search_term: str) -> list:
        image_ids = []
        image_ids.extend(self.author_to_images.get(search_term, []))
        image_ids.extend(self.camera_to_images.get(search_term, [])) 
        image_ids.extend(self.tag_to_images.get(search_term, []))
        return [self.images[image_id] for image_id in image_ids]
        

cache = Cache()

def store_cache(data: list):
    cache.clear()
    cache.store(data)

def search(search_term: str) -> list:
    return cache.search(search_term)
