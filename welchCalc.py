from flask import Flask, request, render_template, jsonify
import pandas as pd
from io import StringIO
from scipy import stats

app = Flask(__name__)

# Route for the home page which renders the file upload form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle the file upload and analysis
@app.route('/calculate', methods=['POST'])
def calculate():
    if 'file' not in request.files:
        return "No file uploaded", 400

    file = request.files['file']
    control = request.form.get('control')
    variant = request.form.get('variant')

    if file.filename == '':
        return "No file selected", 400

    if file and file.filename.endswith('.csv'):
        # Read the uploaded CSV file
        file_data = file.read().decode('utf-8')
        csv_data = StringIO(file_data)
        df = pd.read_csv(csv_data)

        # Perform analysis (example: summary statistics)
    
    rps_mapping = {
        'A': 'A_RPS',
        'B': 'B_RPS',
        'C': 'C_RPS'
    }

# Mapping control and variant using the dictionary
    control = rps_mapping.get(control, control)  # Default to control if not in mapping
    variant = rps_mapping.get(variant, variant)

    if control == variant:
        error_message = "Please choose two different groups for control and variant."
        return render_template('index.html', error_message=error_message)
    
    def compare_groups(group1, group2):
    # Sum the RPS for the selected groups
        total_rps_group1 = df[group1].sum(skipna=True)
        total_rps_group2 = df[group2].sum(skipna=True)

        rps_mapping2 = {
            'A_RPS': 'A',
            'B_RPS': 'B',
            'C_RPS': 'C'
        }
        # Compare the total RPS and find the group with the highest RPS
        if total_rps_group1 > total_rps_group2:
            return rps_mapping2.get(group1, group1)
        elif total_rps_group2 > total_rps_group1:
            return rps_mapping2.get(group2, group2)
        else:
            return f"Both groups {group1} and {group2} have the same RPS of {total_rps_group1}."
        
    higherGroup = compare_groups(control, variant)

    group1 = df[control].fillna(0)
    group2 = df[variant].fillna(0)

    t_stat, p_value = stats.ttest_ind(group1, group2, equal_var=False)
    return jsonify({
        'higherGroup': higherGroup,
        'p_value': p_value
        })

if __name__ == '__main__':
    app.run(debug=True)