import cloudinary
from cloudinary.uploader import upload
          
cloudinary.config( 
  cloud_name = "dtghsmx0s", 
  api_key = "155646927271619", 
  api_secret = "kYyrS0ssz2NlVjQw0i17Z5ZnnfY" 
)

# Upload an image
response = upload("example.jpg")

# Print the URL of the uploaded image
print("Uploaded image URL:", response['secure_url'])
