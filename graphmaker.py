import pandas as pd
import datetime
import logging
from bokeh.core.properties import value
from bokeh.io import show, output_file, curdoc
from bokeh.models import ColumnDataSource, Legend, HoverTool, Title
from bokeh.plotting import figure, show, output_file
# from bokeh.charts import Bar, output_file, show
from bokeh.layouts import row, widgetbox
from bokeh.models.widgets import Button, RadioButtonGroup, Select, Slider, Paragraph
import math

links = pd.read_csv("/Users/visheshk/Dropbox/ecoXPT/eventmetas.csv")
evMetas = dict(zip(list(links.Type), list(links.meta)))
# evMetas[""]


# df = pd.read_csv("../allTheData.csv")
df = pd.read_csv("/Users/visheshk/Dropbox/ecoXPT/allTheData.csv")

df = df.sort_values("timestamp", ascending = False)
timedf = df

# 2017-05-29 22:15:06.582413-04
pattern = "%Y-%m-%d %H:%M:%S.%f"

def getSec(t):
	return int(time.mktime(time.strptime(t[:-3], pattern)))	

def makeTime(t):
	return time.strptime(t[:-3], pattern)

def makeMeta(e):
  # print e
  # return evMetas[e]
  if (e  in evMetas.keys()):
    return evMetas[e]
  return "None"
# df["times"] = df["timestamp"].apply(getSec)
# df["timet"] = df["timestamp"].apply(makeTime)

df["metas"] = df["type"].apply(makeMeta)

studs = ['dmlwblock2pair3', 
  'dmlwblock2pair9', 
  'dmlwblock2pair8',
  'dmlwblock2pair12', 
  'dmlwblock2pair11',
  'dmlwblock2pair7', 
  'dmlwblock2pair1', 
  'dmlwblock2pair5',
  'dmlwblock2pair6', 
  'dmlwblock2pair2',
  'dmlwblock2pair4', 
  'dmlwblock2pair10']

userdf = df
def subuserdf (users):
  global userdf
  userdf = df[df["username"].isin(users)]

subuserdf(studs)
latesttime = datetime.datetime.strptime(userdf.iloc[0]["timestamp"][:-3], pattern)
earliesttime = datetime.datetime.strptime(userdf.iloc[len(userdf) - 1]["timestamp"][:-3], pattern)
campLength = (latesttime - earliesttime).days * 1440

def endTime(gap):
  return (latesttime - datetime.timedelta(minutes = gap)).strftime('%Y-%m-%d %H:%M:%S.%f')

def startTime (gap):
  return (earliesttime + datetime.timedelta(minutes = gap)).strftime('%Y-%m-%d %H:%M:%S.%f')  

def makesubdf(timeStartGap, timeEndGap):
  if (timeEndGap >= timeStartGap):
    timeStartGap = timeEndGap + 10
    start.value = timeStartGap
  oldestTime = endTime(timeStartGap)
  newestTime = endTime(timeEndGap)
  global timedf 
  timedf = userdf[(userdf["timestamp"] > oldestTime) & (userdf["timestamp"] < newestTime)]
  # return userdf[userdf["timestamp"] > lastTime]

# timedf = makesubdf(6)
typecounts = df
def mainTimeProcessing():
  global typecounts
  # makesubdf(15)
  a = timedf.groupby(["username", "metas"])
  typecounts = a.size()

finalDict = {}
states = ["Analysis", "Exploration", "Collection", "Experimentation", "Hypothesis", "Data"]
# finalDict = {action: states}


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

stackDict = {}

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

print campLength
start = Slider(title="Oldest point of time from now", value=15, start=1, end=campLength, step=1)
end = Slider(title="Latest point of time from now", value=0, start=1, end=campLength, step=1)
para = Paragraph(text = """ Test""")

inputs = widgetbox(start, end, para)

def everythingForStack (startgap, endgap):
  makesubdf(startgap, endgap)
  mainTimeProcessing()
  setupFinalDict()
  fillFinalDict()
  setupStackDict()
  fillStackDict()

def update_data(attrname, old, new):
  # global start
  # gap = start.value
  # print gap
  everythingForStack(start.value, end.value)
  global source
  source.data = stackDict
  # global p
  enddays = start.value / 1440
  endhrs = (start.value % 1440) / 60
  endmins = start.value % 60
  startdays = end.value / 1440
  starthrs = (end.value % 1440) / 60
  startmins = end.value % 60
  titletext = "Beginning: " + str(enddays) + " days, " + str(endhrs) + " hours, " + str(endmins) + " minutes ago. Ending: "  + str(startdays) + " days, " + str(starthrs) + " hours, " + str(startmins) + " minutes ago."
  # p.title = Title(text=titletext, align="left")
  global para
  para.text = titletext
  

start.on_change('value', update_data)
end.on_change('value', update_data)

everythingForStack(15, 0)

source = ColumnDataSource(data=stackDict)
p = figure(x_range=studs, plot_height=700, title="Student actions", toolbar_location=None, tools="")

colors = ["#FF77FF", "#ff5050", "#cccc00", "#6666ff", "#009999", "#66ff66"]
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

makePlot()


curdoc().add_root(row(inputs, p, width=800))
curdoc().title = "Student States"
