import sys
import json

# Read input from AJAX request
data = json.loads(sys.stdin.read())
user_input = data['input']

# Process input and generate output
output = f"You entered: {user_input}"

# Send output back to JavaScript
print(json.dumps({'output': output}))
