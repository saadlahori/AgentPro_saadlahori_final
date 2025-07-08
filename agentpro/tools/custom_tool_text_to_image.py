# TextToImage_FluxPro_Tool_HuggingFace_Gradio_Space.py

import os
import time
from gradio_client import Client
from pydantic import Field
from agentpro.tools import Tool
import re 

class TextToImage_FluxProTool(Tool):
    name: str = Field(default="Text-to-Image (FLUX-Pro)")
    description: str = Field(
        default="Generate an image from a text prompt using FLUX-Pro. "
                "Input format: 'A cat | width=512 | height=512'"
    )
    action_type: str = Field(default="flux_image_gen")
    input_format: str = Field(default="Prompt | width=512 | height=512")

    def generate(self, input_text: str) -> str:
        # Defaults
        prompt = ""
        width, height = 768, 768

        # Parse input
        parts = [p.strip() for p in input_text.split("|")]
        if parts:
            prompt = parts[0]

        for part in parts[1:]:
            if "=" in part:
                key, val = part.split("=")
                if key.strip() == "width":
                    width = int(val.strip())
                elif key.strip() == "height":
                    height = int(val.strip())

        if not prompt:
            return "❌ Prompt is empty."

        try:
            client = Client("NihalGazi/FLUX-Pro-Unlimited")
            result = client.predict(
                prompt=prompt,
                width=width,
                height=height,
                seed=0,
                randomize=True,
                server_choice="Google US Server",
                api_name="/generate_image"
            )

            temp_path = result[0]
            if not os.path.exists(temp_path):
                return "❌ Image file not found after generation."

            # Save locally to ./generated/
            #filename = f"flux_image_{int(time.time())}.webp"
            safe_prompt = re.sub(r'[^\w\s-]', '', prompt).strip().replace(' ', '_')
            filename = f"flux_image_{safe_prompt}_{int(time.time())}.webp"
            local_dir = os.path.join(os.getcwd(), "Media/Generated_Images")
            os.makedirs(local_dir, exist_ok=True)
            final_path = os.path.join(local_dir, filename)

            with open(temp_path, "rb") as src, open(final_path, "wb") as dst:
                dst.write(src.read())

            return final_path  # return local path

        except Exception as e:
            return f"❌ Error during image generation: {e}"

    def run(self, input_data: str) -> str:
        return self.generate(input_data)



# # WORKING CODE agentpro/tools/custom_tool_text_to_image.py

# import os
# import time
# from gradio_client import Client
# from pydantic import Field
# from agentpro.tools import Tool

# class TextToImage_FluxProTool(Tool):
#     name: str = Field(default="Text-to-Image (FLUX-Pro)")
#     description: str = Field(
#         default="Generate an image from a text prompt using FLUX-Pro. "
#                 "Input format: 'A cat | width=512 | height=512'"
#     )
#     action_type: str = Field(default="flux_image_gen")
#     input_format: str = Field(default="Prompt | width=512 | height=512")

#     def generate(self, input_text: str) -> str:
#         # Defaults
#         prompt = ""
#         width, height = 768, 768

#         # Parse input
#         parts = [p.strip() for p in input_text.split("|")]
#         if parts:
#             prompt = parts[0]

#         for part in parts[1:]:
#             if "=" in part:
#                 key, val = part.split("=")
#                 if key.strip() == "width":
#                     width = int(val.strip())
#                 elif key.strip() == "height":
#                     height = int(val.strip())

#         if not prompt:
#             return "❌ Prompt is empty."

#         try:
#             client = Client("NihalGazi/FLUX-Pro-Unlimited")
#             result = client.predict(
#                 prompt=prompt,
#                 width=width,
#                 height=height,
#                 seed=0,
#                 randomize=True,
#                 server_choice="Google US Server",
#                 api_name="/generate_image"
#             )

#             local_path = result[0]
#             if not os.path.exists(local_path):
#                 return "❌ Image file not found after generation."

#             # Copy to known location
#             filename = f"flux_image_{int(time.time())}.webp"
#             final_path = os.path.join("generated", filename)
#             os.makedirs("generated", exist_ok=True)
#             with open(local_path, "rb") as src, open(final_path, "wb") as dst:
#                 dst.write(src.read())

#             return final_path  # << Path for Streamlit to load/display

#         except Exception as e:
#             return f"❌ Error during image generation: {e}"

#     def run(self, input_data: str) -> str:
#         return self.generate(input_data)

