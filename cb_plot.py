import plotly.plotly as py
import psycopg2
import cb_global

con = cb_global.con
cur = cb_global.cur
log = cb_global.log

from plotly.graph_objs import *
py.sign_in('harjinder1988', cb_global.apikey)

try:
	cur.execute("""select * from """)

trace0 = Scatter(
    x=[1, 2, 3, 4],
    y=[10, 15, 13, 17]
)
trace1 = Scatter(
    x=[1, 2, 3, 4],
    y=[16, 5, 11, 9]
)
data = Data([trace0, trace1])

unique_url = py.plot(data, filename = 'basic-line')