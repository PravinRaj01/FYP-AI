import streamlit as st
import firebase_admin
from firebase_admin import firestore

# ✅ Initialize Firestore Client
db = firestore.client()

st.title("💾 Saved Translations")

# ✅ Check if the user is logged in
if "user" not in st.session_state or not st.session_state["user"]:
    st.warning("⚠️ Please log in to view and manage saved translations.")
    st.stop()

# ✅ Fetch Translations for Logged-in User
try:
    # Fetch translations for the logged-in user
    translations_ref = db.collection("translations").where("user", "==", st.session_state["user"]).stream()
    translations = []

    for doc in translations_ref:
        data = doc.to_dict()
        translations.append({
            "id": doc.id,  # Keep this for deletion purposes but don't display it
            "Input Text": data.get("input_text", ""),
            "Output Text": data.get("output_text", "")
        })

    # ✅ Display Translations in a Table with a Delete Button Next to Each Row
    if translations:
        st.markdown("### Your Saved Translations")

        # Display table with delete buttons next to each row
        for index, translation in enumerate(translations):
            col1, col2, col3, col4 = st.columns([3, 3, 1, 1])

            with col1:
                st.markdown(f"**Input:** {translation['Input Text']}")
            with col2:
                st.markdown(f"**Output:** {translation['Output Text']}")
            with col3:
                # ✅ Delete Button (Row-Wise)
                if st.button(f"❌ Delete", key=f"delete_{translation['id']}"):
                    try:
                        db.collection("translations").document(translation['id']).delete()
                        st.success("✅ Translation successfully deleted!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error deleting translation: {e}")

            st.markdown("---")

    else:
        st.info("No saved translations found.")

except Exception as e:
    st.error(f"❌ Error loading saved translations: {e}")
