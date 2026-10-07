import json
from datetime import datetime
from pathlib import Path

import streamlit as st

APP_TITLE = "Smart Food Management System"
DATA_FILE = Path(__file__).with_name("inventory.json")

DEFAULT_INVENTORY = [
    {
        "id": "FD001",
        "name": "Milk",
        "category": "Dairy",
        "quantity": 10,
        "unit": "litres",
        "purchase_date": "2026-10-01",
        "expiry_date": "2026-10-03",
    },
    {
        "id": "FD002",
        "name": "Rice",
        "category": "Grains",
        "quantity": 25,
        "unit": "kg",
        "purchase_date": "2026-09-15",
        "expiry_date": "2027-09-15",
    },
]


def load_inventory():
    if DATA_FILE.exists():
        try:
            with DATA_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)
                if isinstance(data, list):
                    return data
        except (json.JSONDecodeError, OSError):
            pass
    save_inventory(DEFAULT_INVENTORY)
    return DEFAULT_INVENTORY.copy()


def save_inventory(inventory):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(inventory, file, indent=2)


st.set_page_config(page_title=APP_TITLE, layout="wide")

if "inventory" not in st.session_state:
    st.session_state.inventory = load_inventory()

if "role" not in st.session_state:
    st.session_state.role = None


# --- Login ---
if st.session_state.role is None:
    st.title(APP_TITLE)
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username.lower() == "admin" and password == "admin123":
            st.session_state.role = "ADMIN"
            st.rerun()
        elif username.lower() == "employee" and password == "employee123":
            st.session_state.role = "EMPLOYEE"
            st.rerun()
        else:
            st.error("Invalid credentials. Access denied.")
    st.stop()


# --- Main Dashboard ---
st.title(APP_TITLE)
st.sidebar.write(f"Logged in as: **{st.session_state.role}**")

if st.sidebar.button("Logout"):
    st.session_state.role = None
    st.rerun()

menu = ["View Inventory", "Search Food", "Update Quantity", "Expiry Monitor"]
if st.session_state.role == "ADMIN":
    menu = ["Add Food", *menu, "Remove Food", "Summary"]

choice = st.sidebar.selectbox("Navigation", menu)


# --- Helpers ---
def get_inventory_df():
    return st.session_state.inventory


# View Inventory
if choice == "View Inventory":
    st.header("Current Inventory")
    if not st.session_state.inventory:
        st.info("No items in inventory.")
    else:
        st.dataframe(st.session_state.inventory, use_container_width=True)

# Add Food
elif choice == "Add Food":
    st.header("Add New Food Item")
    with st.form("add_food_form"):
        food_id = st.text_input("Food ID (e.g. FD003)", max_chars=20).strip().upper()
        name = st.text_input("Food Name").strip().title()
        category = st.text_input("Category").strip().title()
        quantity = st.number_input("Quantity", min_value=1, step=1)
        unit = st.text_input("Unit (e.g. kg, litres, pcs)").strip()
        purchase_date = st.date_input("Purchase Date")
        expiry_date = st.date_input("Expiry Date")
        submitted = st.form_submit_button("Add Item")

        if submitted:
            if not food_id:
                st.error("Food ID is required.")
            elif any(item["id"].upper() == food_id for item in st.session_state.inventory):
                st.error(f"Food ID '{food_id}' already exists.")
            elif expiry_date < purchase_date:
                st.error("Expiry date cannot be before purchase date.")
            elif not name or not category or not unit:
                st.error("Name, category, and unit are required.")
            else:
                st.session_state.inventory.append(
                    {
                        "id": food_id,
                        "name": name,
                        "category": category,
                        "quantity": int(quantity),
                        "unit": unit,
                        "purchase_date": str(purchase_date),
                        "expiry_date": str(expiry_date),
                    }
                )
                save_inventory(st.session_state.inventory)
                st.success(f"{name} has been added to inventory.")

# Search Food
elif choice == "Search Food":
    st.header("Search Food")
    query = st.text_input("Enter Food Name or Category").strip().lower()
    if query:
        results = [
            item
            for item in st.session_state.inventory
            if query in item["name"].lower() or query in item["category"].lower()
        ]
        if results:
            st.dataframe(results, use_container_width=True)
        else:
            st.warning(f"No items found matching '{query}'.")

# Update Quantity
elif choice == "Update Quantity":
    st.header("Update Quantity")
    if not st.session_state.inventory:
        st.info("Inventory is empty.")
    else:
        item_ids = [item["id"] for item in st.session_state.inventory]
        selected_id = st.selectbox("Select Food ID to Update", item_ids)
        target_item = next(item for item in st.session_state.inventory if item["id"] == selected_id)
        st.write(f"**Current Quantity:** {target_item['quantity']} {target_item['unit']}")
        new_qty = st.number_input("New Quantity", min_value=0, step=1, value=target_item["quantity"])
        if st.button("Update"):
            target_item["quantity"] = int(new_qty)
            save_inventory(st.session_state.inventory)
            st.success(f"Updated quantity for {target_item['name']} to {new_qty} {target_item['unit']}.")

# Remove Food
elif choice == "Remove Food":
    st.header("Remove Food Item")
    if not st.session_state.inventory:
        st.info("Inventory is empty.")
    else:
        item_ids = [item["id"] for item in st.session_state.inventory]
        selected_id = st.selectbox("Select Food ID to Remove", item_ids)
        if st.button("Delete Item"):
            st.session_state.inventory = [
                item for item in st.session_state.inventory if item["id"] != selected_id
            ]
            save_inventory(st.session_state.inventory)
            st.success(f"Item {selected_id} removed successfully.")
            st.rerun()

# Expiry Monitor
elif choice == "Expiry Monitor":
    st.header("Expiry Status Monitor")
    current_date = datetime.now()
    rows = []
    for item in st.session_state.inventory:
        exp_date = datetime.strptime(item["expiry_date"], "%Y-%m-%d")
        delta = (exp_date - current_date).days
        if delta < 0:
            status = "EXPIRED"
        elif 0 <= delta <= 3:
            status = "EXPIRING SOON"
        else:
            status = "AVAILABLE"
        rows.append(
            {
                "ID": item["id"],
                "Name": item["name"],
                "Days to Expiry": delta,
                "Status": status,
            }
        )
    st.table(rows)

# Summary
elif choice == "Summary":
    st.header("Inventory Summary Report")
    total_items = len(st.session_state.inventory)
    total_quantity = sum(item["quantity"] for item in st.session_state.inventory)
    current_date = datetime.now()
    expired = 0
    expiring_soon = 0
    available = 0

    for item in st.session_state.inventory:
        delta = (datetime.strptime(item["expiry_date"], "%Y-%m-%d") - current_date).days
        if delta < 0:
            expired += 1
        elif 0 <= delta <= 3:
            expiring_soon += 1
        else:
            available += 1

    col1, col2 = st.columns(2)
    col1.metric("Total Unique Items", total_items)
    col2.metric("Total Quantity", total_quantity)

    st.write("---")
    st.write(f"- **Expired Items:** {expired}")
    st.write(f"- **Expiring Soon (0–3 days):** {expiring_soon}")
    st.write(f"- **Available Items:** {available}")


# Save inventory on each change if app runs
# ensures file remains in sync.
if st.session_state.get("inventory") is not None:
    save_inventory(st.session_state.inventory)
