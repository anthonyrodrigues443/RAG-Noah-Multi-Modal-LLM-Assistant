import streamlit as st
st.markdown(
    '<h1><font color="yellow"><center>Developer is currently working on Noah', unsafe_allow_html=True)

st.markdown(
    '<hr><h3>Vision of Noah 🎯 <br><br>  📌To have Real Time Computer Vision capabilities along with GPT. <br>📌To be integrated in AR glasses ',
      unsafe_allow_html=True)


st.sidebar.markdown('<h1><center>Connect with developer', unsafe_allow_html=True)

style_image_dp = """
    max-width: 150px;
    height: auto;
    max-height: 150px;
    display: block;
    margin-left: auto;
    margin-right: auto;
    border-radius: 50%;
"""


st.sidebar.markdown(
    f'<img src="{"https://media.licdn.com/dms/image/D4E03AQGREUZ3djPpog/profile-displayphoto-shrink_400_400/0/1685977776362?e=1724889600&v=beta&t=16HVxWzwc5clVOIpWqIqgq6FuTPViYf-g2hZPAmZuyc"}" style="{style_image_dp}">',
    unsafe_allow_html=True)

git = st.sidebar.link_button('Github', 'https://github.com/Sharkytony', type='primary', use_container_width=True)


st.sidebar.link_button('LinkedIn', 'https://linkedin.com/in/anthonyrodrigues443', type='primary', use_container_width=True)