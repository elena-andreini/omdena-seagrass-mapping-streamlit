import strealit as st

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """


def make_font_poppins():
    with open("src/styles.css") as css:
        st.markdown(f'<style>{css.read()}</style>' , unsafe_allow_html= True)

    # Render the custom CSS style
    st.markdown("<link href='https://fonts.googleapis.com/css2?family=Poppins:wght@500&display=swap' rel='stylesheet'>", unsafe_allow_html=True)

    # Hide Streamlit style
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

########

def display_image(url, caption=None):
    st.markdown("<p></p>",unsafe_allow_html=True)
    image_url = url
    st.image(image_url, caption=caption, use_column_width=True)
    st.markdown("<p></p>",unsafe_allow_html=True)

########
def homepage():
    # st.title("Home Page")
    # st.write("Welcome to the home page!")
    ################### HEADER SECTION #######################
    display_image('https://cdn-images-1.medium.com/max/800/0*vBDO0wwrvAIS5e1D.png')
    
    st.markdown("<h1 style='text-align: center; color: auto;'>Mapping Seagrass Meadows with Satellite Imagery and Computer Vision</h1>",
                unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center; color: #FFFFD0; font-family: Segoe UI;'>A web-based pixel-level Classification Model for identifying seagrass in sattelite images</h3>", unsafe_allow_html=True)
    
    display_image('https://upload.wikimedia.org/wikipedia/commons/4/45/Sanc0209_-_Flickr_-_NOAA_Photo_Library.jpg')

def about():
    # st.title("About Page")
    # st.write("This is the about page.")
    # from page_utils import font_modifier, display_image
    
    display_image('https://cdn-images-1.medium.com/max/800/0*vBDO0wwrvAIS5e1D.png')
    
    ################### INFORMATION SECTION #######################
    st.header('Challenge Background')
    st.markdown(
                """
                <style>
                .tab {
                    text-indent: 0px;  /* adjust as needed */
                    text-align: justify;  /* Add this line */
                }
                </style>
                <div class="tab" style="text-align=justify;">Seagrasses, forming vast marine meadows in shallow salt waters from tropics to the Arctic, are vital for biodiversity. They provide habitats for fish and shellfish, supporting local coastal economies. Moreover, they stabilise sediment, absorb wave energy, and contribute significantly to carbon absorption, making them crucial allies in combating climate change.</div>
                <p></p>
                
                """
                ,unsafe_allow_html=True)
    
    st.header('The Problem')
    st.markdown(
                """
                <style>
                .tab {
                    text-indent: 0px;  /* adjust as needed */
                    text-align: justify;  /* Add this line */
                }
                </style>
                <div class="tab" style="text-align=justify;">The declining health of Posidonia oceanica meadows in the Mediterranean Sea is a pressing concern, attributed to climate change and various human activities. These meadows, crucial for their ecological significance, are in jeopardy due to factors such as warming, ocean acidification, coastal urban development, fishing, and aquaculture. This decline has led to a substantial loss of goods and services provided by these ecosystems. While P. oceanica is the most vital and studied seagrass species in the region, there has been a limited effort to collate and provide a comprehensive distribution of these meadows. This lack of information impedes our ability to effectively address the regression of these critical habitats.</div>
                <p></p>
                
                """
                ,unsafe_allow_html=True)
    
    st.header('Goal of the Project')
    st.markdown(
                """
                <style>
                .tab {
                    text-indent: 0px;  /* adjust as needed */
                    text-align: justify;  /* Add this line */
                }
                </style>
                <div class="tab" style="text-align=justify;">Our project aims to develop accessible and efficient methods for mapping seagrass meadows using readily available satellite imagery and  computer vision. We envision these results as valuable tools for long-term seagrass monitoring, including tracking restoration and replanting efforts. Our primary goal is to create a pixel-level classification and segmentation model to map seagrass distribution, with a focus on the Mediterranean, especially Italian waters. Using computer vision techniques, we'll identify seagrass regions by analyzing satellite images and classifying pixels based on data from public databases indicating seagrass presence or absence. An essential aspect of this project involves comparing our model's outcomes with established habitat suitability models for P. oceanica presence. Habitat suitability models predict species presence in a location by analyzing the relationship between observed occurrences and environmental conditions. They assess marine habitat status, forecast species distribution changes from human and environmental impacts, and guide restoration efforts by identifying optimal areas.</div>
                <p></p>
                
                """
                ,unsafe_allow_html=True)
    
    # font_modifier.make_font_poppins()
    make_font_poppins()
def classify():
    # st.title("Contact Page")
    # st.write("Contact us at example@example.com")
    display_image('https://cdn-images-1.medium.com/max/800/0*vBDO0wwrvAIS5e1D.png')
    # st.title("Mapping seagrass with Satellite Imagery and Deep Learning")
    img_file = st.file_uploader("Choose an image to classify", type=["tif"])
    main(img_file)

def guide():
    display_image('https://cdn-images-1.medium.com/max/800/0*vBDO0wwrvAIS5e1D.png')

def datasets():
    display_image('https://cdn-images-1.medium.com/max/800/0*vBDO0wwrvAIS5e1D.png')

def repository():
    display_image('https://cdn-images-1.medium.com/max/800/0*vBDO0wwrvAIS5e1D.png')

def gallery():
    display_image('https://cdn-images-1.medium.com/max/800/0*vBDO0wwrvAIS5e1D.png')
