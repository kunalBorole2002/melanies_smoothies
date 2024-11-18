import streamlit as st
from snowflake.snowpark.functions import col
import requests
import json

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write("""Choose the fruits you want in your custom Smoothie!""")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be: ',name_on_order)
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up yo 5 ingredients',
    my_dataframe,
    max_selections = 5
)



if ingredients_list:
    ingredients_string = ''

    for each_fruit in ingredients_list:
        ingredients_string += each_fruit + ' '
        st.subheader(each_fruit + ' Nutrition Infromation')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+each_fruit)
        st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)

    #st.write(ingredients_string)
    my_insert_stmt = """insert into smoothies.public.orders(ingredients, name_on_order) 
                        values('"""+ingredients_string+"""','"""+name_on_order+"""')"""
    
    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered,'+name_on_order+'!', icon="✅")
        st.write(session.table('orders'))
    
