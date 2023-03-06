import json

# Open the input and output files
with open("input.txt", "r") as input_file, open("output.json", "w") as output_file:
    # Iterate over each line in the input file
    for line in input_file:
        # Split the line by the timestamp, author, and content
        parts = line.strip().split("] ")
        timestamp = parts[0][1:]
        author, content = parts[1].split(": ", 1)
        # Create a dictionary with the message information
        message = {"timestamp": timestamp, "author": author, "content": content}
        # Write the message as a JSON object on a new line in the output file
        output_file.write(json.dumps(message) + "\n")
