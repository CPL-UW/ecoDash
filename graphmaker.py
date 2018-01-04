import pandas as pd
import datetime
import logging
from bokeh.core.properties import value
from bokeh.io import show, output_file, curdoc
from bokeh.models import ColumnDataSource, Legend, HoverTool, Title
from bokeh.plotting import figure, show, output_file
# from bokeh.charts import Bar, output_file, show
from bokeh.layouts import row, widgetbox
from bokeh.models.widgets import Button, RadioButtonGroup, Select, Slider, Paragraph, Div
import math

links = pd.read_csv("../../eventmetas.csv")
evMetas = dict(zip(list(links.Type), list(links.meta)))

df = pd.read_csv("../../allTheData.csv")

# timedf = df
# 2017-05-29 22:15:06.582413-04
pattern = "%Y-%m-%d %H:%M:%S.%f"

studsA = ['dmlwblock2pair3', 
  'dmlwblock2pair9', 
  'dmlwblock2pair8',
  'dmlwblock2pair12', 
  'dmlwblock2pair11',
  'dmlwblock2pair5',
  'dmlwblock2pair6', 
  'dmlwblock2pair2',
  'dmlwblock2pair4', 
  'dmlwblock2pair10']

studsB = ['dmlwblock2pair3', 
  'dmlwblock2pair1', 
  'dmlwblock2pair11',
  'dmlwblock2pair12', 
  'dmlwblock2pair7', 
  'dmlwblock2pair5',
  'dmlwblock2pair6', 
  'dmlwblock2pair2',
  'dmlwblock2pair4', 
  'dmlwblock2pair10']

classes = {
  "Class A": studsA,
  "Class B": studsB
}


def getSec(t):
  return int(time.mktime(time.strptime(t[:-3], pattern))) 

def makeTime(t):
  return time.strptime(t[:-3], pattern)

def makeMeta(e):
  if (e  in evMetas.keys()):
    return evMetas[e]
  return "None"


def subuserdf (users):
  global userdf
  userdf = df[df["username"].isin(users)]

def endTime(gap):
  # return (latesttime - datetime.timedelta(minutes = gap)).strftime('%Y-%m-%d %H:%M:%S.%f')
  return (latesttime - datetime.timedelta(minutes = gap)).strftime(pattern)

def startTime (gap):
  return (earliesttime + datetime.timedelta(minutes = gap)).strftime(pattern)

def makesubdf(timeStartGap, timeEndGap):
  if (timeEndGap >= timeStartGap):
    timeStartGap = timeEndGap + 10
    start.value = timeStartGap
  oldestTime = endTime(timeStartGap)
  newestTime = endTime(timeEndGap)
  global timedf 
  timedf = userdf[(userdf["timestamp"] > oldestTime) & (userdf["timestamp"] < newestTime)]
  # return userdf[userdf["timestamp"] > lastTime]

def mainTimeProcessing():
  global typecounts
  # makesubdf(15)
  a = timedf.groupby(["username", "metas"])
  typecounts = a.size()

def setupFinalDict():
  global finalDict
  global typecounts
  for s in studs:
    finalDict[s] =  {
      "Analysis": 0,
      "Exploration": 0, 
      "Collection": 0, 
      "Experimentation": 0, 
      "Hypothesis": 0, 
      "Data": 0,
      # "None": 0
    }
  for e in typecounts.iteritems():
    if e[0][1] != "None":
      finalDict[e[0][0]][e[0][1]] = e[1]

def fillFinalDict():
  global finalDict
  for s in studs:
    finalDict[s]["total"] = sum(finalDict[s].values())

def setupStackDict():
  global stackDict
  stackDict = {"students": studs}
  for st in states:
    stackDict[st] = []

def fillStackDict():
  global stackDict
  global finalDict
  for s in studs:
    if s not in finalDict:
      for st in states:
        stackDict[st].append(0)
    else:
      if sum(finalDict[s].values()) == 0:
        for st in states:
          stackDict[st].append(0)
      else:
        for st in states:
          if st in finalDict[s]:
            stackDict[st].append(finalDict[s][st] / (1.0 * finalDict[s]["total"]))
          else:
            stackDict[st].append(0)

