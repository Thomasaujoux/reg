

from pydantic import BaseModel, Field

class Model_Input(BaseModel):
    category: str = Field(description="The category of the song, it must be one of them : DJ, chill, date, melancholy, party, sport, study")
    song_ids : str = Field(description="The ids of the songs, like this 11dFghVXANMlKmJXsNCbNl,11dFghVXANMlKmJXsNCbNl,11dFghVXANMlKmJXsNCbNl")
    genres : str = Field(default=None, title="If we want to add genre, not implemented yet")
    limit : int = Field(gt=0, description="The number of songs to add, it must be greater than 0")
