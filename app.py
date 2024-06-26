import streamlit as st
from PIL import Image
import io

from Edge_extraction.extract import sobel, canny, xdog

st.title('Image Colorisation App')


uploaded_file = st.file_uploader("Choose a file", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:

    st.markdown("### Edge extractors")
    
    image = Image.open(uploaded_file)

    # Options for processing image
    option = st.selectbox(
        'Choose an edge extractor to apply',
        ('Canny edge extractor', 'Sobel edge extractor', 'Xdog edge extractor')
    )

    if option == 'Canny edge extractor':
        thresh1 = st.slider('Threshold 1', min_value=0, max_value=255, value=100)
        thresh2 = st.slider('Threshold 2', min_value=0, max_value=255, value=200)
    elif option == 'Sobel edge extractor':
        thresh = st.slider('Threshold', min_value=0, max_value=255, value=100)
    elif option == 'Xdog edge extractor':
        gamma = st.slider('Gamma', min_value=0.0, max_value=1.0, value=0.95, step=0.05)
        sigma = st.slider('Sigma', min_value=0.1, max_value=10.0, value=1.0, step=0.1)
        k = st.slider('K', min_value=1, max_value=10, value=3)
        epsilon = st.slider('Epsilon', min_value=-1.0, max_value=0.0, value=-0.05, step=0.01)
        phi = st.slider('Phi', min_value=1, max_value=300, value=100)

    if st.button('Apply'):
        modified_image = None
        if option == 'Canny edge extractor':
            modified_image = canny(image, thresh1=thresh1, thresh2=thresh2)
        elif option == 'Sobel edge extractor':
            modified_image = sobel(image, thresh=thresh)
        elif option == 'Xdog edge extractor':
            modified_image = xdog(image, gamma=gamma, sigma=sigma, k=k, epsilon=epsilon, phi=phi)

        col1, col2 = st.columns(2) 
        col1.image(image, caption='Original Image', use_column_width=True)

        col2.image(modified_image, caption='Extracted edges', use_column_width=True)


    st.markdown("---")
    st.markdown("### Compare Edge Extractors")

     # Checkboxes for showing/hiding edge methods
    show_original = st.checkbox('Original', value=True)
    show_canny = st.checkbox('Canny Edge Detector', value=True)
    show_sobel = st.checkbox('Sobel Edge Detector', value=True)
    show_xdog = st.checkbox('XDoG Edge Detector', value=True)

    # Button to apply selected methods
    if st.button('Compare'):
        images = {}
        if show_original:
            images['Original'] = image
        if show_canny:
            images['Canny'] = canny(image)
        if show_sobel:
            images['Sobel'] = sobel(image)
        if show_xdog:
            images['XDoG'] = xdog(image)

        if images:
            # Display images in a grid layout
            cols = st.columns(len(images))
            for col, (key, img) in zip(cols, images.items()):
                col.image(img, caption=f'{key} Edge Detection', use_column_width=True)