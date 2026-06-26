# Data Management System with Pandas and JSON

#### Video Demo: <https://youtu.be/_xB7TPexVXw>
#### Description:

This project is a command-line based data management system developed in Python as a final project for CS50P. It allows users to manage and analyze structured data related to clients and products using a combination of JSON storage, object-oriented programming, and Pandas for data manipulation.

The system supports:
- Viewing data
- Inserting new records
- Updating existing records
- Pandas for flexible data manipulation and analysis.

## Project Structure

### `project.py`
This is the main file responsible for:
- Program execution flow
- Handling command-line arguments (`--input`, `--dev`)
- Loading and saving data
- Integrating all system components

### `project_classes.py`
Defines the core data models:
- `Client`
- `Product`

These classes:
- Encapsulate data structure
- Include validation logic using property setters (e.g., email format, category validation)
- Manage instance tracking through class-level lists

### `test_project.py`
Contains automated tests using `pytest` to ensure correctness of:
- Data splitting (`split_data`)
- Duplicate validation (`check_for_duplicates`)
- Instance conversion (`instances_to_dict`)

A setup function clears stored instances before each test to avoid shared state issues.

## Data Handling Design

The system uses a hybrid approach:
- **Pandas DataFrames** for flexible data manipulation and querying
- **Custom classes** for validation and structured data representation

Data is stored in a `data.json` file and loaded into DataFrames at runtime. After execution, all changes are validated and written back to the file.

## Command-Line Interface

The program behavior is controlled through command-line arguments:
- `--input` → Enables interactive user input mode
- `--dev` → Runs developer-only one-time operations

### Input Mode Features
Users can:
- View all records or search by specific fields
- Insert new clients or products
- Update existing records

## Update System Design

When updating records:
- The program creates **temporary objects** using `register=False`
- This allows validation through class setters without storing duplicates
- After validation, changes are applied back to the DataFrame

This design ensures:
- Data integrity
- Reuse of validation logic
- No unintended side effects

## Data Validation

Validation is enforced through:
- Property setters (e.g., email format, category constraints)
- Duplicate checks before saving:
  - No duplicate client emails
  - No duplicate product (name + brand) combinations

## Data Analysis

Since data is stored in Pandas DataFrames, the system supports flexible analysis, such as:
- Sorting clients by country
- Ranking products by sales
- Filtering and grouping data

Additionally, Plotly is used to display tables in a more readable format.

## Saving Data

The function `instances_to_dict()` converts all registered objects into a dictionary format. This data is merged with existing DataFrame data and saved back into `data.json`.

Before saving, the program ensures:
- No duplicate entries exist
- Data structure remains consistent

## Design Decisions

Some key design choices include:
- Using both classes and DataFrames to balance validation and flexibility
- Introducing a `register` parameter to control instance tracking
- Separating developer operations (`--dev`) from user interactions
- Using class-level storage for instance management

## Future Improvements

If expanded further, this project could include:
- Additional data classes
- Change history tracking with timestamps
- AI integration for business insights and querying
- A graphical user interface (GUI)

## Conclusion

This project demonstrates how object-oriented programming, data analysis tools, and file-based persistence can be combined into a cohesive system. It provides both structured validation and flexible data manipulation, making it a solid foundation for more advanced data management applications.