def setDivText():
  global div
  # global para
  div.text = "Data starts: " + str(endTime(start.value))[:-7] + " <br /> Data ends: " + str(endTime(end.value))[:-7]
  # para.text = "Data starts: " + str(endTime(start.value))[:-7] + " \n Data ends: " + str(endTime(end.value))[:-7]
    # global p
  # enddays = truncateDecimals(start.value / 1440)
  # endhrs = truncateDecimals((start.value % 1440) / 60)
  # endmins = truncateDecimals(start.value % 60)
  # startdays = truncateDecimals(end.value / 1440)
  # starthrs = truncateDecimals((end.value % 1440) / 60)
  # startmins = truncateDecimals(end.value % 60)
  # titletext = "Data starts: " + str(endTime(start.value))[:-7] + " \n Data ends: " + str(endTime(end.value))[:-7]
   # + " \n <br />Beginning: " + str(enddays) + " days, " + str(endhrs) + " hours, " + str(endmins) + " minutes ago. Ending: "  + str(startdays) + " days, " + str(starthrs) + " hours, " + str(startmins) + " minutes ago."
  # p.title = Title(text=titletext, align="left")
  # global para
  # para.text = titletext

def everythingForStack (startgap, endgap):
  makesubdf(startgap, endgap)
  mainTimeProcessing()
  setupFinalDict()
  fillFinalDict()
  setupStackDict()
  fillStackDict()

def truncateDecimals(longFloat):
  twodecs = int(longFloat * 100)
  return twodecs/100.0

def update_data(attrname, old, new):
  if (new in twindow.keys() and new != "Custom"):
    end.value = start.value - twindow[time_window.value]
  elif (time_window.value != "Custom"):
    if (start.value == new):
      end.value = start.value - twindow[time_window.value]
    elif (end.value == new):
      start.value = end.value + twindow[time_window.value]
  everythingForStack(start.value, end.value)
  global source
  source.data = stackDict
  setDivText()

def update_class(attrname, old, new):
  u = classes[class_select.value]
  subuserdf(u)
  global users
  global studs
  users = u
  studs = u
  everythingForStack(start.value, end.value)
  global source
  source.data = stackDict

def makePlot():
  global source
  global states
  global colors
  p.vbar_stack(states, x='students', width=0.9, color=colors, source=source, legend=[value(x) for x in states])
  p.y_range.start = 0
  p.x_range.range_padding = 0.1
  p.xgrid.grid_line_color = None
  p.axis.minor_tick_line_color = None
  p.outline_line_color = None
  p.legend.orientation = "horizontal"
  p.xaxis.major_label_orientation = math.pi/4

df = df.sort_values("timestamp", ascending = False)

df["metas"] = df["type"].apply(makeMeta)
users = studsA
studs = studsA

userdf = df

subuserdf(users)

latesttime = datetime.datetime.strptime(userdf.iloc[0]["timestamp"][:-3], pattern)
earliesttime = datetime.datetime.strptime(userdf.iloc[len(userdf) - 1]["timestamp"][:-3], pattern)
campLength = (latesttime - earliesttime).days * 1440

# timedf = makesubdf(6)
typecounts = df

finalDict = {}
states = ["Analysis", "Exploration", "Collection", "Experimentation", "Hypothesis", "Data"]
# finalDict = {action: states}

stackDict = {}

print campLength
start = Slider(title="Oldest point of time from now", value=20, start=1, end=campLength, step=1)
end = Slider(title="Latest point of time from now", value=0, start=1, end=campLength, step=1)
para = Paragraph(text = """ Test""")
div = Div(text= """Test""")
twindow = {"Custom": -1, "5 min": 5, "10 min": 10, "20 min": 20, "1 hour": 60, "1 day": 1440}
time_window = Select(value="Custom", title='Time Window', options=twindow.keys())
class_select = Select(value="Class A", title='Classroom', options=classes.keys())

# inputs = widgetbox(start, end, para)
setDivText()
inputs = widgetbox(start, end, time_window, div, class_select)

start.on_change('value', update_data)
end.on_change('value', update_data)
time_window.on_change('value', update_data)
class_select.on_change('value', update_class)

everythingForStack(15, 0)

source = ColumnDataSource(data=stackDict)
p = figure(x_range=studs, plot_height=700, title="Student actions", toolbar_location=None, tools="")

colors = ["#FF77FF", "#ff5050", "#cccc00", "#6666ff", "#009999", "#66ff66"]

makePlot()

curdoc().add_root(row(inputs, p, width=800))
curdoc().title = "Student States"
