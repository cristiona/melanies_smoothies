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

import requests  
smoothiefroot_response = requests.get("[https://my.smoothiefroot.com/api/fruit/watermelon](https://my.smoothiefroot.com/api/fruit/watermelon)")  
st.text(smoothiefroot_response)


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

    #     # Update the rows that were checked
    # for _, order in editable_df.iterrows():

    #     if order["ORDER_FILLED"]:
    #         session.sql("""
    #             UPDATE smoothies.public.orders
    #             SET ORDER_FILLED = TRUE
    #         """).collect()
        

# st.write(editable_df)


# if editable_df:
    
# st.dataframe(orders_filled)
# st.write(order_filled)
