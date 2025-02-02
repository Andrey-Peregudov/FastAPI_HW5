import random

from faker import Faker
from sqlmodel import Session

from database import engine
from models import User
                    # MotoCreate, Moto, Auto, News, CarEnum, MotoEnum)

fake = Faker()


def seed():
    # moto_list=[]
    # for i in MotoEnum:
    #     moto_list.append(i)

    with Session(engine, autoflush=False) as session:
        for _ in range(5):
            a = User(username=fake.user_name(), email=fake.email(), password='111')
            session.add(a)
            session.commit()
        # for _ in range(30):
        #     a= Moto(age=random.randint(2000, 2025), model=moto_list[random.randint(0, len(moto_list)-1)], user_id=random.randint(1, 5))
        #     session.add(a)
        #     session.commit()
        # for _ in range(10):
        #     a= Auto(age=random.randint(2000, 2025), user_id=random.randint(1, 5))
        #     session.add(a)
        #     session.commit()
        # for _ in range(50):
        #     a= News(nums=random.randint(1, 100), text=fake.text(max_nb_chars=20))
        #     session.add(a)
        #     session.commit()

