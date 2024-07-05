import requests
import streamlit as st
from bs4 import BeautifulSoup
from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch
import re


class SummaryGenerator:
    def __init__(self):
        self.model = T5ForConditionalGeneration.from_pretrained('t5-small')
        self.tokenizer = T5Tokenizer.from_pretrained('t5-small')
        self.device = torch.device('cpu')
        self.MAX_TOKENS = 512  # Maximum number of tokens for the T5 model input

    def is_url(self, input_string):
        url_regex = re.compile(
            r'^(?:http|ftp)s?://'
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'
            r'(?::\d+)?'
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(url_regex, input_string) is not None

    def scrape(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            text_content = ' '.join([p.get_text() for p in soup.find_all('p')])
            return text_content
        except Exception as e:
            st.error(f"Error fetching the URL: {e}")
            return None

    def generate_output(self, input_text):
        preprocess_text = input_text.strip().replace('\n', '')
        t5_input_text = "summarize: " + preprocess_text

        # Tokenize input text
        tokenized_text = self.tokenizer.encode(t5_input_text, return_tensors='pt')

        # Handle inputs longer than MAX_TOKENS by chunking
        if tokenized_text.size(1) > self.MAX_TOKENS:
            token_chunks = torch.split(tokenized_text, self.MAX_TOKENS, dim=1)
        else:
            token_chunks = [tokenized_text]

        summaries = []
        for chunk in token_chunks:
            chunk = chunk.to(self.device)
            summary_ids = self.model.generate(chunk,
                                              min_length=30,
                                              max_length=150,
                                              num_beams=2,
                                              no_repeat_ngram_size=3,
                                              early_stopping=True)
            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            summaries.append(summary)

        return ' '.join(summaries)


# Streamlit UI
st.title("Summary Generation with T5 Model")

input_text = st.text_area("Enter your text here")

if st.button("Generate"):
    if input_text:
        text_generator = SummaryGenerator()
        with st.spinner("Generating output..."):
            if text_generator.is_url(input_text):
                url_text = text_generator.scrape(input_text)
                if url_text:
                    output_text = text_generator.generate_output(url_text)
                else:
                    output_text = "Error processing the URL."
            else:
                output_text = text_generator.generate_output(input_text)
        st.success("Output generated!")
        st.text_area("Generated output", value=output_text, height=200)
    else:
        st.error("Please enter some text to generate output.")
