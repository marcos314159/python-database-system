from project import split_data, check_for_duplicates, instances_to_dict
from project_classes import Client, Product
from contextlib import redirect_stdout
import io
import pandas as pd
import pytest


# ---------- Test Setup ----------

def setup_function():
        """Reset instance storage before each test to avoid side effects."""
            Client.client_instances.clear()
                Product.product_instances.clear()


                # ---------- Test Data ----------

                test_dict = {
                        "Clients": [{"id": 1, "email": "a"}, {"id": 2, "email": "b"}],
                            "Products": [{"id": 1, "name": "a", "brand": "b"}, {"id": 2, "name": "c", "brand": "d"}]
                }

                test_client_df = pd.DataFrame([{"id": 1, "email": "a"}, {"id": 2, "email": "b"}])
                test_client_df.set_index("id", drop=False, inplace=True)

                test_product_df = pd.DataFrame([
                        {"id": 1, "name": "a", "brand": "b"},
                            {"id": 2, "name": "c", "brand": "d"}
                ])
                test_product_df.set_index("id", drop=False, inplace=True)

                duplicates_client_df = pd.DataFrame([
                        {"id": 1, "email": "a"},
                            {"id": 2, "email": "a"}
                ])
                duplicates_client_df.set_index("id", drop=False, inplace=True)

                duplicates_product_df = pd.DataFrame([
                        {"id": 1, "name": "a", "brand": "b"},
                            {"id": 2, "name": "a", "brand": "b"}
                ])
                duplicates_product_df.set_index("id", drop=False, inplace=True)


                # ---------- Tests ----------

                def test_split_data():
                        """Ensure JSON data is correctly converted into DataFrames."""
                            df1, df2 = split_data(test_dict)

                                pd.testing.assert_frame_equal(df1, test_client_df)
                                    pd.testing.assert_frame_equal(df2, test_product_df)


                                    def test_check_for_duplicates():
                                            """Ensure duplicate detection behaves correctly."""

                                                # Duplicate client email
                                                    with pytest.raises(SystemExit, match="Email already registered"):
                                                                check_for_duplicates(duplicates_client_df, test_product_df)

                                                                    # Duplicate product (name + brand)
                                                                        with pytest.raises(SystemExit, match="Item already exists"):
                                                                                    check_for_duplicates(test_client_df, duplicates_product_df)

                                                                                        # Valid case (no duplicates)
                                                                                            f = io.StringIO()
                                                                                                with redirect_stdout(f):
                                                                                                            check_for_duplicates(test_client_df, test_product_df)

                                                                                                                assert f.getvalue() == "Changes saved\n"


                                                                                                                def test_instances_to_dict():
                                                                                                                        """Ensure instance conversion to dictionary format works correctly."""

                                                                                                                            # No instances should return None
                                                                                                                                assert instances_to_dict() is None

                                                                                                                                    # Create test instances
                                                                                                                                        Client(
                                                                                                                                                    email="abc@gmail.com",
                                                                                                                                                            name="b",
                                                                                                                                                                    address="c",
                                                                                                                                                                            city="d",
                                                                                                                                                                                    country="e"
                                                                                                                                        )

                                                                                                                                            Product(
                                                                                                                                                        name="a",
                                                                                                                                                                category="Electronics",
                                                                                                                                                                        price=1,
                                                                                                                                                                                cost_price=2,
                                                                                                                                                                                        weight="3g",
                                                                                                                                                                                                dimensions="b",
                                                                                                                                                                                                        brand="c",
                                                                                                                                                                                                                stock=1
                                                                                                                                            )

                                                                                                                                                result = instances_to_dict()

                                                                                                                                                    # Validate structure
                                                                                                                                                        assert "Clients" in result
                                                                                                                                                            assert "Products" in result

                                                                                                                                                                assert result["Clients"][0]["email"] == "abc@gmail.com"
                                                                                                                                                                    assert result["Products"][0]["name"] == "a"
                                                                                                                        
                                                                                                                                            )
                                                                                                                                        )
                ])
                ])
                ])
                }
