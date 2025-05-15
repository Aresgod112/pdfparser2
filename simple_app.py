import streamlit as st

st.title("Simple Streamlit App")
st.write("This is a simple Streamlit app without any custom dependencies.")

# Add a button
if st.button("Click me"):
    st.success("Button clicked!")

# Add a text input
name = st.text_input("Enter your name")
if name:
    st.write(f"Hello, {name}!")
