from neweb.views import *
from fusioncharts import FusionCharts
import MySQLdb
import abc, six
def makeChart(request):
    conn=Singleton.dbase()
    cursor=conn.getCursor()
    cursor.execute("select distinct FoodName, FoodPrice from FoodItem")
    row=cursor.fetchall()
    dataSource = {}
    dataSource['chart'] = { 
	    "caption": "Food and Price",
	    "subCaption": "DUClub",
	    "xAxisName": "Item",
	    "yAxisName": "Price (In Taka)",
	    "numberPrefix": "Taka",
	    "theme": "carbon"
    }
    dataSource['data'] = []
    for key in row:
        data = {}
	data['label'] = key[0]
	data['value'] = key[1]
	dataSource['data'].append(data)    	  		
	column2D = FusionCharts("column2D", "ex1" , "800", "500", "chart-1", "json", dataSource)
    return render(request, 'chart.html', {'output': column2D.render()})
