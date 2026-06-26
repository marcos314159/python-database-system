from project_classes import Client, Product
import pandas as pd
import plotly.graph_objects as go
import json
import sys


def main():
    # Load data into DataFrames
    client_df, product_df = load_data()

    # Run developer-only operations (manual data manipulation)
    if "--dev" in sys.argv:
        run_one_time_operations(client_df, product_df)

    # Run user input interface
    if "--input" in sys.argv:
        input_handling(client_df, product_df)

    # Save any changes made during execution
    save_changes(client_df, product_df)


def load_data():
    """Load and validate JSON data from file."""
    try:
        with open("data.json", "r") as file:
            try:
                data = json.load(file)
                return split_data(data)

            except json.decoder.JSONDecodeError:
                sys.exit("No data to work with")

    except FileNotFoundError:
        sys.exit("File not found")


# Developer-only function for running one-time data operations.
# Intended for temporary use (e.g., analyzing, viewing, inserting, updating, or deleting data).
def run_one_time_operations(client_df, product_df):
    """
    Example usage:

    c1 = Client(...)
    p1 = Product(...)

    These operations will execute once when the program runs with --dev.
    """
    pass

def split_data(data):
    # Convert JSON data into Pandas DataFrames
    client_df = pd.DataFrame(data["Clients"])
    client_df.set_index("id", drop=False, inplace=True)

    product_df = pd.DataFrame(data["Products"])
    product_df.set_index("id", drop=False, inplace=True)

    return client_df, product_df


def check_for_duplicates(client_df, product_df):
    # Ensure no duplicate client emails exist
    c_duplicates = client_df.duplicated(subset="email")
    if c_duplicates.any():
        sys.exit("Email already registered")

    # Ensure no duplicate product (name + brand) combinations exist
    p_duplicates = product_df.duplicated(subset=["name", "brand"])
    if p_duplicates.any():
        sys.exit("Item already exists")

    print("Changes saved")


def instances_to_dict():
    # Convert all Client and Product instances into dictionary format
    data_dict = {}

    for cl in Client, Product:
        cl_list = []

        for o in cl.get_all_instances():
            # Remove leading underscore from attribute names
            d = {k.lstrip("_"): v for k, v in vars(o).items()}
            cl_list.append(d)

        if cl_list:
            data_dict.update({f"{cl.__name__}s": cl_list})

    return data_dict if data_dict else None


def display_table(df):
    """Display a DataFrame using a Plotly table."""
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns), align='left'),
        cells=dict(values=df.transpose().values.tolist(), align='left'))
    ])
    fig.show()


def search_and_display(df, column, value, not_found_msg):
    """Search a DataFrame by column and display results."""
    match = df[df[column] == value]

    if not match.empty:
        display_table(match)
        return True

    print(not_found_msg)
    return False


