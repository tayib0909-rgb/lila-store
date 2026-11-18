from dataclasses import dataclass

FIELDS = ["name", "origin", "history", "temperament", "height", "weight", "lifespan",
          "grooming", "exercise", "trainability", "fact", "funny", "person",
          "superpower", "says", "perfect", "portrait"]


@dataclass
class Breed:
    name: str
    origin: str
    history: str
    temperament: str
    height: str
    weight: str
    lifespan: str
    grooming: int
    exercise: int
    trainability: int
    fact: str
    funny: str
    person: str
    superpower: str
    says: str
    perfect: str
    portrait: str
    category: str = ""
    img_id: str = ""


def B(*args):
    assert len(args) == len(FIELDS), (args[0], len(args))
    return Breed(*args)
