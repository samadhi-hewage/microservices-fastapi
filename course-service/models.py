from pydantic import BaseModel

class Course(BaseModel):
    id: int
    name: str
    duration: str

class CourseCreate(BaseModel):
    name: str
    duration: str