def input_handling(client_df, product_df):
    """
    Handles all user-driven operations via terminal input.
    Supports viewing, inserting, and updating data.
    """

    def input_view():
        """Handles viewing data."""
        while True:
            print("[clients] [products] [exit]")
            choice = input().lower()

            if choice == "exit":
                return

            if choice == "clients":
                df = client_df
                # a list with existing options
                options_list = ["email", "name", "all entries", "exit"]
                # actual options string to be printed
                options = "[email] [name] [all entries] [exit]"

            elif choice == "products":
                df = product_df
                # a list with existing options
                options_list = ["name", "brand", "all entries", "exit"]
                # actual options string to be printed
                options = "[name] [brand] [all entries] [exit]"

            else:
                print("Invalid input")
                continue

            while True:
                print(f"{options}")
                sub_choice = input().lower()

                if sub_choice == "exit":
                    return

                if sub_choice == "all entries":
                    display_table(df)
                    return

                if sub_choice not in options_list:
                    print("Invalid input")
                    continue

                while True:
                    value = input(f"{sub_choice.capitalize()}: ")

                    if value == "exit":
                        return

                    found = search_and_display(df, sub_choice, value,
                                               f"{sub_choice.capitalize()} not found")

                    if found:
                        return

    def input_insert():
        """Handles inserting new data."""
        while True:
            print("[clients] [products] [exit]")
            choice = input().lower()

            if choice == "exit":
                return

            if choice == "clients":
                # Create new Client instance
                Client(
                    email=input("Email: "),
                    name=input("Name: "),
                    address=input("Address: "),
                    city=input("City: "),
                    country=input("Country: ")
                )
                return

            elif choice == "products":
                # Create new Product instance
                Product(
                    name=input("Name: "),
                    category=input("Category: "),
                    price=float(input("Price: ")),
                    cost_price=float(input("Cost price: ")),
                    weight=input("Weight: "),
                    dimensions=input("Dimensions: "),
                    brand=input("Brand: "),
                    color=input("Color: ")
                )
                return

            else:
                print("Invalid input")

    def input_update():
        """Handles updating existing data."""
        while True:
            print("[clients] [products] [exit]")
            choice = input().lower()

            if choice == "exit":
                return

            if choice == "clients":
                # Update client data (search by email)
                while True:
                    client_email = input("Email: ")

                    if client_email == "exit":
                        return

                    match = client_df[client_df["email"] == client_email]

                    if match.empty:
                        print("User not found")
                        continue

                    break

                # Temporary instance, won't be added to instances dictionary later on
                row_data = match.to_dict("records")[0]
                c = Client(**row_data, register=False)
                print(c)

                field_map = {
                    "email": "email",
                    "e-mail": "email",
                    "name": "name",
                    "address": "address",
                    "city": "city",
                    "country": "country"
                }

                while True:
                    print("[email / e-mail] [name] [address] [city] [country] [exit]")
                    field = input("What would you wish to alter? ").lower()

                    if field == "exit":
                        return

                    if field not in field_map:
                        print("Invalid input")
                        continue

                    break

                # Apply validated update through setter
                new_value = input(f"New {field_map[field]}: ")
                setattr(c, field_map[field], new_value)

                # Save validated value back to DataFrame
                client_df.at[c.id, field_map[field]] = getattr(c, field_map[field])
                return

            elif choice == "products":
                # Update product data (search by name + brand)
                while True:
                    try:
                        product_name, product_brand = input(
                            "Product name/brand: ").split("/")
                        product_name = product_name.strip()
                        product_brand = product_brand.strip()

                    except ValueError:
                        print("Invalid format (use name/brand)")
                        continue

                    match = product_df[
                        (product_df["name"] == product_name) &
                        (product_df["brand"] == product_brand)
                    ]

                    if match.empty:
                        print("Product not found")
                        continue

                    break

                # Temporary instance, won't be added to instances dictionary later on
                row_data = match.to_dict("records")[0]
                p = Product(**row_data, register=False)
                print(p)

                while True:
                    field_list = ["price", "cost price", "stock", "sales", "exit"]
                    print("[price] [cost price] [stock] [sales] [exit]")
                    field = input("What would you like to update? ").lower()

                    if field == "exit":
                        return

                    if field not in field_list:
                        print("Invalid input")
                        continue

                    break

                while True:
                    try:
                        value = float(input("[+/-]value: "))

                        # Apply updates through class methods
                        if field == "price":
                            p.update_price(value)
                            product_df.at[p.id, "price"] = p.price

                        elif field == "cost price":
                            p.update_cost_price(value)
                            product_df.at[p.id, "cost_price"] = p.cost_price

                        elif field == "stock":
                            p.update_stock(int(value))
                            product_df.at[p.id, "stock"] = p.stock

                        elif field == "sales":
                            p.update_sales(int(value))
                            product_df.at[p.id, "sales"] = p.sales

                        return

                    except ValueError:
                        print("Invalid input, use [+ or -] followed by a number")

            else:
                print("Invalid input")

    # Main input loop
    while True:
        print("[view] [insert] [update] [exit]")
        choice = input().lower()

        if choice == "view":
            input_view()
            return

        elif choice == "insert":
            input_insert()
            return

        elif choice == "update":
            input_update()
            return

        elif choice == "exit":
            return

        else:
            print("Invalid input")


def save_changes(client_df, product_df):
    # Convert instance-based data into dictionary format
    instances_dict = instances_to_dict()

    # Merge DataFrame data with instance data (if any)
    if instances_dict:
        clients_list = (
            client_df.to_dict("records") + instances_dict["Clients"]
            if "Clients" in instances_dict else client_df.to_dict("records")
        )

        products_list = (
            product_df.to_dict("records") + instances_dict["Products"]
            if "Products" in instances_dict else product_df.to_dict("records")
        )
    else:
        clients_list = client_df.to_dict("records")
        products_list = product_df.to_dict("records")

    # Validate no duplicates before saving
    check_for_duplicates(pd.DataFrame(clients_list), pd.DataFrame(products_list))

    # Write updated data back to JSON file
    with open("data.json", "w") as file:
        json.dump({"Clients": clients_list, "Products": products_list}, file, indent=2)


if __name__ == "__main__":
    main()
