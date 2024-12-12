import requests
import datetime
import pandas as pd


def open_data(state):
    """Opens drug recall data for state and convert to json

    Args:
        state (string): two letter state abbreviation

    Returns:
        dict: contains meta data and results for the selected states drug recall data
    """

    state_data = requests.get(
        f"https://api.fda.gov/drug/enforcement.json?search=state:{state}&limit=1000"
    )
    state_data = state_data.json()
    return state_data


def get_last_updated_date(state_data):
    """Retrieves the date that the API was last updated

    Args:
        state_data (dict): state meta data and recall data

    Returns:
        date: last updated date
    """
    meta_data = state_data["meta"]
    updated_date = meta_data["last_updated"]
    updated_date = datetime.datetime.strptime(updated_date, "%Y-%m-%d")
    updated_date = updated_date.date()
    return updated_date


def organize_results(state_data):
    """sorts through state recall data and creates an output in a pandas dataframe to be used in graphs in the jupyter notebook

    Args:
        state_data (dict): state meta and recall data. recall data is under the key "results"

    Returns:
        dataframe: dataframe of relevant information from each recall event
    """
    final_table = []
    column_headers = [
        "Event ID",
        "Classification",
        "Status",
        "Distribution Pattern",
        "Reason for Recall",
        "Route",
        "Manufacturer",
        "Voluntary Mandated",
    ]

    results = state_data["results"]

    for event in range(len(results)):
        id = results[event]["event_id"]
        classification = results[event]["classification"]
        status = results[event]["status"]
        dist_pat = results[event]["distribution_pattern"]
        reason_recall = results[event]["reason_for_recall"]

        open_fda = results[event]["openfda"]
        route = open_fda.get("route", ["N/A"])
        manufacturer = results[event]["recalling_firm"]
        mandated = results[event]["voluntary_mandated"]
        final_table.append(
            [
                id,
                classification,
                status,
                dist_pat,
                reason_recall,
                route,
                manufacturer,
                mandated,
            ]
        )

    output = pd.DataFrame(final_table)
    output.columns = column_headers
    output.set_index("Event ID")
    return output


def main(state):
    """Performs all above functions

    Args:
        state (string): two letter state abbreviation

    Returns:
        date: date that the data was last updated
        dataframe: recall data in dataframe

    """

    state_data = open_data(state)
    updated_date = get_last_updated_date(state_data)
    results = organize_results(state_data)
    return updated_date, results
