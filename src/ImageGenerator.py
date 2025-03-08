''' Image generator for the adventure game'''

from openai import OpenAI

class ImageGenerator():
     
    def __init__(self):
          self.image_client = OpenAI()

    def get_image(self, original_prompt: str):
            if len(original_prompt) >= 900:
                # get 4o-mini to summarize prompt
                summarize_prompt = f"Summarize and shorten this description to fewer than 900 characters: {original_prompt}"
                summary_response = self.image_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": summarize_prompt}],
                )
                prompt = summary_response.choices[0].message.content
            else:
                prompt = original_prompt
            image_prompt = f"Create a vivid and interesting image depicting this scene: {prompt[:920]}"
            image_response = self.image_client.images.generate(
                    model="dall-e-2",
                    prompt=image_prompt,
                    size="512x512",
                    quality="standard",
                    n=1,
                )
            return image_response.data[0].url
