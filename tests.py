# from subdirectory.filename import function_name
from functions.run_python_file import run_python_file


#print(get_file_content("calculator", "lorem.txt"))
#print(get_file_content("calculator", "main.py"))
#print(get_file_content("calculator", "pkg/calculator.py"))
#print(get_file_content("calculator", "/bin/cat"))

#print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
#print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
#print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

print(run_python_file("calculator", "main.py"))
print(run_python_file("calculator", "tests.py"))
print(run_python_file("calculator", "../main.py")) # (this should return an error)
print(run_python_file("calculator", "nonexistent.py")) # (this should return an error)