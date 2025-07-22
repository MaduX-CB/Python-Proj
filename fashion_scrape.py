import tkinter as tk
from tkinter import ttk, messagebox
from bs4 import BeautifulSoup
from PIL import Image, ImageTk
from io import BytesIO
from requests import get
from datetime import datetime, timedelta

# Web scraping
url = "https://www.sojoee.com/"
sojoee = get(url)
sojoee_parsed = BeautifulSoup(sojoee.text, "html.parser")
product_img = sojoee_parsed.find_all("div", attrs={"class": "product-img-wrap"})
product_info = sojoee_parsed.find_all("div", attrs={"class": "product-info-wrap info"})
data = []
for img, info in zip(product_img, product_info):
    name = info.find("a", attrs={"class": "name nasa-bold woocommerce-loop-product__title nasa-show-one-line"}).text
    price = info.find("span", attrs={"class": "woocommerce-Price-amount amount"}).text
    pics = img.find("img", attrs={"class": "attachment-woocommerce_thumbnail"})
    product = (name.strip(), price, pics["data-src"])
    data.append(product)

# GUI setup
root = tk.Tk()
root.title("Sojoee Clothing Store")
cart = []  # Cart to hold selected products

# Functionality
def clean_price(price):
    try:
        return float(price.replace("₦", "").replace(",", "").strip())
    except ValueError:
        return 0.0

def add_to_cart(item, price):
    cart.append((item, clean_price(price)))
    update_cart()

def remove_item_from_cart(item_name):
    for idx, (name, price) in enumerate(cart):
        if name == item_name:
            del cart[idx]
            break
    update_cart()

def update_cart():
    for widget in cart_list_frame.winfo_children():
        widget.destroy()

    total = 0
    for item, price in cart:
        item_frame = tk.Frame(cart_list_frame)
        item_frame.pack(fill="x", pady=5)

        description_text = tk.Text(item_frame, wrap="word", height=3, font=("Arial", 12), width=25)
        description_text.insert("1.0", f"{item}\nPrice: ₦{price:,.2f}")
        description_text.config(state="disabled")
        description_text.pack(side="left", fill="x", expand=True)

        scroll = ttk.Scrollbar(item_frame, orient="vertical", command=description_text.yview)
        description_text.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")

        # Remove Button
        remove_button = tk.Button(
            item_frame,
            text="Remove",
            command=lambda n=item: remove_item_from_cart(n),
            bg="#dc3545", fg="white", font=("Arial", 10, "bold")
        )
        remove_button.pack(side="right", padx=5)

        total += price

    total_label.config(text=f"Total: ₦{total:,.2f}")

def load_image(image_url):
    try:
        response = get(image_url)
        img = Image.open(BytesIO(response.content))
        img.thumbnail((150, 150))
        return ImageTk.PhotoImage(img)
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

