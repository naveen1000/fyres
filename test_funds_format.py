
from Fyres_Funds import format_funds

def test_format_funds():
    # Test Case 1: Mixed values
    data_mixed = {
        "fund_limit": [
            {
                "title": "Total Balance",
                "equityAmount": 685001.44,
                "commodityAmount": 0.0
            },
            {
                "title": "Utilized Amount",
                "equityAmount": 0.0,
                "commodityAmount": 0.0
            },
            {
                "title": "Collaterals",
                "equityAmount": 0.0,
                "commodityAmount": 100.0
            }
        ]
    }
    print("--- Test Case 1: Mixed Values ---")
    print(format_funds(data_mixed))
    print("\n")

    # Test Case 2: Top level fallback
    data_fallback = {
        "Total Balance": 5000.0,
        "Utilized": 0.0,
        "Zero Value": 0,
        "Some Text": "Hello"
    }
    print("--- Test Case 2: Top Level Fallback ---")
    print(format_funds(data_fallback))
    print("\n")
    
    # Test Case 3: Nested items fallback
    data_nested = {
        "fund_limit": [
            {
                "title": "Misc",
                "val1": 100,
                "val2": 0
            }
        ]
    }
    print("--- Test Case 3: Nested Items Fallback ---")
    print(format_funds(data_nested))
    print("\n")

if __name__ == "__main__":
    test_format_funds()
