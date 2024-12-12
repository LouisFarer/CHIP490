import statistics as stats


def CKD_EPI(sex, patient_value, age):
    """Calculates patient's eGFR based on age, sex, and creatinine measurement

    Args:
        sex (string): F for Female, other for Male
        patient_value (float): patient's creatinine value from CMP
        age (int): patient's age

    Returns:
        flaot: patient's eGFR
    """
    if sex == "F":
        k = 0.7
        a = -0.241
        coefficient = 1.012
    else:
        k = 0.9
        a = -0.302
        coefficient = 1
    low = min(patient_value / k, 1)
    high = max(patient_value / k, 1)
    eGFR = 142 * (low**a) * (high**-1.2) * (0.9938**age) * coefficient
    return eGFR


def Body_Mass_Index(weight, height):
    """Calculates patient's BMI based on their height and weight

    Args:
        weight (int): patient weight in pounds
        height (int): patient heigh in inches

    Returns:
        float: patient BMI
    """
    return (weight * 703) / (height**2)


def mean_calc(dataframe, measure):
    """Calculates and round mean and converts data type such that it can be printed in rich table

    Args:
        dataframe (datframe): patient data frame
        measure (string): column name from dataframe

    Returns:
        string: rounded mean of column data
    """
    mean = str(round(stats.mean(dataframe[measure]), 2))
    return mean


def standard_deviation(dataframe, measure):
    """Calculates and round standard deviation and converts data type such that it can be printed in rich table

    Args:
        dataframe (datframe): patient data frame
        measure (string): column name from dataframe

    Returns:
        string: rounded standard deviation of column data
    """
    stdv = str(round(stats.stdev(dataframe[measure]), 2))
    return stdv
