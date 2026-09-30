import streamlit as st

st.title("Smart AI Traveller APP")

destination=st.text_input("Enter destination")
travel_date=st.date_input("Enter the travel Date")
budget=st.number_input("Enter budget")
hotel_required=st.selectbox("Do you need hotel stay",("Yes","No"))

travel_type=st.selectbox(
    "Travel Type",
    ["Solo","Family","Couple","Business"]
    )

interest =st.multiselect(
    "Interest",
    ["Beach","Temple","Adventure","Nature"]
)
if st.button("Submit"):
    st.write("Budget Analysis")
    if budget < 10000:
        st.write("Low Budget")
        hotel_type="Budget Hotel"
    elif budget < 30000:
        st.write("Medium Budget")
        hotel_type="3_star Hotel"
    elif budget < 50000:
        st.write("Premium Budget")
        hotel_type="5_star Hotel"
    else:
        st.write("Luxury Budget")
    #st.write(f"Budget Category : {budget_category}")
    st.write(f"Recommended Stay : {hotel_type}")
    st.write(f"""
    AI Travel Agent Summary\n
    -----------------------
    Destination \t: {destination}\n
    Travel Date \t: {travel_date}\n
    Budget  \t: {budget}\n
    Hotel_Required \t: {hotel_required}\n
    """)

    st.write("## Travel Recommendation")

    if travel_type == "Solo":
        st.info("Explore local attractions and backpacking routes.")

    elif travel_type == "Family":
        st.info("Choose family-friendly hotels and sightseeing packages.")

    elif travel_type == "Couple":
        st.info("Romantic resorts and candle-light dinners recommended.")

    elif travel_type == "Business":
        st.info("Stay near business districts with conference facilities.")

    else:
      print("Happy Journey")

    st.balloons()
