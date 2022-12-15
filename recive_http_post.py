import requests

def append_to_file(file_name, input_data):
  # Open the file in append mode
  with open(file_name, "a") as f:
    # Write the input data to the file
    f.write(input_data)

# Receive the input data from the POST request
input_data = request.form['input_data']

# Call the append_to_file function to write the data to the file
append_to_file("my_file.txt", input_data)
