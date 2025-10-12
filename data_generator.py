# -*- coding: utf-8 -*-
"""
task variant 16
"""

"""
Генератор тестовых данных для задания 30: Анализ авиакомпаний
Создает три файла:
1. partners.csv - данные об партнерах
2. projects.xlsx - данные о проектах
3. completion.json - данные о завершенности проектов
"""

import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta
import random

# Настройка генератора случайных чисел для воспроизводимости
np.random.seed(42)
random.seed(42)

def generate_partners_data():
    """Генерация данных о партнерах (CSV)"""
    partners_data = [
        {"partner_id": "P001", "name": "PARTNER01"},
        {"partner_id": "P002", "name": "PARTNER02"},
        {"partner_id": "P003", "name": "PARTNER03"},
        {"partner_id": "P004", "name": "PARTNER04"},
        {"partner_id": "P005", "name": "PARTNER05"},
        {"partner_id": "P006", "name": "PARTNER06"},
        {"partner_id": "P007", "name": "PARTNER07"},
        {"partner_id": "P008", "name": "PARTNER08"},
        {"partner_id": "P009", "name": "PARTNER09"},
        {"partner_id": "P010", "name": "PARTNER10"}
    ]

    df_partners = pd.DataFrame(partners_data)
    df_partners.to_csv('data/partners.csv', index=False, encoding='utf-8')
    print("✓ Файл partners.csv создан")
    return partners_data

def generate_projects_data(partners_data):
    """Генерация данных о рейсах (Excel)"""

    project_types = ["mvp", "optimization", "production", "scaling"]

    projects_data = []
    projects_counter = 1


    # бюджет
    min_budget = 1000
    max_budget = 500000


    for _ in range(5000):  # Генерируем 5000 проектов
        partner = random.choice(partners_data)


        # Бюджет зависит от стадии проекта
        project_stage = random.choice(project_types)
        if "mvp" in project_stage:
            max_budget = random.randint(1000, 20000)
        elif "optimization" in project_stage:
            max_budget = random.randint(20999,50000)
        elif "production" in project_stage:
            max_budget = random.randint(50999,250000)
        else:
            max_budget = random.randint(250999, 500000)

        budget_value = random.randint(int(max_budget * 0.6), max_budget)

        project_details = {
            "project_id": f"pr{projects_counter:05d}",
            "partner_id": partner["partner_id"],
            "project_type": project_stage,
            "budget": budget_value
        }

        projects_data.append(project_details)
        projects_counter += 1

    df_projects = pd.DataFrame(projects_data)
    df_projects.to_excel('data/projects.xlsx', index=False)
    print("✓ Файл projects.xlsx создан")
    return projects_data

def generate_completion_data(projects_data):
    """% освоения бюджета (JSON)"""
    projects_completion = ["one_third", "two_thirds", "full"]

    completion_data = []
    completion_counter = 1

    for project_details in projects_data:
        # Для каждого проекта выбираем один % освоения бюджета
        num_completion_vars = random.randint(0, 2)  # нумерация в списке начинается с 0

        completion_var = projects_completion[num_completion_vars]

        if completion_var == "one_third":
            completion_multiplier = random.uniform(0.03, 0.33)
        elif completion_var == "two_thirds":
            completion_multiplier = random.uniform(0.34, 0.66)
        else:  # full
            completion_multiplier = random.uniform(0.67, 1.0)

        #budget_completion = round(budget * completion_multiplier, 2)

        projects_completion_percent = {
                "project_id": project_details["project_id"],
                "completion_percent": completion_multiplier
            }

        completion_data.append(projects_completion_percent)
        completion_counter += 1

    # Сохраняем в JSON
    with open('data/projects_completion_percent.json', 'w', encoding='utf-8') as f:
        json.dump(completion_data, f, ensure_ascii=False, indent=2)

    print("✓ Файл tickets.json создан")
    return completion_data

def main():
    """Основная функция генерации данных"""
    print("Генерация тестовых данных для анализа выполнения проектов...")
    print("=" * 50)

    # Создаем папку data если её нет
    if not os.path.exists('data'):
        os.makedirs('data')
        print("✓ Создана папка 'data'")

    # Генерируем данные
    partners_data = generate_partners_data()
    projects_data = generate_projects_data(partners_data)
    completion_data = generate_completion_data(projects_data)

    print("=" * 50)
    print(f"Сгенерировано:")
    print(f"- Партнерских компаний: {len(partners_data)}")
    print(f"- Проектов: {len(projects_data)}")
    print(f"- Уровней выполнения проектов: {len(completion_data)}")
    print("\nВсе файлы сохранены в папке 'data/'")

if __name__ == "__main__":
    main()
