#!/usr/bin/env python3
# module for gpt generator
# generate different types of content using gpt-3 or gpt-4
import os
import sqlite3
from openai import OpenAI
import settings


class GPTTextGenerator:
    def __init__(self, model_name="gpt-3.5-turbo"):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model_name = model_name

    def generate_text(self, messages, max_tokens=100):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            max_tokens=max_tokens,
        )
        return response.choices[0].message


class ProductDescriptionGenerator(GPTTextGenerator):
    def __init__(
        self,
        product_name,
        product_category,
        product_description,
        product_specifics,
        model="gpt-4-0125-preview",
    ):
        super().__init__(model)
        self.product_name = product_name
        self.product_category = product_category
        self.product_description = product_description
        self.product_specifics = product_specifics

    def create_product_details_message(self):
        return (
            f"VidaProduct: {self.product_name}\n"
            f"Category: {self.product_category}\n"
            f"Description: {self.product_description}\n"
            f"Specifics: {self.product_specifics}\n"
        )

    def tun_description(self):
        prompt_messages = [
            {
                "role": "user",
                "content": "You are selling products in online store. Your role is to create a "
                "description for the product and give in the provided format. "
                "The details of the product are given after the instructions.",
            },
            {"role": "user", "content": "Instruction: "},
            {
                "role": "user",
                "content": "Please craft an informative and engaging product description that adopts "
                "a professional tone. It should not only persuade the customer to "
                "purchase the product but also convey the product's potential to enhance "
                "the customer's life. Avoid a personal or casual style, repetitive "
                "information, and focus on selling both the product and its value "
                "proposition. Keep max of 10000 characters. Write it in Dutch. Use the html tags like <p>, <li>, <ul> "
                "for the formatting. Don't use tags like <h1>, <h2>, <h3>, <h4>, <h5>, <h6> as well as don't make whole"
                "html page. Don't use the VidaXL brand name in the description."
                "Use the following details to create the description:",
            },
            {"role": "user", "content": "VidaProduct details: "},
            {
                "role": "user",
                "content": self.create_product_details_message(),
            },
        ]

        return self.generate_text(prompt_messages, max_tokens=4000).content

    def generate_bol_name(self):
        prompt_msg = [
            {"role": "user", "content": "Instruction:"},
            {
                "role": "user",
                "content": "You are a seller on an online marketplace. Your task is to generate a name for "
                "a new product. The product details are given after this instructions."
                "Do not use the VidaXL brand name in the product name."
                "Return the name in the dutch language and max of 250 characters. Use the following format: /n"
                "[Name] - [Serie] - [Productgroep] - [Kenmerk 1] - [Kenmerk 2] - [Kenmerk 3] - [Kenmerk 4] - "
                "[Kenmerk 5] - [Kenmerk 6] ... - [Kenmerk N]",
            },
            {"role": "user", "content": "VidaProduct details:"},
            {
                "role": "user",
                "content": self.create_product_details_message(),
            },
        ]
        return self.generate_text(prompt_msg, max_tokens=250).content


class OftionnSocialMediaGenerator(GPTTextGenerator):
    def __init__(self):
        super().__init__()

    def generate_post(self, instruction):
        instr_beginning = """
        You are a social media manager of a company oftionn.
        Company is doing a automation of office work, but is also helping 
        people work with office tools more efficiently.
        Company is also selling the electronic products which are improve people's life.
        Your role is to create a content for the company's LinkedIn page.
        Content should be informative and engaging. It should have professional tone.
        Should not be personal or casual. Should not be too long or too short - max 600 characters.
        """
        return self.generate_text(
            [{"role": "user", "content": instr_beginning + "\n" + instruction}],
            max_tokens=600,
        )


first_post = """It has been 2 days since you posted about the launch of the website.
        You promised there will be more features released every week. We as oftionn, just
        added a blog page to our website. Blog can be reached at https://oftionn.com/blog.
        For now we are just moving the posts from an old oftionn website, but except that we
        launched the audio transcription of the posts in the spotify. You can find the link to the
        spotify in the blog page. Please create a informative, elegant and engaging post for the LinkedIn page.
        Please inform in the post about the above mentioned changes.
        """


class GPT_ImageGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    def generate_img_prompt(self, text):
        instruction = f"""
        You are a image prompt engineer. Your tasks is to generate the image,
        which will be represented given text. Generate ideal prompt with length of 100 characters. Given text: {text}"""
        response = self.client.completions.create(
            model="gpt-3.5-turbo-instruct", prompt=instruction, max_tokens=100
        )
        return response.choices[0].text.strip()

    def generate_img_for_(self, text):
        prompt = self.generate_img_prompt(text)
        response = self.client.images.generate(model="dall-e-3", prompt=prompt)
        return response.data[0].url


def generate_post():
    linkedin_generator = OftionnSocialMediaGenerator()
    linkedin_post = linkedin_generator.generate_post(first_post)
    print(linkedin_post)
    post_img_generator = GPT_ImageGenerator()
    img_url = post_img_generator.generate_img_for_(linkedin_post)
    print(img_url)


class DB_Updator:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def insert_post(self, post):
        self.cursor.execute("INSERT INTO posts (content) VALUES (?)", (post,))
        self.conn.commit()

    def close(self):
        self.conn.close()
