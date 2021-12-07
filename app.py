from bokeh.models import DataTable, TableColumn, PointDrawTool, ColumnDataSource, CustomJS
from bokeh.plotting import figure, output_file, show, Column
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from streamlit_bokeh_events import streamlit_bokeh_events
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.plotting import figure
import subprocess
import sys
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
import plotly.express as px
import numpy as np
import random
import os
from faker import Faker
from streamlit_ace import st_ace
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
import ruamel.yaml

# Gretel
from getpass import getpass
from gretel_client import configure_session, ClientConfig
from gretel_client.helpers import poll

import json
from smart_open import open
import yaml

# ------------------------------------------------------------------------------------------------

fake = Faker()


def nameresolver():

    return 0


def colip(coltype, nrows, i, tblcols):
    # for cc in colnames:
    #     pass
    #     # eval()
    if coltype == "Number":
        x = int(st.text_input(label="enter an integer", value=0, key="int"+str(i)))
        return [x]*nrows

    if coltype == "String":
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

    if coltype == "Names":
        nametype = st.selectbox(
            "select name type", ('Full name', 'First name', 'First name - male', 'First name - female', 'Last name'), key="nt"+str(i))
        op = [None]*nrows
        if nametype == 'Full name':
            for i in range(nrows):
                op[i] = fake.name()
        elif nametype == 'First name':
            for i in range(nrows):
                op[i] = fake.first_name()
        elif nametype == 'First name - male':
            for i in range(nrows):
                op[i] = fake.first_name_male()
        elif nametype == 'First name - female':
            for i in range(nrows):
                op[i] = fake.first_name_female()
        elif nametype == 'Last name':
            for i in range(nrows):
                op[i] = fake.last_name()
        return op

    if coltype == "Countries":
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
        st.write("Coming soon ⚙")
        return 0

    if coltype == "Python Expression":
        content = st_ace(language="python", theme="twilight", auto_update=True,
                         wrap=True, min_lines=1, max_lines=2, key="code"+str(i))
        if content != "":
            return eval(content)


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
    # htmlp1 = '''
    #         <style>
    #             .text {
    #                 color: #000000;
    #                 -webkit-text-stroke: 0.2px white;
    #                 text-shadow: 1px 0px 1px #CCCCCC, 0px 1px 1px #EEEEEE, 2px 1px 1px #CCCCCC, 1px 2px 1px #EEEEEE, 3px 2px 1px #CCCCCC, 2px 3px 1px #EEEEEE, 4px 3px 1px #CCCCCC, 3px 4px 1px #EEEEEE, 5px 4px 1px #CCCCCC, 4px 5px 1px #EEEEEE, 6px 5px 1px #CCCCCC, 5px 6px 1px #EEEEEE, 7px 6px 1px #CCCCCC;

    #             }
    #                 del {
    #                 background: #000;
    #                 color: #fff;
    #                 text-decoration:none;
    #                 }
    #             .bruh{
    #                 display:inline;
    #                 margin-right:10px;
    #             }

    #         </style>
    #         <h1 class="text">Data Tweaking Labs🧊</h1>
    #         <h3 class="text bruh"><i>Synthetic Data Generation</i></h3>
    #         <del>v0.0.1</del>
    #         '''

    # st.markdown(htmlp1, unsafe_allow_html=True)

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

    st.markdown("""
    <h2>New Data:</h2>
    <h5 style="font-style: italic;">Generate new data based on the distribution furnished by the user. The product further gives us insights into the bias that the dataset has and ways to mitigate it.</h5>""", unsafe_allow_html=True)

    st.subheader("Create your dataset:")

    ncols = int(st.text_input(label="Enter no. of cols", value=1))
    nrows = int(st.text_input(label="Enter no. of rows", value=10))
    colnames = [None]*ncols
    coltypes = [None]*ncols
    colsubtypes = [None]*ncols
    colflags = [None]*ncols
    tblcols = [None]*ncols

    st.write("_________")
    st.markdown("<h4>Describe the columns:</h4>",
                unsafe_allow_html=True)

    for i in range(int(ncols)):
        with st.expander(label="Column "+f"{i}"):
            colnames[i] = st.text_input(
                label="Column name", key="coln"+f"{i}")
            coltypes[i] = st.selectbox("Column type:",
                                       ("Numerical(Float)", "Categorical(eg: Names, Countries)"), key="colt"+f"{i}")
            if coltypes[i] == "Numerical(Float)":
                colsubtypes[i] = st.selectbox("Describe the column:", (
                    'Number', 'Distribution', 'Python Expression'), key="colst"+f"{i}")
            elif coltypes[i] == "Categorical(eg: Names, Countries)":
                colsubtypes[i] = st.selectbox("Describe the column: "+f"{i}"+" ("+f"{colnames[i]}"+")", (
                    'Blank', 'String', 'Distribution', 'Names', 'Countries', 'Python Expression'), key="colst"+f"{i}")
            tblcols[i] = colip(colsubtypes[i], nrows, i, tblcols)

    st.write("____________")
    st.markdown("<h4>Columns added:</h4>",
                unsafe_allow_html=True)
    with st.expander(label=""):
        for i in range(ncols):
            st.write("col "+f"{i}"+" - name: " +
                     colnames[i]+" | type: "+colsubtypes[i]+"\n")
    st.write("____________")
    st.markdown("<h3>Generated Table: </h3>", unsafe_allow_html=True)
    df = pd.DataFrame(tblcols)

    df2 = df.transpose()
    df2.columns = colnames
    rowstoshow = st.slider(label="no. of rows to show in preview",
                           min_value=5, max_value=10)
    st.table(df2.head(rowstoshow))

    if st.button(label="Download Dataset"):
        df2.to_csv("generateddata.csv")
        st.write("Dataset downloaded ✔")
        st.caption("check your project folder")

