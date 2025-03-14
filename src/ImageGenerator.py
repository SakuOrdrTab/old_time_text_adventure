''' Image generator for the adventure game. Currently uses openAI Dall-E 2, which is EXPENSIVE!'''

from openai import OpenAI

class ImageGenerator():
     
    def __init__(self):
          '''Needs open ai API key currently'''
          self.image_client = OpenAI()
          self.style = ""

    def set_style(self, style : str) -> None:
        '''Imports style from adventure py file'''
        self.style = style

    def get_image(self, original_prompt: str):
        '''Creates an Dall-E image from scene. Image prompt has a hard limit of 1000 tokens.'''
        try:
            if len(original_prompt) >= 900:
                summarize_prompt = f"Create a DALL-E prompt describing this scene: {original_prompt}.\nThe prompt must be less than 900 characters long!"
                summary_response = self.image_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": summarize_prompt}],
                )
                prompt = summary_response.choices[0].message.content
            else:
                prompt = original_prompt

            image_prompt = f"Create a vivid and interesting image depicting this scene in the style of {self.style}: {prompt[:900]}"
            print(f"image prompt: {image_prompt}")
            image_response = self.image_client.images.generate(
                model="dall-e-2",
                prompt=image_prompt,
                size="512x512",
                quality="standard",
                n=1,
            )
            # Check if image data is available
            if image_response.data and len(image_response.data) > 0:
                return image_response.data[0].url
            else:
                # Fallback image if no data returned
                return "/static/images/placeholder.png"
        except Exception as e:
            print("Image generation error:", e)
            # Return a fallback image if an exception occurs
            return "/static/error.png"
