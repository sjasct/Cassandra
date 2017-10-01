import async2rewrite

file = input("> ")
file_result = async2rewrite.from_file(file)
print(file_result)