# Created by Dayu Wang (dwang@stchas.edu) on 2022-03-22

# Last updated by Dayu Wang (dwang@stchas.edu) on 2022-03-24


from .search import search
from django.http.response import FileResponse
from django.shortcuts import render
from os import mkdir
from rest_framework.decorators import api_view
from shutil import make_archive, rmtree


def home(request):
    return render(request, "wisdom_google_trends_data_collector/home.html")


@api_view(["POST"])
def submit(request):
    if request.method == "POST":
        if request.path.replace('/', '') == "submit":
            input_data = {
                "start_date": request.POST["start-date"],
                "end_date": request.POST["end-date"],
                "search_terms": request.POST["search-terms"],
                "suggestion_switch": request.POST["suggestion-switch"] == "on",
                "suggestions": request.POST["suggestions"] if request.POST["suggestion-switch"] == "on" else None,
                "first_index": int(request.POST["first-index"])
            }

            rmtree(r"./wisdom_google_trends_data_collector/output_files")
            mkdir(r"./wisdom_google_trends_data_collector/output_files")
            mkdir(r"./wisdom_google_trends_data_collector/output_files/archive")
            mkdir(r"./wisdom_google_trends_data_collector/output_files/with_suggestions")
            mkdir(r"./wisdom_google_trends_data_collector/output_files/with_suggestions/reliable")
            mkdir(r"./wisdom_google_trends_data_collector/output_files/with_suggestions/unreliable")
            mkdir(r"./wisdom_google_trends_data_collector/output_files/without_suggestions")

            result = search(input_data)
            path = None
            if result:
                path = r"./wisdom_google_trends_data_collector/output_files/with_suggestions"
            else:
                path = r"./wisdom_google_trends_data_collector/output_files/without_suggestions"

            make_archive(r"./wisdom_google_trends_data_collector/output_files/archive/output", "zip", path)
            zip_file = open(r"./wisdom_google_trends_data_collector/output_files/archive/output.zip", "rb")

            return FileResponse(zip_file)