def checkout():
    if not cart:
        messagebox.showerror("Error","No item was chosen.")
        return

    checkout_window = tk.Toplevel(root)
    checkout_window.title("Checkout")

    tk.Label(checkout_window, text="Checkout", font=("Arial", 18, "bold")).pack(pady=10)

    tk.Label(checkout_window, text="Name:").pack(anchor="w", padx=10)
    name_entry = tk.Entry(checkout_window, width=40)
    name_entry.pack(padx=10, pady=5)

    tk.Label(checkout_window, text="Address:").pack(anchor="w", padx=10)
    address_entry = tk.Text(checkout_window, width=40, height=4)
    address_entry.pack(padx=10, pady=5)

    tk.Label(checkout_window, text="Phone Number:").pack(anchor="w", padx=10)
    phone_entry = tk.Entry(checkout_window, width=40)
    phone_entry.pack(padx=10, pady=5)

    tk.Label(checkout_window, text="Payment Method:").pack(anchor="w", padx=10)
    payment_method = ttk.Combobox(checkout_window, values=["Credit Card", "PayPal", "Cash on Delivery"], state="readonly")
    payment_method.pack(padx=10, pady=5)
    payment_method.set("Select Payment Method")

    # Shipping Options
    tk.Label(checkout_window, text="Shipping Method:").pack(anchor="w", padx=10)
    shipping_options = ttk.Combobox(
        checkout_window, values=["Standard Shipping (3-5 days)", "Express Shipping (1-2 days)"], state="readonly"
    )
    shipping_options.pack(padx=10, pady=5)
    shipping_options.set("Standard Shipping (3-5 days)")

    # Gift Wrap Option
    gift_var = tk.BooleanVar()
    gift_wrap_check = tk.Checkbutton(checkout_window, text="Add Gift Wrap", variable=gift_var)
    gift_wrap_check.pack(anchor="w", padx=10, pady=5)

    def place_order():
        name = name_entry.get().strip()
        address = address_entry.get("1.0", "end-1c").strip()
        phone = phone_entry.get().strip()
        payment = payment_method.get()
        shipping = shipping_options.get()
        gift_wrap = "Yes" if gift_var.get() else "No"

        if not name or not address or not phone or payment == "Select Payment Method":
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            int(phone)
        except:
            messagebox.showerror("Error","Phone Number is invalid")
            return

        if shipping=="Standard Shipping (3-5 days)":
            no_days = 4
        elif shipping == "Express Shipping (1-2 days)":
            no_days = 2

        delivery_date = datetime.now() + timedelta(days=no_days)
        delivery_date_str = delivery_date.strftime("%A, %d %B %Y")

        order_summary = f"Order placed successfully!\n\nName: {name}\nAddress: {address}\nPhone: {phone}\nPayment: {payment}\nShipping: {shipping}\nGift Wrap: {gift_wrap}\nDelivery Date: {delivery_date_str}\n\nItems Ordered:\n"
        total = 0
        for item, price in cart:
            order_summary += f"- {item} (₦{price:,.2f})\n"
            total += price

        order_summary += f"\nTotal: ₦{total:,.2f}"
        messagebox.showinfo("Order Summary", order_summary)
        checkout_window.destroy()
        cart.clear()
        update_cart()

    tk.Button(
        checkout_window,
        text="Place Order",
        command=place_order,
        bg="#28a745", fg="white", font=("Arial", 12, "bold")
    ).pack(pady=10, side="bottom")

# Product and cart layout
header_frame = tk.Frame(root, pady=10)
header_frame.pack(fill="x")
title_label = tk.Label(header_frame, text="Sojoee Clothing Store", font=("Arial", 24, "bold"), fg="#2E86C1")
title_label.pack()

main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

product_frame = tk.Frame(main_frame)
product_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

cart_frame = tk.Frame(main_frame, width=200, padx=10, pady=10)
cart_frame.pack(side="right", fill="y")

canvas = tk.Canvas(product_frame)
scrollbar = ttk.Scrollbar(product_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

def display_products():
    for item_name, price, image_url in data:
        item_frame = tk.Frame(scrollable_frame, pady=5)
        item_frame.pack(fill="x", padx=5, pady=5)

        img = load_image(image_url)
        image_label = tk.Label(item_frame, image=img)
        image_label.image = img
        image_label.pack(side="left", padx=10)

        text_frame = tk.Frame(item_frame)
        text_frame.pack(side="left", fill="both", expand=True)

        item_label = tk.Label(text_frame, text=item_name, font=("Arial", 12), justify="left", anchor="w", wraplength=200)
        item_label.pack(fill="x")

        price_label = tk.Label(text_frame, text=f"Price: {price}", font=("Arial", 12, "bold"), anchor="w")
        price_label.pack(fill="x")

        add_button = tk.Button(
            text_frame, text="Add to Cart",
            command=lambda n=item_name, p=price: add_to_cart(n, p),
            bg="#28a745", fg="white", font=("Arial", 10, "bold")
        )
        add_button.pack(pady=2)

display_products()

cart_label = tk.Label(cart_frame, text="Shopping Cart", font=("Arial", 18, "bold"))
cart_label.pack(anchor="w")

cart_canvas = tk.Canvas(cart_frame)
cart_scrollbar = ttk.Scrollbar(cart_frame, orient="vertical", command=cart_canvas.yview)
cart_list_frame = tk.Frame(cart_canvas)

cart_list_frame.bind("<Configure>", lambda e: cart_canvas.configure(scrollregion=cart_canvas.bbox("all")))
cart_canvas.create_window((0, 0), window=cart_list_frame, anchor="nw")
cart_canvas.configure(yscrollcommand=cart_scrollbar.set)

cart_canvas.pack(side="left", fill="both", expand=True)
cart_scrollbar.pack(side="right", fill="y")

total_label = tk.Label(cart_frame, text="Total: ₦0.00", font=("Arial", 14, "bold"))
total_label.pack(anchor="w", pady=10)

checkout_button = tk.Button(cart_frame, text="Checkout", command=checkout, bg="#17a2b8", fg="white", font=("Arial", 12, "bold"))
checkout_button.pack(fill="x")

root.mainloop()