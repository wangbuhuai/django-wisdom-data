# Created by Dayu Wang (dwang@stchas.edu) on 2022-02-23

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-03-24


from datetime import datetime
from pytrends.request import TrendReq


def search(input_data):
    pytrends = TrendReq(hl="en-US", tz=360)
    search_terms = input_data["search_terms"].split('\r\n')
    index = input_data["first_index"]
    output_path = None

    for term in search_terms:
        if term.strip() == '':
            continue

        refined_term = term
        final_suggestion = None

        if input_data["suggestion_switch"]:  # Suggestions turned on
            # Get the closest search keyword.
            split_term = term.split()
            for suggestion in pytrends.suggestions(term):
                tokens = suggestion["title"].split()
                count = 0
                for token in split_term:
                    if token in tokens:
                        count += 1
                if count < (1 if len(split_term) == 1 else 2):
                    continue
                for sug in input_data["suggestions"].split('\r\n'):
                    if sug.strip() == '':
                        continue
                    if sug.lower() in suggestion["type"].strip().lower():
                        refined_term = suggestion["mid"].strip()
                        final_suggestion = ("%s (%s)" % (suggestion["title"], suggestion["type"])).strip()
                        break

        # Search the current keyword using Google Trends.
        pytrends.build_payload([refined_term],
                               timeframe=input_data["start_date"] + ' ' + input_data["end_date"],
                               geo=None)
        result = pytrends.interest_over_time()

        # Prepare and save the result to the output file.
        now = datetime.now().strftime("%Y-%m-%dT%H%M")
        o_filename = "%s%03d - " % ('' if final_suggestion is not None else '!', index)
        o_filename += (term + " - " + now + " - CSV") \
            .replace(' ', '_').replace('.', '') + ".csv"
        if not input_data["suggestion_switch"]:
            output_path = r"./wisdom_google_trends_data_collector/output_files/without_suggestions/"
        elif final_suggestion is None:
            output_path = r"./wisdom_google_trends_data_collector/output_files/with_suggestions/unreliable/"
        else:
            output_path = r"./wisdom_google_trends_data_collector/output_files/with_suggestions/reliable/"
        o_filename = output_path + o_filename
        index += 1
        if not result.empty:
            new_col_name = term if final_suggestion is None else final_suggestion
            result.rename(columns={refined_term: new_col_name}, inplace=True)
            result.drop(labels=["isPartial"], axis=1, inplace=True)
        result.to_csv(o_filename)

    return input_data["suggestion_switch"]
