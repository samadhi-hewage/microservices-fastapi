from fastapi import FastAPI
from models import Course, CourseCreate

app = FastAPI(title="Course Service")

courses = [
    Course(id=1, name="Computer Science", duration="4 years"),
    Course(id=2, name="IT", duration="3 years")
]

@app.get("/api/courses")
def get_courses():
    return courses

@app.post("/api/courses")
def add_course(course: CourseCreate):
    new_course = Course(id=len(courses) + 1, **course.dict())
    courses.append(new_course)
    return new_course
