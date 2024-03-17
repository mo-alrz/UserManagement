from flask import Flask, render_template, request, session
import pandas as pd
from openpyxl import load_workbook
from datetime import datetime

app = Flask(__name__)

# Read the Excel file and store it in a global variable
df = pd.read_excel('UserData.xlsx', sheet_name='Export')


@app.route('/', methods=['GET', 'POST'])
def index():
    df['Country'] = df['Country'].astype(str)
    unique_countries = sorted(df['Country'].unique())  # Sort the unique countries alphabetically
    selected_country = None

    if request.method == 'POST':
        selected_country = request.form['country']
        filtered_df = df[df['Country'] == selected_country].sort_values(by='Building')
        if filtered_df.empty:
            message = f"No data available for {selected_country}"
            return render_template('index.html', unique_countries=unique_countries, data=message,
                                   selected_country=selected_country)
        else:
            return render_template('index.html', unique_countries=unique_countries,
                                   data=filtered_df.to_html(index=False), selected_country=selected_country)
    else:
        return render_template('index.html', unique_countries=unique_countries, selected_country=selected_country)


@app.route('/add_remove', methods=['POST'])
def add_remove():
    action = request.form['action']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    role = request.form['role']
    selected_country = request.form['selected_country']
    current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if action == 'add':
        worksheet_name = 'Add'
    elif action == 'remove':
        worksheet_name = 'Remove'
    else:
        return "Invalid action"

    # Open the Excel file
    wb = load_workbook('AddRemove.xlsx')

    # Select the worksheet based on action
    ws = wb[worksheet_name]

    # Append the data to the worksheet
    ws.append([first_name, last_name, email, selected_country, role, current_datetime])  # Use selected_country

    # Save the changes to the Excel file
    wb.save('AddRemove.xlsx')

    # Read the updated Excel file
    df_updated = pd.read_excel('AddRemove.xlsx', sheet_name=worksheet_name)

    filtered_df = df_updated[df_updated['Country'] == selected_country]
    # Render a template to display the content of the updated Excel file
    return render_template('AddRemove.html', data=filtered_df.to_html(index=False))


if __name__ == '__main__':
    app.run(debug=True)
