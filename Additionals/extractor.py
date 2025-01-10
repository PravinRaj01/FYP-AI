import zipfile

zip_file_path = "fine_tuned_bart.zip"
destination = "./fine_tuned_bart"

with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
    zip_ref.extractall(destination)

print("Model files extracted!")

