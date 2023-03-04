import urllib.request
from PIL import Image
from mtcnn import MTCNN
from facenet_pytorch import InceptionResnetV1
import numpy as np
import cv2
import torch
from scipy.spatial import distance

model = InceptionResnetV1(pretrained='vggface2').eval()
detector = MTCNN()
image_size=(256,400)

def find_closest_match(df, path,  threshold_norm=0.7):
    try:
        # Load the image
        image = cv2.imread(path)
        # image = Image.open(io.BytesIO(image.read()))
        # Convert PIL.Image to numpy.ndarray
        img = np.array(image)
        print(img.shape)
        # Change image color from RGB to BGR
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        # Detect the face in the image
        face = detector.detect_faces(img)[0]
        # Crop the face from the image
        face_cropped = img[face['box'][1]:face['box'][1] + face['box'][3], face['box'][0]:face['box'][0]+face['box'][2]]
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
        face_embedding = model(face_cropped)[0]
        # print(face_embedding.detach().numpy())
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
        # print(df['distance_norm'])
        # Find the index of the closest match
        closest_index = df['distance_norm'].idxmin()
        print("Similarity level: ", df.at[closest_index, 'distance_norm'])
        
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
    
