with open("tree1.txt", "r") as f:
    data = f.read()

# Replace NBSP with regular space
data = data.replace("\u00A0", " ")

# Write data back to file
with open("tree1.txt", "w") as f:
    f.write(data)