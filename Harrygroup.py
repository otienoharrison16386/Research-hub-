import streamlit as st
import pandas as pd
import os
from datetime import datetime

GROUP_PIN = "harry123"
ALLOWED_NAMES = ["Harrison", "Amudavi", "Makena", "Cameraman", "Gideon", "Ishmael", "John mark", "Mjshakers", "MrMan", "Kinara"]
# --------------------------

os.makedirs("uploads", exist_ok=True)
st.set_page_config(page_title="Private Research Hub", page_icon="🔒", layout="centered")

if "authed" not in st.session_state:
    st.session_state.authed = False

if not st.session_state.authed:
    st.title("🔒 Private Research Group")
    st.caption("Access for 10 members only")
    pin = st.text_input("Enter Group Password", type="password", placeholder="harry123")
    if st.button("Enter Hub", use_container_width=True):
        if pin == GROUP_PIN:
            st.session_state.authed = True
            st.rerun()
        else:
            st.error("Wrong password - ask Harrison")
    st.stop()

st.title("📚 Research Hub")
st.caption("10 members: Harrison, Amudavi, Makena, Cameraman, Gideon, Ishmael, John mark, Mjshakers, MrMan, Kinara")

DATA_FILE = "data.csv"
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Name","Title","FilePath","FileName","Date"])

with st.form("upload_form", clear_on_submit=True):
    st.subheader("Upload Research")
    name = st.selectbox("Select your name", ALLOWED_NAMES)
    title = st.text_input("Research Title / Topic")
    file = st.file_uploader("Upload ANY file", type=None)
    submit = st.form_submit_button("Upload", type="primary", use_container_width=True)
    if submit:
        if not file or not title.strip():
            st.warning("Add title and file")
        else:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_name = "".join(c for c in file.name if c.isalnum() or c in "._- ")
            save_path = f"uploads/{ts}_{safe_name}"
            with open(save_path, "wb") as f:
                f.write(file.getbuffer())
            row = {"Name": name, "Title": title.strip(), "FilePath": save_path, "FileName": file.name, "Date": datetime.now().strftime("%Y-%m-%d %H:%M")}
            df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success(f"Uploaded as {name}!")
            st.rerun()

st.divider()
st.subheader(f"All Uploads ({len(df)})")
if len(df) > 0:
    filter_name = st.selectbox("Filter by member", ["All"] + ALLOWED_NAMES)
    view_df = df if filter_name == "All" else df[df["Name"] == filter_name]
    view_df = view_df.iloc[::-1]
    for idx, row in view_df.iterrows():
        with st.container(border=True):
            c1, c2 = st.columns([3,1])
            with c1:
                st.markdown(f"**{row['Title']}**")
                st.caption(f"👤 {row['Name']} | 📅 {row['Date']} | 📄 {row['FileName']}")
            with c2:
                if os.path.exists(row['FilePath']):
                    with open(row['FilePath'], "rb") as f:
                        st.download_button("Download", f, file_name=row['FileName'], key=f"dl_{idx}_{ts}", use_container_width=True)
else:
    st.info("No uploads yet.")

if st.button("Logout"):
    st.session_state.authed = False
    st.rerun()
