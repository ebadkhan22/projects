import streamlit as st
from datetime import datetime
import uuid
import random
import time

st.set_page_config(page_title="Ebad Foods", page_icon="🍔", layout="wide")

# ---- PAGE NAVIGATION ----
pages = ["Home", "Menu", "Cart", "Order History", "Contact Us"]
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", pages)

# ---- MENU DATA ----
menu = {
    "Cheeseburger": {
        "price": 580,
        "img": "https://tse2.mm.bing.net/th?id=OIP.JGigDSijh-lKRw6YaZQGVwHaDs&pid=Api&P=0&h=220",
        "desc": "Juicy grilled beef patty with melted cheese, lettuce, and sauce."
    },
    "Fries": {
        "price": 280,
        "img": "https://tse2.mm.bing.net/th?id=OIP.mL_jcJr_MKr4R3I3IOqpzQHaE8&pid=Api&P=0&h=220",
        "desc": "Crispy golden potato fries served hot."
    },
    "Chicken Nuggets": {
        "price": 350,
        "img": "https://tse3.mm.bing.net/th?id=OIP.54JLdjjsly78jNY_QTrYngHaE7&pid=Api&P=0&h=220",
        "desc": "Bite-sized crispy chicken chunks."
    },
    "Soft Drink": {
        "price": 110,
        "img": "https://tse4.mm.bing.net/th?id=OIP.OouIyZUshFtt5iPdkfoThgHaD8&pid=Api&P=0&h=220",
        "desc": "Chilled refreshing beverage."
    },
    "Ice Cream": {
        "price": 220,
        "img": "https://tse2.mm.bing.net/th?id=OIP.hQhKrL8WKbFWdf5w6tdP6wHaEK&pid=Api&P=0&h=220",
        "desc": "Creamy and cold dessert treat."
    },
    "Biryani": {
        "price": 450,
        "img": "https://th.bing.com/th/id/OIP.gATgZd9KeyhPWJLyorjJcAHaE7?w=263&h=180&c=7&r=0&o=7&cb=iwp2&dpr=1.3&pid=1.7&rm=3",
        "desc": "Spiced rice with tender meat and flavors."
    },
    "Karahi": {
        "price": 800,
        "img": "https://th.bing.com/th/id/OIP.Ey9FOpKM8YsYp839Tu7KKwHaEJ?w=307&h=180&c=7&r=0&o=7&cb=iwp2&dpr=1.3&pid=1.7&rm=3",
        "desc": "Traditional spicy meat curry served hot."
    },
    "Naan": {
        "price": 50,
        "img": "https://th.bing.com/th/id/OIP.mnQWOQBdXbkcMxrsHbTawAHaHa?w=197&h=197&c=7&r=0&o=7&cb=iwp2&dpr=1.3&pid=1.7&rm=3",
        "desc": "Soft, fluffy flatbread."
    }
}

# ---- SESSION STATE ----
if "cart" not in st.session_state:
    st.session_state.cart = {item: 0 for item in menu}
if "order_history" not in st.session_state:
    st.session_state.order_history = []

# ---- STICKY CART IN SIDEBAR ----
with st.sidebar.expander("🛒 Cart Summary"):
    total = sum(q * menu[i]['price'] for i, q in st.session_state.cart.items())
    for item, qty in st.session_state.cart.items():
        if qty > 0:
            st.write(f"{item} x {qty}")
    st.markdown(f"**Total:** Rs.{total}")

