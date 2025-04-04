import os

from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Завантажує .env
load_dotenv()

# Формує URL з env-змінних
DATABASE_URL = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
)

Base = declarative_base()


# Таблиця студентів
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)

    group = relationship("Group", back_populates="students")
    grades = relationship("Grade", back_populates="student")


# Таблиця груп
class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    students = relationship("Student", back_populates="group")


# Таблиця викладачів
class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    subjects = relationship("Subject", back_populates="teacher")


# Таблиця предметів
class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)

    teacher = relationship("Teacher", back_populates="subjects")
    grades = relationship("Grade", back_populates="subject")


# Таблиця оцінок
class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    grade = Column(Float, nullable=False)
    date_received = Column(Date, nullable=False)

    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")


def init_db():
    ps_engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(ps_engine)
    return ps_engine


if __name__ == "__main__":
    engine = init_db()
    Session = sessionmaker(bind=engine)
    session = Session()
    print("База даних і таблиці успішно створені.")
