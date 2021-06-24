import cv2
import os
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request



def facecrop(imgname):
   img = cv2.imread(imgname)

   imgname = imgname.split('.')

   detected = f"{imgname[0]}_detected.{imgname[1]}"

   gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

   face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

   faces = face_cascade.detectMultiScale(gray, 1.1, 4)

   counter = 0
   for (x, y, w, h) in faces:
      cv2.rectangle(img, (x - 50, y - 50), (x + w + 50, y + h + 50), (0, 0, 255), 4)
      faces = img[y - 50: y + h + 50, x - 50: x + w + 50]

      name = f'{imgname[0]}_face_{counter}'

      counter += 1

      cv2.imwrite(f'Cropped_Image/{name}.jpg', faces)


   cv2.imwrite(f'static/{detected}', img)


@app.route("/", methods=['GET', 'POST'])

def upload_file():
   Alert = ""
   if request.method == 'POST':
      file = request.files['file-1']

      extension  = file.filename.split(".")

      if file.filename == '':
         Alert = "Please Select A File"
         Alert1 = ""
         return render_template('Upload.html', Alert=Alert)


      if extension[1] == "jpg" or extension[1] == "jpeg":
         filename = secure_filename(file.filename)
         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

         facecrop(f"Images/{file.filename}")

         x = filename.split('.')
         x[0] = f"{x[0]}_detected"
         filename = '.'.join(x)
         return render_template('Upload.html', Alert = filename)

      else:
         return render_template('Upload.html', Alert1 = "INVALID FILE FORMAT")

   else:
      return render_template('Upload.html')


if __name__ == "__main__":
   UPLOAD_FOLDER = os.path.join(os.getcwd(), "Images")

   app = Flask(__name__)
   app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
   app.run(debug=True)
