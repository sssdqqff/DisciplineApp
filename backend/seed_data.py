from app.database import Sessionlocal, engine, Base
from app.models.category import Category
from app.models.task import Task


def seed():
    # Создаём таблицы, если их нет
    Base.metadata.create_all(bind=engine)

    with Sessionlocal() as session:

        # --- CATEGORIES ---
        cat_work = Category(
            name="Работа",
            description="Задачи по работе"
        )
        cat_study = Category(
            name="Учёба",
            description="Учебные задания"
        )
        cat_home = Category(
            name="Дом",
            description="Домашние дела"
        )

        session.add_all([cat_work, cat_study, cat_home])
        session.flush()  # чтобы получить id категорий

        # --- TASKS ---
        task1 = Task(
            name="Сделать отчёт",
            description="Подготовить отчёт по проекту",
            category_id=cat_work.id
        )

        task2 = Task(
            name="Выучить главы 1–3",
            description="Подготовиться к зачёту",
            category_id=cat_study.id
        )

        task3 = Task(
            name="Помыть посуду",
            description="После ужина",
            category_id=cat_home.id,
            is_active=True
        )

        session.add_all([task1, task2, task3])
        session.commit()

    print("База данных успешно заполнена!")


if __name__ == "__main__":
    seed()
