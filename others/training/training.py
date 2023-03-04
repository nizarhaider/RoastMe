import pandas as pd
import urllib.request
from PIL import Image
from mtcnn import MTCNN
from facenet_pytorch import InceptionResnetV1
import numpy as np
import cv2
import torch
from tqdm import tqdm
from scipy.spatial import distance
import itertools

# Load model
model = InceptionResnetV1(pretrained='vggface2').eval().to('cpu')

# Initialize the MTCNN detector
detector = MTCNN()

# Load dataframe
df = pd.read_csv('others/training/cleaned_output.csv')

# url column name
url_col = 'image_url'

# Create a column to store the facial embeddings
df['embeddings'] = None

# Image size
img_size = (256,256)

counter = 0


# Define batch size
batch_size = 32

# Group rows in DataFrame into batches
batches = [df.iloc[i:i+batch_size] for i in range(0, len(df), batch_size)]
print(df)
# Iterate over batches
for batch in tqdm(batches, total=len(batches), desc="batches processed"):
    print(batch)
  # Process batch of imagesq
    for index, row in batch.iterrows():
      url = row[url_col]
      try:
          urllib.request.urlopen(url)
          # Download the image
          try:
            image = Image.open(urllib.request.urlretrieve(url)[0])
            image = image.resize(img_size)
            # Convert PIL.Image to numpy.ndarray
            img = np.array(image)
            # Change image color from RGB to BGR
            img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            # Detect the faces in the image
            faces = detector.detect_faces(img)
            if faces:
                face_bounding_box = faces[0]['box']
                # Crop the face from the image
                face_cropped = image.crop((face_bounding_box[0], face_bounding_box[1], face_bounding_box[0]+face_bounding_box[2], face_bounding_box[1] + face_bounding_box[3]))
                # Convert PIL.Image to numpy.ndarray
                face_cropped = np.array(face_cropped)
                # Change image color from RGB to BGR
                face_cropped = cv2.cvtColor(face_cropped, cv2.COLOR_RGB2BGR)
                # Resize the face_cropped tensor to match the expected input size of the model
                face_cropped = cv2.resize(face_cropped, (160, 160)).astype(float)
                # Reorder dimensions of your image data so it is in HWC format
                face_cropped = face_cropped.transpose((2, 0, 1))
                # Normalize the pixel values to be between -1 and 1
                face_cropped = (face_cropped / 255) * 2 - 1
                # Convert numpy.ndarray to tensor
                face_cropped = torch.from_numpy(face_cropped)
                # Extract the facial embeddings
                face_cropped = face_cropped.float()
                face_cropped = torch.unsqueeze(face_cropped, 0)
                face_cropped = face_cropped.to('cpu')

                face_embeddings = model(face_cropped)[0]
                # Save face_embeddings to the dataframe
                df.at[index, 'embeddings'] = face_embeddings
          except:
            counter += 1
            continue

      except urllib.error.HTTPError as e:
          # Image is not accessible, skip this iteration
          counter += 1
          continue

print(f"/n {counter} images were removed")
#Save the dataframe to a new file
df.dropna(inplace=True)
df['embeddings'] = df['embeddings'].apply(lambda x: (x.detach().cpu().numpy()))
df.to_csv('data_with_embeddings.csv', index=False)