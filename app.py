from streamlit_bokeh_events import streamlit_bokeh_events
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.plotting import figure
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np

st.title('Data Tweaking Labs🧊')
st.text('Synthic Data Generation')
st.file_uploader('Upload Data')

st.radio('Pick one', ['Bias Detection and Mitigation',
                      'New Data', 'More Data'])
st.multiselect('Alogrithms', ['milk', 'apples', 'potatoes'])

# Here

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})

st.dataframe(df)


# xmin = float(input("Enter lowest x value "))
# xmax = float(input("Enter highest x value "))
# ymin = float(input("Enter lowest y value "))
# ymax = float(input("Enter highest y value "))


# class LineBuilder:
#     def __init__(self, line):
#         self.line = line
#         self.xs = list(line.get_xdata())
#         self.ys = list(line.get_ydata())
#         self.cid = line.figure.canvas.mpl_connect('button_press_event', self)

#     def __call__(self, event):
#         print('click', event)
#         if event.inaxes != self.line.axes:
#             return
#         self.xs.append(event.xdata)
#         self.ys.append(event.ydata)
#         self.line.set_data(self.xs, self.ys)
#         self.line.figure.canvas.draw()


# fig, ax = plt.subplots()
# ax.set_title('click to build line segments')
# ax.set_xlim([xmin, xmax])
# ax.set_ylim([ymin, ymax])
# line, = ax.plot([], [])  # empty line
# linebuilder = LineBuilder(line)
# plt.show()

dataframe = pd.DataFrame(
    np.random.randn(10, 20),
    columns=('col %d' % i for i in range(20)))

st.dataframe(dataframe.style.highlight_max(axis=0))
x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)

st.text_input("hi", key="hi")


st.line_chart({"data": [1, 5, 2, 6, 2, 1]})

with st.expander("See explanation"):
    st.write("""
        The chart above shows some numbers I picked for you.
        I rolled actual dice for these, so they're *guaranteed* to
        be random.
    """)
    st.image("https://emoji.gg/assets/emoji/1721_cozysip.png")

if st.text_input("password is 1234") == "1234":
    chart_data = pd.DataFrame(
        np.random.randn(20, 3),
        columns=['a', 'b', 'c'])

    chart_data

# Add a selectbox to the sidebar:
add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

# Add a slider to the sidebar:
add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)

left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
left_column.button('Press me!')

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")


# import function

# create plot
p = figure(tools="lasso_select")
cds = ColumnDataSource(
    data={
        "x": [1, 2, 3, 4],
        "y": [4, 5, 6, 7],
    }
)
p.circle("x", "y", source=cds)

# define events
cds.selected.js_on_change(
    "indices",
    CustomJS(
        args=dict(source=cds),
        code="""
        document.dispatchEvent(
            new CustomEvent("YOUR_EVENT_NAME", {detail: {your_data: "goes-here"}})
        )
        """
    )
)

# result will be a dict of {event_name: event.detail}
# events by default is "", in case of more than one events pass it as a comma separated values
# event1,event2
# debounce is in ms
# refresh_on_update should be set to False only if we dont want to update datasource at runtime
# override_height overrides the viewport height
result = streamlit_bokeh_events(
    bokeh_plot=p,
    events="YOUR_EVENT_NAME",
    key="foo",
    refresh_on_update=False,
    override_height=600,
    debounce_time=500)

# use the result
st.write(result)
