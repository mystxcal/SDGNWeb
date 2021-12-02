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
import random
from faker import Faker

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn import metrics

from aif360.sklearn.inprocessing import GridSearchReduction
from aif360.sklearn.datasets import fetch_adult
from aif360.sklearn.metrics import disparate_impact_ratio, average_odds_error, generalized_fpr
from aif360.sklearn.metrics import generalized_fnr, difference
from aif360.algorithms.preprocessing import DisparateImpactRemover
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

fake = Faker()


def colip(coltype, nrows, i):
    if coltype == "int":
        x = int(st.text_input(label="enter an integer", value=0, key="int"+str(i)))
        return [x]*nrows

    if coltype == "string":
        x2 = st.text_input(label="enter a string",
                           value="foo", key="str"+str(i))
        return [x2]*nrows

    if coltype == "sequence":
        start = int(st.text_input(
            label="enter start value", value=0, key="sta"+str(i)))
        increment = int(st.text_input(
            label="enter increment value", value=1, key="inc"+str(i)))
        op = [None]*nrows
        for i in range(nrows):
            op[i] = start+(i*increment)
        return op

    if coltype == "names":
        nametype = st.selectbox(
            "select name type", ('full name', 'first name', 'first name - male', 'first name - female', 'last name'), key="nt"+str(i))
        op = [None]*nrows
        if nametype == 'full name':
            for i in range(nrows):
                op[i] = fake.name()
        elif nametype == 'first name':
            for i in range(nrows):
                op[i] = fake.first_name()
        elif nametype == 'first name - male':
            for i in range(nrows):
                op[i] = fake.first_name_male()
        elif nametype == 'first name - female':
            for i in range(nrows):
                op[i] = fake.first_name_female()
        elif nametype == 'last name':
            for i in range(nrows):
                op[i] = fake.last_name()
        return op

    if coltype == "countries":
        op = [None]*nrows
        for i in range(nrows):
            op[i] = fake.country()
        return op

    if coltype == "list":
        lst = st.text_input(
            label="enter a list of things, comma seperated", value="foo, bar, baz", key="lab"+str(i))
        howlst = st.selectbox(
            "how do you want to generate the column", ('random', 'in sequence'), key="howl"+str(i))
        lst = lst.split(sep=",")
        llen = len(lst)
        if howlst == "random":
            lop = []
            for i in range(nrows):
                lop.append(lst[random.randint(0, llen-1)])
        elif howlst == "in sequence":
            lop = []
            for i in range(nrows):
                lop.append(lst[i % llen])

        return lop

    if coltype == "distribution":
        return 0


# dataset = st.file_uploader('Upload Data')
testoutput = []


page = st.sidebar.radio('What do you want to do?', ('Home', 'Bias Detection and Mitigation',
                                                    'New Data', 'More Data', 'Test'))
dataset = st.sidebar.file_uploader('Upload Data')

if dataset is not None:
    datatbl = pd.read_csv(dataset)
    st.sidebar.write("Uploaded dataset:")
    st.sidebar.dataframe(datatbl.head())

htmlp2 = '''
            <style>
        .floating-menu {
            font-family: sans-serif;
            background: black;
            padding: 5px;;
            width: 180px;
            z-index: 100;
            position: fixed;
            bottom: 0px;
            right: 0px;
        }
        
        .floating-menu a, 
        .floating-menu h3 {
            font-size: 0.9em;
            display: block;
            margin: 0 0.5em;
            color: white;
        }
        </style>
        <nav class="floating-menu">
            <h3>Data Tweaking Labs🧊</h3>
            <a href="https://github.com/synthdatagen" target="_blank">Github</a>
            <a href="https://docs.google.com/presentation/d/1H2cDNjSosFWmXeIfXjcs_qUbVFiEZqbJBaqiaUtnAws/edit?usp=sharing" target="_blank">Presentation</a>
            <a href="" target="_blank">Paper</a>
        
        </nav>
    '''
