''' Image generator for the adventure game'''

from openai import OpenAI

class ImageGenerator():
     
    def __init__(self):
          self.image_client = OpenAI()

    def get_image(self, original_prompt: str):
        try:
            if len(original_prompt) >= 900:
                summarize_prompt = f"Summarize and shorten this description to fewer than 900 characters: {original_prompt}"
                summary_response = self.image_client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": summarize_prompt}],
                )
                prompt = summary_response.choices[0].message.content
            else:
                prompt = original_prompt

            image_prompt = f"Create a vivid and interesting image depicting this scene: {prompt[:920]}"
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
