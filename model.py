import urllib.request
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1
import numpy as np
import cv2
import torch
from scipy.spatial import distance

model = InceptionResnetV1(pretrained='vggface2').eval()
detector = MTCNN()
image_size = (256, 400)

def find_closest_match(df, path, threshold_norm=0.7):
    try:
        # Load the image
        image = cv2.imread(path)
        # Convert the image color from BGR to RGB
        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Detect the face in the image
        boxes, probs = detector.detect(img)
        if boxes is None:
            raise Exception("No face detected")
        
        # Use the first detected face
        box = boxes[0].astype(int)
        # Crop the face from the image
        face_cropped = img[box[1]:box[3], box[0]:box[2]]
        
        # Resize the face_cropped tensor to match the expected input size of the model
        face_cropped = cv2.resize(face_cropped, (160, 160)).astype(float)
        # Normalize the pixel values to be between -1 and 1
        face_cropped = (face_cropped / 255) * 2 - 1
        # Convert the face to tensor
        face_cropped = torch.tensor(face_cropped).permute(2, 0, 1).unsqueeze(0).float()
        # Extract the facial embeddings
        face_embedding = model(face_cropped)[0]
        print("Generated Embeddings")
        
        # Define the distance function
        def find_distance(x):
            if x is not None:
                return distance.euclidean(x, face_embedding.detach().numpy())
            else:
                return None
        
        # Apply the distance function to the 'embeddings' column of the dataframe
        df['distance'] = df['embeddings'].apply(find_distance)
        # Normalize the distance
        df['distance_norm'] = df['distance'] / df['distance'].max()
        # Find the index of the closest match
        closest_index = df['distance_norm'].idxmin()
        
        if df.at[closest_index, 'distance_norm'] < threshold_norm:
            # Return the 'comments' column of the closest match
            url = df.at[closest_index, 'image_url']
            image = Image.open(urllib.request.urlretrieve(url)[0])
            comments = df.at[closest_index, 'comments']
            fun_pass = "True"
            result = comments, image
            return fun_pass, result
        else:
            fun_pass = "Similarity not found"
            result = 0, 0
            return fun_pass, result

    except:
        fun_pass = "Cannot detect face"
        result = 0, 0
        return fun_pass, result
