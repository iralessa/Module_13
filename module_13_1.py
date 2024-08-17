import time
import asyncio

async def start_strongman(name, power):
    print(f'Силач {name} начал соревнования.')
    for i in range(1, 6):  # Количество шаров - 5
        await asyncio.sleep(1 / power)  # Задержка обратно пропорциональна силе
        print(f'Силач {name} поднял {i} шар.')
    print("Силач ", name, "закончил соревнования.")

async def start_tournament():
    print("начало соревнования")
    task1 = asyncio.create_task(start_strongman('Pasha', 3))
    task2 = asyncio.create_task(start_strongman('Denis', 4))
    task3 = asyncio.create_task(start_strongman('Apollon', 5))
    print("конец соревнования")
    await task1
    await task2
    await task3
start = time.time()
asyncio.run(start_tournament())
finish = time.time()
print(f"Working time = {round(finish-start,2)} seconds")