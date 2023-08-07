from dataclasses import dataclass, field


@dataclass
class FilmWork:
    id: str
    title: str
    description: str
    imdb_rating: str
    actors_names: list[str] = field(default_factory=list)
    writers_names: list[str] = field(default_factory=list)
    director: list[str] = field(default_factory=list)
    genre: list[str] = field(default_factory=list)
    actors: list[dict] = field(default_factory=list)
    writers: list[dict] = field(default_factory=list)