st.markdown(htmlp2, unsafe_allow_html=True)
if page == 'Home':
    htmlp1 = '''
            <style>
                .text {
                    color: #444444;
                    background: #FFFFFF;
                    text-shadow: 1px 0px 1px #CCCCCC, 0px 1px 1px #EEEEEE, 2px 1px 1px #CCCCCC, 1px 2px 1px #EEEEEE, 3px 2px 1px #CCCCCC, 2px 3px 1px #EEEEEE, 4px 3px 1px #CCCCCC, 3px 4px 1px #EEEEEE, 5px 4px 1px #CCCCCC, 4px 5px 1px #EEEEEE, 6px 5px 1px #CCCCCC, 5px 6px 1px #EEEEEE, 7px 6px 1px #CCCCCC;
                    color: #444444;
                    background: #FFFFFF;

                }
                    del {
                    background: #000;
                    color: #fff;
                    text-decoration:none;
                    }
                .bruh{
                    display:inline;
                    margin-right:10px;
                }


            </style>
            <h1 class="text">Data Tweaking Labs🧊</h1>
            <h3 class="text bruh"><i>Synthetic Data Generation</i></h3>
            <del>v0.0.1</del>
            '''

    st.markdown(htmlp1, unsafe_allow_html=True)

    st.write("Synthetic data, as the name suggests, is data that is artificially created rather than being generated by actual events. It is often created with the help of algorithms and is used for a wide range of activities, including as test data for new products and tools, for model validation, and in AI model training. Synthetic data is important for businesses due to three reasons: privacy, product testing and training machine learning algorithms.")
    st.subheader('Benefits of synthetic Data:')
    st.write('1. Overcoming real data usage restrictions: Real data may have usage constraints due to privacy rules or other regulations. Synthetic data can replicate all important statistical properties of real data without exposing real data, thereby eliminating the issue.')
    st.write('2. Creating data to simulate not yet encountered conditions: Where real data does not exist, synthetic data is the only solution.')
    st.write('3. Immunity to some common statistical problems: These can include item nonresponse, skip patterns, and other logical constraints.')
    st.write('4. Immunity to some common statistical problems: These can include item nonresponse, skip patterns, and other logical constraints.')
    st.subheader('Bias Mitigation:')
    st.write("For Bias detection our applications utilizes already established metrics and mitigation algorithms by IBM-AIF360. Further In our work we implement those on new datasets. Also we use this tool to interpret if AI models generate bias data. If yes we provide a mitigated data")


# Navigation of the App
if page == 'Bias Detection and Mitigation':
    st.subheader("Coming Soon ⚙")
    # BIAS DETECTION

    if dataset is not None:

        st.write(datatbl)
        datatbl = datatbl.dropna(how='any', axis=0)
        datatbl.info()

        datatbl = datatbl.dropna(how='any', axis=0)
        datatbl.info()

        # Drop unnecessary column
        datatbl = datatbl.drop(['Loan_ID'], axis=1)


# NEW DATA
elif page == 'New Data':

    st.subheader("Create your dataset:")

    ncols = int(st.text_input(label="Enter no. of cols", value=1))
    nrows = int(st.text_input(label="Enter no. of rows", value=10))
    colnames = [None]*ncols
    coltypes = [None]*ncols
    tblcols = [None]*ncols

    st.write("_________")
    st.markdown("<h4>Describe the columns:</h4>",
                unsafe_allow_html=True)

    for i in range(int(ncols)):
        colnames[i] = st.text_input(
            label="column "+f"{i}", key="coln"+f"{i}")
        coltypes[i] = st.selectbox("column type for column "+f"{i}"+" ("+f"{colnames[i]}"+")", (
            'int', 'string', 'sequence', 'names', 'countries', 'list', 'distribution'), key="colt"+f"{i}")
        tblcols[i] = colip(coltypes[i], nrows, i)
        st.write("____________")

    st.subheader("no of rows:")
    st.write(f"{nrows}")
    st.subheader("columns added:")
    for i in range(ncols):
        st.write("col "+f"{i}"+" - name: " +
                 colnames[i]+" | type: "+coltypes[i]+"\n")
    st.write("____________")
    st.markdown("<h3>Generated Table: </h3>", unsafe_allow_html=True)
    df = pd.DataFrame(tblcols)

    df2 = df.transpose()
    df2.columns = colnames
    st.table(df2.head())

elif page == 'More Data':
    st.subheader("Coming Soon ⚙")
elif page == 'Test':

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


# Hide Hamborgor and "Made with StreamLit"
hide_streamlit_style = """
            <style>
            # MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

# -------------------------------------------------------------------------------------

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
