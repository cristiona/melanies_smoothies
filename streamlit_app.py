# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col
from snowflake.snowpark.functions import when_matched

# Write directly to the app
st.title(":cup_with_straw: Pending Smoothie Order:cup_with_straw:")
st.write("Orders that need to be filled.")

cnx = st.connection("snowflake")
session = cnx.session()




data = session.table("smoothies.public.orders")
# st.dataframe(data)
orders_filled = data.filter(col("ORDER_FILLED") ==0).collect()

if orders_filled:
    
    editable_df = st.data_editor(orders_filled)

    submitted = st.button("Submit order")
    
    if submitted:
        # st.success("Someone clicked the button ")
    
        og_dataset = session.table("smoothies.public.orders")
        edited_dataset = session.create_dataframe(editable_df)
        og_dataset.merge(edited_dataset
                             , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                             , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                            )
        st.success("Orders updated successfully!")

else:
    st.success('No pending orders')


smoothiefroot_response = requests.get(
    "https://my.smoothiefroot.com/api/fruit/watermelon"
)
# st.text(smoothiefroot_response.json())

sf_df = st.dataframe(data = smoothiefroot_response.json(), use_container_width = True)
