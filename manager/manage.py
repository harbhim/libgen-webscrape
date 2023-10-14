import toml

try:
    with open("./settings.toml", "r") as toml_file:
        settings = toml.load(toml_file)

except FileNotFoundError:
    raise Exception("File settings.toml is not present")
