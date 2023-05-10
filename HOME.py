import streamlit as st
from PIL import Image

image = Image.open('IZANAMI.png')
st.image(image, use_column_width=True)

tab1, tab2, tab3 = st.tabs(["Top", "ご意見・ご要望", "バージョン履歴"])

# with tab1:
with tab1:
    st.header("TOP")
    st.write('Comming Soon!')

# with tab2:
with tab2:
    st.write("""
        <iframe src="https://docs.google.com/forms/d/e/1FAIpQLScdZ7GQtJbOq9keBHqWbfkEiUoo60vOmSZznBbwvq84NmV76A/viewform?embedded=true" 
            width="640" height="1108" frameborder="0" marginheight="0" marginwidth="0">
            読み込んでいます…
        </iframe>
    """, unsafe_allow_html=True)
with tab3:
    st.header("Ver 1.00")
    st.write('Izanami をリリースしました。')
