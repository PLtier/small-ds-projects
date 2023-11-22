import nltk;
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
import re

from nltk.corpus import stopwords;

stop_words = set(stopwords.words('english'))

def lemmatize(sentence):
    def get_wordnet_pos(tag):
        """Map NLTK's POS tags to the format used by WordNetLemmatizer"""
        first_letter = tag[0]
        tag_dict = {"J": wordnet.ADJ,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}

        return tag_dict.get(first_letter, wordnet.NOUN)

    lemmatizer = WordNetLemmatizer()

    # sentence = "I  i.e.       _was_        drinking    soda."
    tokens = nltk.pos_tag(word_tokenize(sentence))
    # print(tokens)
    return ' '.join([lemmatizer.lemmatize(token, get_wordnet_pos(tag)) for token, tag in tokens])


def remove_stop_words(text):
    return ' '.join(word for word in text.split() if word not in stop_words)


ipv6_pattern = r'(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}:((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))'
ipv4_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}(?:/\d{1,2})?\b'
mac_address_pattern = r'\b(?:[0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}\b'
path_pattern = r'(?:^|\s)\.\/[a-zA-Z][^ ]*\/[^ ]+|\/[a-zA-Z][^ ]*\/[^ ]+'
command_pattern = r'(?:^|\s)\/[a-zA-Z]\S*'
bandwidth_pattern = r'\b(?:\d+\s?|)(?:[Mm][Bb]|[Gg][Bb])\/(?:s|sec)\b'
size_pattern = r'\b(?:\d+\s?|)(?:[Mm][Bb]|[Gg][Bb])\b'
floating_point_pattern = r'\b\d+\.\d+\b'
file_pattern = r'\b\w+\.\w+\b'
mac_pattern = r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})'

def replace_common_tech_words(text):
    text = text.lower()  # Lowercase text Actually it influences meaning slightly, but for simplicity I do it here
    text = re.sub(mac_pattern, ' _BIA_ ', text) # Replace BIA addresses
    text = re.sub(ipv4_pattern, ' _IPV4_ADDRESS_ ', text) # Replace IPv4 addresses
    text = re.sub(ipv6_pattern, ' _IPV6_ADDRESS_ ', text)  # Replace IPv6 addresses
    text = re.sub(mac_address_pattern, ' _MAC_ADDRESS_ ', text)  # Replace MAC addresses
    text = re.sub(path_pattern, ' _FILE_PATH_ ', text)  # Replace file paths
    text = re.sub(command_pattern, ' _COMMAND_ ', text)  # Replace commands
    text = re.sub(bandwidth_pattern, ' _BANDWIDTH_ ', text)  # Replace bandwidth
    text = re.sub(size_pattern, ' _SIZE_ ', text)  # Replace sizes
    text = re.sub(floating_point_pattern, ' _NUM_ ', text)  # Replace floating point numbers
    text = re.sub(r'-?\b\d+\b', ' _NUM_ ', text)  # Replace other numbers
    text = re.sub(file_pattern, ' _FILENAME_ ', text) # match files like text.txt
    return text

def remove_unnecessary_signs(text):
    text = text.replace(',', " ")
    text = text.replace("i.e.", " ").replace("i.e", " ")
    text = re.sub(r'[.;\/\\()\-\+=?:{}%÷]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()  # Remove and trim whitespaces
    return text