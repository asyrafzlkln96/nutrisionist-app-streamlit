import streamlit as st
import google.generativeai as genai
import os

from dotenv import load_dotenv

load_dotenv()
from PIL import Image

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def get_gemini_response(input_prompt,image):
	model=genai.GenerativeModel('gemini-pro-vision')
	response=model.generate_content([input_prompt,image[0]])
	return response.text

def display_image(uploaded_file):
	if uploaded_file is not None:
		bytes_data= uploaded_file.getvalue()

		image_parts=[
			{
				"mime_type": uploaded_file.type,
				"data": bytes_data
			}
		]
		return image_parts
	else:
		raise FileNotFoundError("No File Uploaded!")

st.set_page_config(page_title="Calories Advisor App using Gemini AI")
st.header("Calories Advisor App")

uploaded_file=st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""
if uploaded_file is not None:
	image=Image.open(uploaded_file)
	st.image(image, caption="Uploaded Image", use_column_width=True)

submit = st.button("Tell me about the total calories and nutrition percentage")

input_prompt="""
You are an expert in nutritionist where you need to see the food items from the image
               and calculate the total calories, also provide the details of every food items with calories intake
               using below format

               1. Item 1 - no of calories
               2. Item 2 - how many percentage of Carbohydrate, Protein, Fiber, and other nutrition present
	       3. Item 3 - is the food healthy or non healthy? If non-healthy, please suggest a healthy food 
               ----
               ----


"""

## If submit button is clicked

if submit:
    image_data=display_image(uploaded_file)
    response=get_gemini_response(input_prompt,image_data)
    st.subheader("The Response is:")
    st.write(response)
