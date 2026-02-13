"""
Module to calculate average BMI per state from database records.

Supported operations include:
- calculate average BMI per state from database records
"""

import src.backend.persistence.bmi_db_helper as operations
import src.backend.core.bmi_calculator as calc

def bmi_per_state_from_db():
    state_names = operations.get_all_states()

    for state in state_names: 
        state_id_db = operations.get_state_id(state)
        city_id = operations.get_cities_id_for_state(state_id_db)

        people_data = []
        for i in city_id:
            person_weight_and_height = operations.get_person_data_for_city(i)
            people_data.append(person_weight_and_height)
        
        bmi_list = []
        for data in people_data:
            bmi = calc.bmi_calculator(data[0], data[1])
            bmi_list.append(bmi)

        bmi_average = round(sum(bmi_list) / float(len(bmi_list)), 2)
        print("Average bmi for state", state, "is", bmi_average)
    