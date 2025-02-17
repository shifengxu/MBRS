from . import *
from .Encoder_MP import Encoder_MP, Encoder_MP_Diffusion
from .Decoder import Decoder, Decoder_Diffusion
from .Noise import Noise
import torchvision.transforms as transforms
from PIL import Image

class EncoderDecoder(nn.Module):
	'''
	A Sequential of Encoder_MP-Noise-Decoder
	'''

	def __init__(self, H, W, message_length, noise_layers):
		super(EncoderDecoder, self).__init__()
		self.encoder = Encoder_MP(H, W, message_length)
		self.noise = Noise(noise_layers)
		self.decoder = Decoder(H, W, message_length)
		self.upsample = transforms.Resize((1123, 794), interpolation=Image.BILINEAR)
		self.downsample = transforms.Resize((H, W), interpolation=Image.BILINEAR)

	def forward(self, image, message):
		encoded_image = self.encoder(image, message)
		# noised_image = self.noise([encoded_image, image])
		upsample_img = self.upsample(encoded_image)
		noised_image = self.noise([upsample_img, image])
		noised_image = self.downsample(noised_image)
		decoded_message = self.decoder(noised_image)
		return encoded_image, noised_image, decoded_message


class EncoderDecoder_Diffusion(nn.Module):
	'''
	A Sequential of Encoder_MP-Noise-Decoder
	'''

	def __init__(self, H, W, message_length, noise_layers):
		super(EncoderDecoder_Diffusion, self).__init__()
		self.encoder = Encoder_MP_Diffusion(H, W, message_length)
		self.noise = Noise(noise_layers)
		self.decoder = Decoder_Diffusion(H, W, message_length)

	def forward(self, image, message):
		encoded_image = self.encoder(image, message)
		noised_image = self.noise([encoded_image, image])
		decoded_message = self.decoder(noised_image)

		return encoded_image, noised_image, decoded_message
