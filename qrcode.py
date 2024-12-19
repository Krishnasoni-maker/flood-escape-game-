import qrcode

# Replace this with your game's direct link
game_link = "https://github.com/Krishnasoni-maker/flood-escape-game-.git"

# Generate QR Code
qr = qrcode.QRCode(
    version=1,  # Controls the size of the QR Code
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)
qr.add_data(game_link)
qr.make(fit=True)

# Create an image of the QR code
img = qr.make_image(fill="black", back_color="white")
img.save("game_qr_code.png")

print("QR code generated and saved as game_qr_code.png")
