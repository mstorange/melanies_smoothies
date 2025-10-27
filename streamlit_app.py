# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app --> see documentation: magic (st.write can plot any data types!)
st.title(":cup_with_straw: Customise your :orange[smoothie!] :balloon:")
st.write(
  """Choose the fruits **you** want in your custom _smoothie_!
  """
)

nameonorder = st.text_input('Name on Smoothie')
st.write('The name on your smoothie will be: ', nameonorder)


# connection zur Snowflake database
cnx = st.connection("snowflake")
session = cnx.session() 
my_df = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"),col("SEARCH_ON")
#st.dataframe(data=my_df, use_container_width=True) # erst das hier zeigt den Table in der App
pd_df = my_df.to_pandas()
st.dataframe(pd_df)

# wir bauen nun einen multiselect GUI, welcher den snowflake table hinterlegt hat und direkt darauf zugreift!
ingredients_list = st.multiselect('Choose up to 5 ingredients: ', my_df, max_selections=5)

# unsere Auswahl printen
if ingredients_list:
    #st.write(ingredients_list) # gibt es als json aus
    #st.text(ingredients_list)
    # wir wollen die list in einen string umwandeln und dann plotten (looks better)
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen, ' is ', search_on, '.')
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)

    insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
    values ('""" + ingredients_string + """', '"""+nameonorder+"""')"""
    #st.write(insert_stmt)
    #st.stop()

    # submit button so that not each chosen entry from multiselect df is automatically added
    insertbutton = st.button('Submit order')

    if insertbutton:
        session.sql(insert_stmt).collect()

        st.success('Your smoothie is ordered!', icon="✅") # success simply adds green bg

# new section to display smoothiefroot nutrition information
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)
    
    
