from flask import Flask, render_template, request, send_file
import qrcode
import io
import base64

app = Flask(__name__)

# Route for the homepage
@app.route("/")
def home():
    return render_template("index.html")

# Route to generate and display the QR code
@app.route("/generate", methods=["POST"])
def generate_qr():
    # Get input data
    input_type = request.form.get("input_type")
    data = request.form.get("data")

    if not data:
        return "No data provided!", 400

    # Generate the QR code
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image in memory
    img_io = io.BytesIO()
    img.save(img_io, "PNG")
    img_io.seek(0)

    # Return the base64-encoded image to display on the webpage
    img_base64 = io.BytesIO()
    img.save(img_base64, "PNG")
    img_base64.seek(0)
    qr_base64 = base64.b64encode(img_base64.getvalue()).decode("utf-8")

    return render_template("result.html", qr_code=qr_base64, data=data)

# Route to download the QR code as an image
@app.route("/download", methods=["POST"])
def download_qr():
    data = request.form.get("data")

    # Generate the QR code
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image for download
    img_io = io.BytesIO()
    img.save(img_io, "PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png", download_name="qr_code.png", as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
