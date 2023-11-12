import re
import cv2
import pytesseract
import matplotlib.pyplot as plt


def ktp_scan(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to preprocess the image
    ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

    # Tampilkan gambar setelah thresholding
    plt.imshow(thresh, cmap='gray')
    plt.title('Hasil Global Thresholding')
    plt.axis('off')
    plt.show()

    # Use pytesseract to extract text from the image
    text = pytesseract.image_to_string(thresh)

    print(text)

def read_ktp(ktp_path):
    img = cv2.imread(ktp_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    th, threshed = cv2.threshold(gray, 127, 255, cv2.THRESH_TRUNC)
    threshed = threshed[5:650][20:1000]

    result = pytesseract.image_to_string(threshed)

    data = {
        'nama': '',
        'nik': '',
        'tempat_tanggal_lahir': '',
        'alamat': '',
        'rt_rw': '',
        'golongan_darah': '',
        'jenis_kelamin': '',
        'kel_desa': '',
        'kecamatan': '',
        'agama': '',
        'status_perkawinan': '',
        'pekerjaan': '',
        'kewarganegaraan': ''
        # Add more fields as needed
    }

    current_field = None
    for line in result.split("\n"):
        if "NIK" in line:
            nik_match = re.search(r'NIK[^\d]*(\d+)', line)
            if nik_match:
                data['nik'] = nik_match.group(1)
            current_field = 'nik'
        elif "Nama" in line:
            data['nama'] = line.replace("Nama", "").strip()
            current_field = 'nama'
        elif "Tempat/Tgl Lahir" in line:
            data['tempat_tanggal_lahir'] = line.replace("Tempat/Tgl Lahir", "").strip()
            current_field = 'tempat_tanggal_lahir'
        elif "Alamat" in line:
            data['alamat'] = line.replace("Alamat", "").strip()
            current_field = 'alamat'
        elif "RT/RW" in line:
            data['rt_rw'] = line.replace("RT/RW", "").strip()
            current_field = 'rt_rw'
        elif "Jenis Kelamin" in line:
            data['jenis_kelamin'] = line.replace("Jenis Kelamin", "").strip()
            current_field = 'jenis_kelamin'
        elif "Gol. Darah" in line:
            data['golongan_darah'] = line.replace("Gol. Darah", "").strip()
            current_field = 'golongan_darah'
        elif "Kel/Desa" in line:
            data['kel_desa'] = line.replace("Kel/Desa", "").strip()
            current_field = 'kel_desa'
        elif "Kecamatan" in line:
            data['kecamatan'] = line.replace("Kecamatan", "").strip()
            current_field = 'kecamatan'
        elif "Agama" in line:
            data['agama'] = line.replace("Agama", "").strip()
            current_field = 'agama'
        elif "Status Perkawinan" in line:
            data['status_perkawinan'] = line.replace("Status Perkawinan", "").strip()
            current_field = 'status_perkawinan'
        elif "Pekerjaan" in line:
            data['pekerjaan'] = line.replace("Pekerjaan", "").strip()
            current_field = 'pekerjaan'
        elif "Kewarganegaraan" in line:
            data['kewarganegaraan'] = line.replace("Kewarganegaraan", "").strip()
            current_field = 'kewarganegaraan'
        elif current_field:
            data[current_field] += " " + line.strip()

    return data



# Load the image in BGR format
image_path = 'temp_image.jpg'
bgr_image = cv2.imread(image_path)

# Convert BGR to RGB
rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)

ocr_data = read_ktp(image_path)

# Display the structured OCR results with labels
plt.figure(figsize=(12, 8))
plt.subplot(121), plt.imshow(rgb_image), plt.title("Citra Asli")

# Prepare the formatted text for display
formatted_text = []
for field, value in ocr_data.items():
    formatted_text.append(f"{field.capitalize()}: {value}")

formatted_text = "\n".join(formatted_text)

plt.subplot(122), plt.text(0.5, 0.5, formatted_text, fontsize=12, ha='left', va='top')
plt.axis('off')
plt.show()

# Print the structured data
for field, value in ocr_data.items():
    print(f"{field.capitalize()}: {value}")

        
