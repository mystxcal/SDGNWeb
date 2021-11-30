from bokeh.models import DataTable, TableColumn, PointDrawTool, ColumnDataSource, CustomJS
from bokeh.plotting import figure, output_file, show, Column
from PIL import Image
from streamlit_drawable_canvas import st_canvas
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
dataset = st.file_uploader('Upload Data')
testoutput = []

if dataset is not None:
    datatbl = pd.read_csv(dataset)
    st.write("Uploaded dataset:")
    st.dataframe(datatbl.head())

page = st.selectbox('Pick one', ['Bias Detection and Mitigation',
                                 'New Data', 'More Data'])

if page == 'Bias Detection and Mitigation':
    st.write("detecting bias")
elif page == 'New Data':

    ncols = st.text_area(label="Enter no. of cols", value="0")

    st.write("Describe the columns:")

    for i in range(int(ncols)):
        st.text_area(label="col"+f"{i}", key="col"+f"{i}", height=10)
    st.multiselect('Alogrithms', ['milk', 'apples', 'potatoes'])

    # Here

    # create plot
    # p = figure(tools="lasso_select")
    # cds = ColumnDataSource(
    #     data={
    #         "x": [1, 2, 3, 4],
    #         "y": [4, 5, 6, 7],
    #     }
    # )
    # p.circle("x", "y", source=cds)

    # # define events
    # cds.selected.js_on_change(
    #     "indices",
    #     CustomJS(
    #         args=dict(source=cds),
    #         code="""
    #         document.dispatchEvent(
    #             new CustomEvent("YOUR_EVENT_NAME", {detail: {your_data: "goes-here"}})
    #         )
    #         """
    #     )
    # )

    # # result will be a dict of {event_name: event.detail}
    # # events by default is "", in case of more than one events pass it as a comma separated values
    # # event1,event2
    # # debounce is in ms
    # # refresh_on_update should be set to False only if we dont want to update datasource at runtime
    # # override_height overrides the viewport height
    # result = streamlit_bokeh_events(
    #     bokeh_plot=p,
    #     events="YOUR_EVENT_NAME",
    #     key="foo",
    #     refresh_on_update=False,
    #     override_height=600,
    #     debounce_time=500)

    # # use the result
    # st.write(result)

    xmin, xmax, ymin, ymax = 2, 4, 5, 15
    xmin = st.slider(label="x-min", min_value=1,
                     max_value=100, value=10, step=1)
    xmax = st.slider(label="x-max", min_value=xmin+1,
                     max_value=xmin+100, value=10, step=1)
    ymin = st.slider(label="y-min", min_value=1,
                     max_value=100, value=10, step=1)
    ymax = st.slider(label="y-max", min_value=ymin+1,
                     max_value=ymin+100, value=10, step=1)
    fig, ax = plt.subplots()
    ax.set_xlim([xmin, xmax])
    ax.set_ylim([ymin, ymax])
    line, = ax.plot([], [])
    plt.savefig('img.png')
    i = Image.open('img.png')
    # st.image(i)
    # st.pyplot(fig)

    canvas_result = st_canvas(
        stroke_width=1, background_image=i, update_streamlit=True)
    testoutput.append(canvas_result)
    print(canvas_result)

    if st.button(label="print output"):
        st.write(testoutput)

    xmin2 = st.slider(label="x-min2", min_value=1,
                      max_value=100, value=10, step=1)
    xmax2 = st.slider(label="x-max2", min_value=xmin2+1,
                      max_value=xmin2+100, value=20, step=1)
    ymin2 = st.slider(label="y-min2", min_value=1,
                      max_value=100, value=10, step=1)
    ymax2 = st.slider(label="y-max2", min_value=ymin2+1,
                      max_value=ymin2+100, value=20, step=1)

    precision = st.slider(label="precision", min_value=5,
                          max_value=10, value=5, step=1)
    if precision is not None:
        points = [0]*precision
        for i in range(precision):
            st.slider(min_value=ymin2, max_value=ymax2, key=str(i) +
                      "pt", label=str((xmin2+(((xmax2-xmin2)/precision)*i+1))))


elif page == 'More Data':
    st.write("more data")
else:
    pass


# output_file("tools_point_draw.html")

# p = figure(x_range=(0, 10), y_range=(0, 10), tools=[],
#            title='Point Draw Tool')
# p.background_fill_color = 'lightgrey'

# source = ColumnDataSource({
#     'x': [1, 5, 9], 'y': [1, 5, 9], 'color': ['red', 'green', 'yellow']
# })

# renderer = p.scatter(x='x', y='y', source=source, color='color', size=10)
# columns = [TableColumn(field="x", title="x"),
#            TableColumn(field="y", title="y"),
#            TableColumn(field='color', title='color')]
# table = DataTable(source=source, columns=columns, editable=True, height=200)

# draw_tool = PointDrawTool(renderers=[renderer], empty_value='black')
# p.add_tools(draw_tool)
# p.toolbar.active_tap = draw_tool

# print(str())


# show(Column(p, table))


def plot_and_move(df):
    p = figure(x_range=(0, 10), y_range=(0, 10), tools=[],
               title='Point Draw Tool')

    source = ColumnDataSource(df)

    renderer = p.scatter(x='x', y='y', source=source, size=10)

    draw_tool = PointDrawTool(renderers=[renderer])
    p.add_tools(draw_tool)
    p.toolbar.active_tap = draw_tool

    source.js_on_change("data", CustomJS(
        code="""
            document.dispatchEvent(
                new CustomEvent("DATA_CHANGED", {detail: cb_obj.data})
            )
        """
    ))

    event_result = streamlit_bokeh_events(
        p, key="foo", events="DATA_CHANGED", refresh_on_update=False, debounce_time=0)

    if event_result:
        df_values = event_result.get("DATA_CHANGED")
        return pd.DataFrame(df_values, index=df_values.pop("index"))
    else:
        return df


df = pd.DataFrame({
    'x': [1, 5, 9], 'y': [1, 5, 9]
})

st.write(plot_and_move(df))
