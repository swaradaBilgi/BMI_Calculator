"""
Module to calculate average BMI per city and store data in the database.

Supported operations include:
- calculate average BMI per city from JSON records

"""

import src.backend.core.bmi_calculator as bmi_calc
import src.backend.persistence.bmi_db_helper as db_ops

def get_bmi_per_city():
    """fetch city wise person data from database, calculate bmi and return average bmi per city"""
    city_names = db_ops.get_all_cities()

    bmi_average = 0.0

    for city in city_names: 
        city_id_db = db_ops.get_city_id(city)
        person_weight_and_height = db_ops.get_person_data_for_city(city_id_db)

        bmi_list = []
        for data in person_weight_and_height:
            bmi = bmi_calc.bmi_calculator(data[0], data[1])
            bmi_list.append(bmi)

        bmi_average = round(sum(bmi_list) / float(len(bmi_list)), 2)
        print("Average bmi for city", city, "is", bmi_average)

    return bmi_average