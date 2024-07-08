import streamlit as st 

st.sidebar.markdown('<h1><center>Connect with me', unsafe_allow_html=True)

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


#button styling
st.markdown("""<style>
.st-emotion-cache-1yzdwac {
    display: inline-flex;
    -webkit-box-align: center;
    align-items: center;
    -webkit-box-pack: inherit;
    justify-content: center;
    font-weight: 10;
    padding: 0.25rem 0.75rem;
    border-radius: 5rem;
    min-height: 2.5rem;
    margin: 0px;
    line-height: 1.6;
    text-decoration: none;
    width: 100%;
    user-select: none;
    background-color: rgb(13, 75, 75);
    color: rgb(255, 255, 255);
    border: 1px solid rgb(255, 7, 75);
}
</style>""", unsafe_allow_html=True)

git = st.sidebar.link_button('Github', 'https://github.com/Sharkytony', type='primary', use_container_width=True)


st.sidebar.link_button('LinkedIn', 'https://linkedin.com/in/anthonyrodrigues443', type='primary', use_container_width=True)


st.markdown(
    '<h1><font color="yellow"><center>Developer is currently working on enabling client camera access for Noah and RAG_Noah</font></h1><br><center>(If you have any suggestions for how to enable camera using js and return the live feed frames to python please do dm me on Linkedin )', unsafe_allow_html=True)

st.markdown(
    '<hr><h3>Vision of Noah 🎯 <br><br>  📌To have Real Time Computer Vision capabilities along with GPT. <br>📌To be integrated in AR glasses ',
      unsafe_allow_html=True)


