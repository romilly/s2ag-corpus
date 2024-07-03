import re

with open("tree3.txt", "r") as f:
    lines = f.readlines()

# Remove "|" at the start of each line
lines = [re.sub(r'^│', '', line) for line in lines]

# Write data back to file
with open("tree3.txt", "w") as f:
    f.writelines(lines)