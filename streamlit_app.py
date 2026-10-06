# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your Smoothie :balloon:")
st.write(
    """Choose the fruits you want in your custom Smoothie!"""
)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table(
    "smoothies.public.fruit_options"
).select(col("FRUIT_NAME"))

# st.dataframe(data=my_dataframe, use_container_width=True)

name_on_order = st.text_input("Name On Smoothie:")
st.write("Name on smoothie is: ", name_on_order)

ingredient_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe,
    max_selections=5
)

if ingredient_list:

    ingredients_string = ""

    for fruit in ingredient_list:
        ingredients_string += fruit + " "
        st.subheader(fruit + 'Nutrition Information')
        

    # Call the Smoothie API
    smoothiefroot_response = requests.get(
        "https://my.smoothiefroot.com/api/fruit/" + fruit)

    sf_df = st.dataframe(
        data=smoothiefroot_response.json(),
        use_container_width=True
    )

    # Create INSERT statement
    my_insert_stmt = """INSERT INTO smoothies.public.orders(name_on_order, ingredients)
                        VALUES ('""" + name_on_order + "', '" + ingredients_string + "')"

    # st.write(my_insert_stmt)

    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success(
            f"Your Smoothie is ordered, {name_on_order}!",
            icon="✅"
        )
