# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app!
st.title(":cup_with_straw: Customize your smoothie! :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#t.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#Convert Snowpark to pandas
pd_df = my_dataframe.to_pandas()
#st.dataframe(data=pd_df, use_container_width=True)
#st.stop()

name_on_order= st.text_input("Name on the smoothie")
st.write(name_on_order)

ingredient_list = st.multiselect("Chose upto five Fruits",my_dataframe,max_selections=5)
if ingredient_list:
    ingredient_str = ''
    for fruit in ingredient_list:
        ingredient_str += fruit + ' '

        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit,'SEARCH_ON'].values[0]
        if search_on :
            st.write("The Search value for " + fruit + " is " + search_on + ".")
            
        else:
            st.write("The Search value for " + fruit + " is not found.")
            search_on = fruit
        

        

        st.subheader(fruit + 'Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+search_on)
        sf_df=st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)
    

    st.text(ingredient_str)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredient_str + """' ,'""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()
    time_to_insert=st.button("submit")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered'+' '+name_on_order, icon="✅")


    
