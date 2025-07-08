from gradio_client import Client

client = Client("NihalGazi/FLUX-Pro-Unlimited")
result = client.predict(
		prompt="Cats and Dogs in Jungle",
		width=1280,
		height=1280,
		seed=0,
		randomize=True,
		server_choice="Google US Server",
		api_name="/generate_image"
)
print(result)