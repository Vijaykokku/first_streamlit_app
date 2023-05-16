import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Dinner')

streamlit.header('Breakfast Menu')

streamlit.text('🥣 Omega 3 & Blueberryoatmeal')
streamlit.text('🥗 Kale,Spinach & Rocket smoothie')
streamlit.text(' 🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avakado Toast')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

#import pandas
my_fruit_list=pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

def get_fruityvice_data(this_fruit_choice):
    #import requests
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
    #take the json version of response and normalize it 
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized
#New Sectrion to display fruityvice apin response
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
      streamlit.error("please select a fruit to get information.")
  else:
    back_from_function=get_fruityvice_data(fruit_choice)
    #output it the screen as table 
    streamlit.dataframe(back_from_function)
except URLError as e:
  streamlit.error()
  
#dont run anything past while we trouble shooting
#streamlit.stop()

#import snowflake.connector
streamlit.header("The fruit loadn list contains:")
#Snowflake-related functions
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall()
#Add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    #my_cur = my_cnx.cursor()
    #my_cur.execute("SELECT * from fruit_load_list")
    my_data_rows =get_fruit_load_list()
    #streamlit.header("The fruit loadn list contains:")
    streamlit.dataframe(my_data_rows)
streamlit.stop()
#allow end user to add the fruit to the list
def insert_row_snowflake(new_fruit):
   with my_cnx.cursor() as my_cur:
    my_cur.execute("insert into fruit_load_list values('"+kiwi+"')")
    return "Thanks for adding" +new_fruit   
ad_my_fruit=streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a fruit to the list'):
     my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
     back_from_function=insert_row_snowflake(add_my_fruit)
    #output it the screen as table 
     streamlit.text(back_from_function)   

#this will not work correctly but go it with for now
#my_cur.execute("insert into fruit_load_list values('from streamlit')")


