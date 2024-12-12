import requests
import pandas as pd
import csv
import calculations


def open_cmp():
    """Open patient CMP data

    Returns:
        dictionary: keys are patient_ids, value is  a list of dictionaries of cmp data values
    """
    cmp_data = requests.get(
        "https://ils.unc.edu/courses/2024_fall/chip490_335/cmp.json"
    )
    cmp_data = cmp_data.json()
    return cmp_data


def open_demos():
    """Opens patient demographics csv file and converts to pandas dataframe. Edits some data types in dataframe for future analysis

    Returns:
        dataframe: pandas dataframe of demographics data, column headers match that of csv file and are removed from data
    """
    demos = requests.get(
        "https://ils.unc.edu/courses/2024_fall/chip490_335/patient_demographics.csv"
    )
    patient_demos = csv.reader(demos.text.splitlines())
    patient_demos = pd.DataFrame(patient_demos)
    patient_demos.columns = patient_demos.iloc[0]
    patient_demos = patient_demos[1:]

    patient_demos["sex"] = patient_demos["sex"].astype(str)
    patient_demos["age"] = patient_demos["age"].astype(int)
    patient_demos["weight_lbs"] = patient_demos["weight_lbs"].astype(int)
    patient_demos["height_inches"] = patient_demos["height_inches"].astype(int)

    return patient_demos


def calculate_eGFR_BMI(cmp, demos):
    """Uses data from cmp data and patient demographics to calculate patient's eGFR and BMI values. Values are inserted into a dataframe along with patient_id

    Args:
        demos (dataframe): dataframe containing patients demographic information
        cmp (dictionary): keys are patient_ids, which has a list of dictionaries of cmp data values

    Returns:
        dataframe: contains patient_id, BMI, and eGFR values for each patient
    """
    calculated_data = [["patient_id", "BMI", "eGFR"]]

    for patient in cmp:
        for results in cmp[patient]:
            if results["measure"] == "Creatinine":
                measure = results["patient_measure"]

        sex = demos.loc[demos["patient_id"] == patient, "sex"].values[0]
        age = demos.loc[demos["patient_id"] == patient, "age"].values[0]
        weight = demos.loc[demos["patient_id"] == patient, "weight_lbs"].values[0]
        height = demos.loc[demos["patient_id"] == patient, "height_inches"].values[0]
        eGFR = calculations.CKD_EPI(sex, measure, age)
        bmi = calculations.Body_Mass_Index(weight, height)
        calculated_data.append([patient, float(bmi), float(eGFR)])

    calculated_data = pd.DataFrame(calculated_data)
    calculated_data.columns = calculated_data.iloc[0]
    calculated_data = calculated_data[1:]
    return calculated_data


def merge_table():
    """Merges patient demos dataframe and BMI+eGFR dataframe together based on patient_id. Filters data such that only patients with eGFR <= 65 remain. Drops columns to only keep sex, age, height, weight, BMI, and eGFR

    Args:
        cmp (dictionary): keys are patient_ids, which has a list of dictionaries of cmp data values
        demos (dataframe): dataframe containing patients demographic information

    Returns:
        dataframe: dataframe for patients with eGFR <= 65
    """
    patient_demos = open_demos()
    cmp = open_cmp()
    eGFR_BMI_table = calculate_eGFR_BMI(cmp, patient_demos)
    output = pd.merge(patient_demos, eGFR_BMI_table, on="patient_id")
    output = output.set_index("patient_id")
    output = output[output["eGFR"] <= 65]
    output = output.drop(
        columns=[
            "first_name",
            "last_name",
            "street_address",
            "city",
            "state",
            "zip_code",
            "home_number",
            "mobile_number",
        ]
    )
    return output
