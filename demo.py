from boto3.dynamodb.conditions import Attr, Key
from datetime import date, timedelta
import boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("fargate-qa-Dash")

def lineChart(table, date, userid):
    red = []
    yellow = []
    green = []
    line_chart = dict()
    response = table.scan(FilterExpression=Attr("Date").eq(date) & Attr("UserId").eq(userid))
    line_chart["ChartLabels"] = []
    if len(response["Items"]) != 0:
        for items in response["Items"]:
            line_chart["ChartId"] = items['Date']
            line_chart["ChartLabels"].append(items["ChartId"])
            for data in items["ChartData"]:
                if data["label"] == "Error":
                    red.append(sum(data["data"]))
                if data["label"] == "Warning":
                    yellow.append(sum(data["data"]))
                if data["label"] == "Information":
                    green.append(sum(data["data"]))

        line_chart["ChartType"] = "line"
        line_chart["ChartData"] = [{
                    "label": "Error",
                    "data": red
                }, {
                    "label": "Warning",
                    "data": yellow
                }, {
                    "label": "Information",
                    "data": green
                }]

        return line_chart
    else:
        return None


def fortNightChart(table, date, userid):
    small = []
    larg = []
    fortnight = dict()
    fortnight["ChartId"] = "fortnight"
    fortnight["ChartType"] = "bar"
    fortnight["ChartLabels"] = []
    s = 0
    m = 0
    response = table.scan(FilterExpression=Attr("Date").eq(date) & Attr("UserId").eq(userid))
    if len(response["Items"]) != 0:
        for items in response["Items"]:
            if items["Date"] not in fortnight["ChartLabels"]:
                fortnight["ChartLabels"].append(items["Date"])
                s=0
                m=0
            else:
                pass
            if items["AnalysisType"].lower() == "large molecule":
                m += 1
            if items["AnalysisType"].lower() == "small molecule":
                s +=1
        small.append(s)
        larg.append(m)
    fortnight["ChartData"] = [{
        "label": "Small Molecule",
        "stack": "a",
        "data": small
    }, {
        "label": "Large Molecule",
        "stack": "a",
        "data": larg
    }]
    return fortnight


def dashBoardChart(table, userid):
    final_chart = []
    sdate = date(2020, 8, 1)
    edate = date(2020, 8, 30)
    delta = edate - sdate
    for i in range(delta.days + 1):
        day = sdate + timedelta(days=i)
        dates = day.strftime("%b %d, %Y")
        forchart = fortNightChart(table, dates ,userid)
        linechart = lineChart(table, dates, userid)
        response = table.scan(FilterExpression=Attr("Date").eq(dates) & Attr("UserId").eq(userid))
        if linechart is None and len(response['Items']) < 1:
            continue
        else:
            final_chart.append(linechart)
            final_chart.append(forchart)
            for items in response["Items"]:
                final_chart.append(items)
    return final_chart


x = dashBoardChart(table, "Nitish.D" )

print(x)
# sdate = date(2020, 8, 15)
# edate = date(2020, 8, 20)

# delta = edate - sdate

# for i in range(delta.days + 1):
#     day = sdate + timedelta(days=i)
#     dates = day.strftime("%b %d, %Y")
#     print(type(dates))