# SYNTHETIC DATA GENERATION METHODS ------------------------------------------------------------------------------

elif page == 'More Data':

    st.title("🗃️More Data")
    st.subheader("Generate Synthetic Data using one of the following methods:")

    modelchoice = st.selectbox('Start by selecting a model',
                               ('Click to choose', 'Gretel', 'CTGAN', 'TGAN'))

# Gretal--------------------------------------------------------------------------------------------------------------

    if modelchoice == 'Gretel':

        # About
        with st.expander("About Gretal"):
            st.image(
                "https://uploads-ssl.webflow.com/5ea8b9202fac2ea6211667a4/5eb59ce904449bf35dded1ab_gretel_wordmark_gradient.svg")

            st.write("""Generate synthetic data to augment your datasets.
                This can help you create AI and ML models that perform
                and generalize better, while reducing algorithmic bias.""")

            st.write("""No need to snapshot production databases to share with your team.
                Define transformations to your data with software,
                and invite team members to subscribe to data feeds in real-time""")

        nrecords = int(st.number_input(label="Number or Records", value=1000))

        yaml = ruamel.yaml.YAML()
        yaml.preserve_quotes = True
        with open('input.yaml') as fp:
            data = yaml.load(fp)
        fp.close()
        # no need to iterate further
        data['models'][0]['synthetics']['generate']['num_records'] = nrecords
        with open('input.yaml', 'w') as fp:
            fp = yaml.dump(data, fp)

        if st.button("Generate"):
            subprocess.call('python gretal.py')
            # creationflags=subprocess.CREATE_NEW_CONSOLE)
            st.write("Synthetic Data is being Generated")
        if st.button("Show Generated Data"):
            if os.path.exists("D:\Development\Codies\Programming\Python\StreamLit\synthetic_data.csv") == True:
                st.write("Dataset Generated")
                syntheddata = pd.read_csv(
                    "D:\Development\Codies\Programming\Python\StreamLit\synthetic_data.csv")
                st.dataframe(syntheddata)
            else:
                st.write("Dataset not yet Generated")

        # syntheddata = pd.read_csv(
        #     "D:\Development\Codies\Programming\Python\StreamLit\synthetic_data.csv")
        # cmpr = pd.read_csv(
        #     "D:\Development\Codies\Programming\Python\StreamLit\zraining_data.csv")
        # cmpr1 = cmpr.select_dtypes(include=np.number)
        # cmpr2 = syntheddata.select_dtypes(include=np.number)
        # for i in range(len(cmpr)):
        #     sc1 = cmpr1.iloc[:, i].sample(n=100, replace=True)
        #     sc2 = cmpr2.iloc[:, i].sample(n=100, replace=True)
        # plt.scatter(sc1, sc2, c=['#1f77b4', '#ff7f0e'])
        # plt.pyplot.show()

        if os.path.exists("D:\Development\Codies\Programming\Python\StreamLit\synthetic_data.csv") == True:
            if st.button("Generate Plots"):
                pass


# CTGAN --------------------------------------------------------------------------------------------------------------
    if modelchoice == 'CTGAN':
        with st.container():

            with st.expander("About CTGAN"):
                st.image(
                    "https://sdv.dev/ctgan.svg")

                st.write("""CTGAN is a collection of Deep Learning based Synthetic Data Generators for single table data,
                which are able to learn from real data and generate synthetic clones with high fidelity.
                Currently, this library implements the CTGAN and TVAE models proposed in
                the Modeling Tabular data using Conditional GAN paper.""")

        st.button("Generate")

    if modelchoice == 'TGAN':
        with st.expander("About TGAN"):

            st.image("https://sdv.dev/rdt.svg")

            st.write("""TGAN is a tabular data synthesizer.
                It can generate fully synthetic data from real data.
                Currently, TGAN can generate numerical columns and categorical columns.""")

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
