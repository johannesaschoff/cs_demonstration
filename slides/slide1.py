import streamlit as st
import pandas as pd
import requests
import ast

st.set_page_config(layout="wide")

@st.cache_data
def fetch_pptx(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to fetch the PPTX. Status code: {response.status_code}")

def render():
    st.title("Craftsmanship and Production")
    st.markdown("**Project types**")
    st.write("- Butchery")
    st.write("- Bakery")
    st.write("- Kitchen")
    st.write("- Woodwork")
    st.write("- Sewing")
    st.write("- Metal Construction Workshop")

    # Section: Slideshow
    st.markdown("**Pitchdeck Preview**")
    columns = st.columns(6)

    for i in range(6):
        with columns[i]:
            st.image(
                f"https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image{i + 1}.png",
                use_column_width=True
            )
            st.image(
                f"https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image{i + 7}.png",
                use_column_width=True
            )

    pptx_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/Pitch.pptx"
    try:
        pptx_data = fetch_pptx(pptx_url)
        st.download_button(
            label="Download PPTX File",
            data=pptx_data,
            file_name="PitchDeck.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        )
    except Exception as e:
        st.error(f"Could not fetch the PPTX file: {e}")

    # Section: Corporate Dataset
    st.markdown("**Matching Corporates**")
    csv_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/dataframe_corporates_with_logos.csv"
    excel_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/craftmanship_production.xlsx"

    try:
        df = pd.read_csv(csv_url)
        df = df[df["Craftsmanship and production"] == True]

        df["Industries"] = df["Industries"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

        st.dataframe(
            df,
            hide_index=True,
            use_container_width=True
        )

        response = requests.get(excel_url)
        if response.status_code == 200:
            excel_data = response.content
            st.download_button(
                label="Download data as Excel",
                data=excel_data,
                file_name="Craftsmanship_and_Production.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        else:
            st.error(f"Failed to fetch the Excel file. Status code: {response.status_code}")

    except Exception as e:
        st.error(f"Failed to load the dataset: {e}")

    # Sentiment annotation
    st.markdown("**Annotate Sentiments**")
    sentiment_data = [
        {"tweet": "What a great new feature! I love it!", "author": "John Rose", "sentiment": "🤩 Positive"},
        {"tweet": "I don't like this feature. It's not useful. I prefer chart improvements.", "author": "Will Hangu", "sentiment": ""},
        {"tweet": "Wow, the Streamlit team can be proud! What an achievement!", "author": "Luca Masucco", "sentiment": ""},
        {"tweet": "The recent ChatGPT breakthrough is really exciting.", "author": "Adrien Tree", "sentiment": ""},
    ]

    sentiment_df = pd.DataFrame(sentiment_data)
    sentiment_df.sentiment = sentiment_df.sentiment.astype("category")
    sentiment_df.sentiment = sentiment_df.sentiment.cat.add_categories(("☯ Neutral", "😤 Negative"))

    annotated_sentiments = st.data_editor(
        sentiment_df, hide_index=True, use_container_width=True, disabled=["tweet", "author"]
    )

    st.download_button(
        "⬇️ Download sentiment annotations as CSV",
        annotated_sentiments.to_csv(index=False).encode("utf-8"),
        "annotated_sentiments.csv",
        mime="text/csv",
    )

render()
