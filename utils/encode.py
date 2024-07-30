from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def encode_string(string):
    string = clean_string(string)
    return model.encode(string).tolist()


def clean_string(string):
    string = string.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    valid_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+# "
    string = ''.join(char for char in string if char in valid_chars)
    string = ' '.join(string.split())
    return string