# ---- HOME PAGE ----
if page == "Home":
    st.markdown("""
        <style>
            .main-title {
                font-size: 3em;
                font-weight: bold;
                text-align: center;
                color: #FF5733;
            }
            .subtitle {
                text-align: center;
                font-size: 1.2em;
                color: #333333;
            }
            .stButton>button {
                background-color: #FF5733;
                color: white;
                font-weight: bold;
            }
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="main-title">🍔 Ebad Foods</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Delicious Bites Delivered Fast</div>', unsafe_allow_html=True)
    st.image("https://tse3.mm.bing.net/th?id=OIP.LxmmIGwq8dQ8nrCAMfm_hgHaFj&pid=Api&P=0&h=220")

    st.markdown("---")

# ---- MENU PAGE ----
elif page == "Menu":
    st.header("📋 Our Menu")
    search_query = st.text_input("🔍 Search Menu")
    filtered_menu = {k: v for k, v in menu.items() if search_query.lower() in k.lower()}

    items_per_row = 3
    menu_items = list(filtered_menu.items())

    for row_start in range(0, len(menu_items), items_per_row):
        cols = st.columns(items_per_row)
        for i, (item, details) in enumerate(menu_items[row_start:row_start + items_per_row]):
            with cols[i]:
                st.image(details["img"], width=150)
                st.markdown(f"### {item}")
                st.caption(details.get("desc", ""))
                st.markdown(f"<span style='color: green; font-size: 18px;'>Rs.{details['price']}</span>", unsafe_allow_html=True)

                qty = st.number_input(
                    f"Quantity for {item}",
                    min_value=0,
                    max_value=10,
                    value=st.session_state.cart.get(item, 0),
                    key=f"qty_{item}"
                )
                st.session_state.cart[item] = qty

                # Suggestions
                if item == "Biryani":
                    st.info("👀 You might also like: Soft Drink!")
                if item == "Karahi":
                    st.info("👀 You might also like: Naan or Soft Drink!")

# ---- CART PAGE ----
elif page == "Cart":
    st.header("🛒 Your Cart")
    total_price = 0
    has_items = False

    for item, qty in st.session_state.cart.items():
        if qty > 0:
            has_items = True
            price = menu[item]['price']
            st.markdown(f"**{item}** - {qty} x Rs.{price} = Rs.{qty * price}")
            total_price += qty * price

    if not has_items:
        st.info("Your cart is empty. Go to the Menu page to add items.")
    else:
        eta = random.randint(25, 45)
        st.markdown(f"### Total: Rs.{total_price}")
        st.markdown(f"🚚 Estimated delivery: **{eta} minutes**")

        with st.form("checkout_form"):
            st.subheader("Customer Details")
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            address = st.text_area("Delivery Address")
            phone = st.text_input("Phone Number")
            submitted = st.form_submit_button("Place Order")

            if submitted:
                with st.spinner("Placing your order..."):
                    time.sleep(2)
                    order_id = str(uuid.uuid4())[:8].upper()
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    st.session_state.order_history.append({
                        "id": order_id,
                        "name": name,
                        "items": {k: v for k, v in st.session_state.cart.items() if v > 0},
                        "total": total_price,
                        "timestamp": timestamp
                    })

                    st.success(f"✅ Order Placed! Thank you, {name}.")
                    st.markdown(f"**Order ID:** `{order_id}`")
                    st.markdown(f"**Total:** Rs.{total_price:.2f}")
                    st.markdown(f"**Order Time:** {timestamp}")
                    st.balloons()

                    with st.expander("📦 View Order Summary"):
                        for item, qty in st.session_state.cart.items():
                            if qty > 0:
                                st.markdown(f"- {item}: {qty} x Rs.{menu[item]['price']} = Rs.{qty * menu[item]['price']}")

                    st.session_state.cart = {item: 0 for item in menu}

# ---- ORDER HISTORY PAGE ----
elif page == "Order History":
    st.header("📅 Order History")
    if st.session_state.order_history:
        for order in reversed(st.session_state.order_history):
            st.markdown(f"### Order ID: `{order['id']}`")
            st.markdown(f"**Name:** {order['name']}")
            st.markdown(f"**Time:** {order['timestamp']}")
            st.markdown(f"**Total:** Rs.{order['total']}")
            with st.expander("Items"):
                for item, qty in order['items'].items():
                    st.markdown(f"- {item}: {qty} x Rs.{menu[item]['price']} = Rs.{qty * menu[item]['price']}")
            st.markdown("---")
    else:
        st.info("No previous orders yet.")

# ---- CONTACT PAGE ----
elif page == "Contact Us":
    st.header("📞 Contact Us")
    st.markdown("Feel free to reach out to us with any questions, feedback, or issues.")
    st.markdown("**Email:** support@ebadfoods.com")
    st.markdown("**Phone:** +92 3332876078")
    st.markdown("**Address:** Governor House Sindh, Karachi")

    st.markdown("---")
    st.subheader("Send us a message")
    with st.form("contact_form"):
        contact_name = st.text_input("Your Name")
        contact_email = st.text_input("Your Email")
        message = st.text_area("Message")
        sent = st.form_submit_button("Send Message")
        if sent:
            st.success("Thank you for your message! We'll get back to you soon.")
