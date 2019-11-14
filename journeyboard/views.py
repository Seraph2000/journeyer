from django.shortcuts import render, redirect
from .models import Journey
from django.contrib import messages


# Create your views here.
def home(request):
    import requests
    import json

    return render(request, 'home.html', {'query': 'Enter a query above...'})


def dashboard(request):
    import requests
    import json

    global query_from, query_to, icscode_from, icscode_to, commonname_from, commonname_to, res

    query_from = ''
    query_to = ''
    icscode_from = ''
    icscode_to = ''
    commonname_from = ''
    commonname_to = ''
    res = ''


    if request.method == "POST":

        app_id = "4207d724"
        app_key = "ded79ff3cee16aa4b10a0d3f4a973279"

        start = request.POST['from']
        finish = request.POST['to']

        query_from = start
        query_to = finish

        get_icscode = requests.get(
            "https://api.tfl.gov.uk/journey/journeyresults/" + str(start) + "/to/" + str(finish) + "?app_id=" + str(app_id) + "&app_key=" + str(app_key)
        )

        try:
            icscode_api = get_icscode.json()
            try:
                # api logic goes here
                icscode_from = icscode_api['fromLocationDisambiguation']['disambiguationOptions'][0]['place']['icsCode']
                icscode_to = icscode_api['toLocationDisambiguation']['disambiguationOptions'][0]['place']['icsCode']
                commonname_from = icscode_api['fromLocationDisambiguation']['disambiguationOptions'][0]['place']['commonName']
                commonname_to = icscode_api['toLocationDisambiguation']['disambiguationOptions'][0]['place']['commonName']
                res = icscode_api['fromLocationDisambiguation']['disambiguationOptions'][0]
            except:
                icscode_from = [item['place']['icsCode'] for item in icscode_api['fromLocationDisambiguation']['disambiguationOptions'] if 'icsCode' in item['place']]
                icscode_to = [item['place']['icsCode'] for item in icscode_api['toLocationDisambiguation']['disambiguationOptions'] if 'icsCode' in item['place']]
                
                if icscode_from != []:
                    icscode_from = icscode_from[0]
                if icscode_to != []:
                    icscode_to = icscode_to[0]

                commonname_from = [item['place']['commonName'] if str(icscode_from) in item['place']['icsCode'] else '' for item in icscode_api['fromLocationDisambiguation']['disambiguationOptions']]
                commonname_to = [item['place']['commonName'] if str(icscode_to) in item['place']['icsCode'] else '' for item in icscode_api['toLocationDisambiguation']['disambiguationOptions']]

                if commonname_from != []:
                    commonname_from = commonname_from[0]
                if commonname_to != []:
                    commonname_to = commonname_to[0]

                res = [item if str(icscode_from) in item['place']['icsCode'] else '' for item in icscode_api['fromLocationDisambiguation']['disambiguationOptions']]

        except Exception as e:
            icscode_api = "Nothing to show"
            message = "There was an error with querying location!"


        # error handling
        try:
            api_request = requests.get(
                "https://api.tfl.gov.uk/journey/journeyresults/" + str(icscode_from) + "/to/" + str(icscode_to) + "?app_id=" + str(app_id) + "&app_key=" + str(app_key)
            )

            api = api_request.json()
            message = "success"

            journey = Journey()
            journey.query_from = str(query_from)
            journey.query_to = str(query_to)
            journey.icscode_from = str(icscode_from)
            journey.icscode_to = str(icscode_to)
            journey.commonname_from = str(commonname_from)
            journey.commonname_to = str(commonname_to)
            journey.save()

        except Exception as e:
            api = "Error"
            message = "Your search came back empty. Please try again."

        return render(
            request, 'dashboard.html', {
                'api': api,
                'icscode_api': icscode_api,
                'message': message,
                'icscode_from': icscode_from,
                'icscode_to': icscode_to,
                'query_from': query_from,
                'query_to': query_to,
                'commonname_from': commonname_from,
                'commonname_to': commonname_to,
                'res': res
            }
        )
    else:
        message = "Please enter start and finish destinations"
        return render(request, 'dashboard.html', {'message': message})


def about(request):
    return render(request, 'about.html', {})

