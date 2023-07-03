# import os
# from flask import Flask, flash, request, redirect, url_for, abort, session

# # UPLOAD_FOLDER = "Downloads/"
# # ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}

# app = Flask(__name__)
# # app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# # def allowed_file(filename):
# #     file_extension = filename.split(".")[-1] 
# #     if file_extension not in ALLOWED_EXTENSIONS:
# #         return {"message": "not valid file"}
    
# #     else:
# #         return {"file_name": filename}

# # @app.route("/", methods=["GET", "POST"])
# # def upload_file():
# #     if request.method == "POST":
# #         file = request.files["file"]

# #         if not file: 
# #             raise {"messsag": "please enter file"}
        
# #         return allowed_file(file.filename)


