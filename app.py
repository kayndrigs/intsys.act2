import streamlit as st
import plotly.express as px
import pandas as pd
import os 
import warnings
import base64
from email_validator import validate_email
import re
import plotly.figure_factory as ff
from streamlit_option_menu import option_menu
warnings.filterwarnings('ignore')


# Adds Favicon of PLM Logo
from PIL import Image
img = Image.open('plm.ico')

# Page icons
st.set_page_config(page_title="PLM Dashboard", page_icon=img,layout="wide")


def main():
    selected = option_menu(
        menu_title=None,
        options=["Home","Projects","Dashboard"],
        icons = ["house","book","bar-chart-line"],
        default_index=0,
        orientation="horizontal",
    )
    if selected == "Home":
        st.title("Welcome to Home Page")
        st.caption("Created by: ")
        st.caption("Bayono, Sean Marie B.")
        st.caption("Marcial, Jerriane Hillary Heart S.")
        st.caption("Ortega, Kazuhiro")
        st.caption("Rodrigo, Kayne Uriel")
        st.caption("Submitted to: Prof. Joel H. Cruz")
    if selected == "Dashboard":
        st.title("Welcome to Dashboard")
    if selected == "Projects":
        # Page Title
        st.title("Classification Model - Personal Identifiable Information Sorter")
        st.caption("Note:")
        st.caption("1. When uploading an external file, rename it to input.csv.")
        st.caption("2. Store all the random files in a single column.")
        st.caption("3. Change column name to random_values.")
        with open("plm_logo2.png", "rb") as f:
            data = base64.b64encode(f.read()).decode("utf-8")
            
            st.sidebar.markdown(
                f"""
                    <div style="display:table;margin-top:-15%;margin-left:0%;">
                        <img src="data:image/png;base64,{data}" width="425" height="100">
                    </div>
                """,
                unsafe_allow_html=True,
            )
        
        
        st.sidebar.header("Choose your filter: ")
        menu = ["Home","About"]
        choice = st.sidebar.selectbox("Menu",menu)
        # Adjust padding of div container in title
        # st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)
        fl = st.file_uploader(":file_folder: Upload a File",type=(["csv","txt","xlsx","xls"]))
        
        # Will read the csv or similar dataset file
        if fl is not None:
            filename = fl.name
            st.write(filename)
            df = pd.read_csv(filename, encoding="ISO-8859-1") #add encoding mechanism
            with st.expander("Current Random Data Values"):
                st.dataframe(df.T)
                
            st.subheader("Additional Input")
        
            with st.form(key='form1'):
                with st.expander("Updated Random Data Values"):
                    st.dataframe(df.T)
                text = st.text_input("Enter Valid Name/ Email/ Phone Number/ Birth date (Note: this cannot be reversed.)")
                submit_button = st.form_submit_button(label='Submit')
            
                if submit_button:
                    # fetching data from local directory
                    new_data = {"random_values":str(text)}
                    dataset_df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
                    dataset_df.to_csv(filename, index=False)
        else:
            # change the directory is none
            df = pd.read_csv("random_dataset4.csv", encoding="ISO-8859-1")
            with st.expander("Current Random Data Values"):
                st.dataframe(df.T)
                
            st.subheader("Additional Input")
            
            with st.form(key='form1'):
                with st.expander("Updated Random Data Values"):
                    st.dataframe(df.T)
                text = st.text_input("Enter Valid Name/ Email/ Phone Number/ Birth date (Note this cannot be reversed.)")
                submit_button = st.form_submit_button(label='Submit')
                
                if submit_button:
                    # fetching data from local directory
                    new_data = {"random_values":str(text)}
                    dataset_df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
                    dataset_df.to_csv("random_dataset4.csv", index=False)
                
        # Process
        phone_df = pd.read_excel('phonePrefix2.xlsx')
        dataset = []
        phonePrefix = []
        
        for i in df.values:
            dataset.extend(i)

        str_list = [str(j) for j in phone_df['phone_prefix']]
        phonePrefix = str_list
        
        #eliminates duplicates
        unique_dataset = list(dict.fromkeys(dataset))
        random_df = pd.DataFrame(unique_dataset) 
        random_df.columns = ['random_data']
        
        
        st.subheader("Sorted Dataset Result")  
        # with st.form(key='sortdata'):
        #     sort_dataset = st.form_submit_button(label='Sort Dataset')
        
        with st.expander('Results'):
            sorted_data = classification(unique_dataset,phonePrefix)
            fig = ff.create_table(sorted_data)
            st.plotly_chart(fig, use_container_width= True)
        

            csv = sorted_data.to_csv(index = False).encode('utf-8')
            st.download_button("Download Data",data=csv, file_name = "Category.csv", mime="text/csv",
                            help = 'Click here to download the data as a CSV file')
        
        

def classification(dataset,phonePrefix):
 # initialize values
    name = []
    cellphoneNumber = []
    dateBirth = []
    emailAddress = []
    invalid_info = []
    
    #token for checking email strings
    emailChars = ['@','.']
    
    # processes the dataset
    for i in dataset:
        
        # initially scans for @ and . characters
        checkEmail = [char for char in emailChars if(char in i)]
        
        # checks validity of phone number based on philippine prefix system
        checkMobileNum = [char for char in phonePrefix if(char in i[0:5])]
        
        # re
        name_string = i.replace(" ","")
        
        # we can't accurately predict if a name is a valid name, therefore, we implement all alphabets as a name
        if name_string.isalpha():
            capitalize_name = i.title()
            name.append(capitalize_name)
        
        # validate and append email
        elif checkEmail:
            try:
                v = validate_email(i)
                if v:
                    emailAddress.append(i)
            except:
                invalid_info.append(i)
                
        # validate and append date
        elif '/' in i:
            check_date = i.split('/')
            if len(check_date[0]) >= 1 and len(check_date[0]) < 3  and len(check_date[1]) >= 1 and len(check_date[1]) < 3 and len(check_date[2]) == 4:
                dateBirth.append(i)
            else: 
                invalid_info.append(i)
            
        # validate and append date
        elif checkMobileNum:
            cellphoneNumber.append(i)
            
        else:
            invalid_info.append(i)

    data = {'name':name,'cellphone_no.':cellphoneNumber,'date_of_birth':dateBirth,'email_address':emailAddress, 'invalid_inputs':invalid_info}
    result = pd.DataFrame.from_dict(data,orient='index')
    result = result.transpose()
    return result

if __name__ == '__main__':
    main()
