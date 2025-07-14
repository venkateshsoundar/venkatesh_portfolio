import fitz  # PyMuPDF
import os
import json
import requests

# Step 1: Download the PDF from GitHub if you want to run directly
pdf_url = "https://github.com/venkateshsoundar/venkatesh_portfolio/raw/main/Venkateshwaran_Resume.pdf"
pdf_local_path = "Venkateshwaran_Resume.pdf"

if not os.path.exists(pdf_local_path):
    print("Downloading PDF from GitHub...")
    r = requests.get(pdf_url)
    with open(pdf_local_path, 'wb') as f:
        f.write(r.content)
    print("Download completed.")

# Step 2: Extract text and images from the PDF

output_dir = 'extracted_resume_images'
os.makedirs(output_dir, exist_ok=True)

doc = fitz.open(pdf_local_path)
pdf_data = []

for page_num in range(len(doc)):
    page = doc[page_num]
    
    # Extract text from page
    text = page.get_text("text")
    
    # Extract images from page
    images = []
    for img_index, img in enumerate(page.get_images(full=True)):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        image_name = f"page{page_num+1}_img{img_index+1}.{image_ext}"

        image_path = os.path.join(output_dir, image_name)
        with open(image_path, "wb") as img_file:
            img_file.write(image_bytes)
        
        images.append(image_path)  # Save image path
    
    pdf_data.append({
        "page": page_num + 1,
        "text": text,
        "images": images
    })

# Step 3: Save extracted data as JSON
json_path = "Venkateshwaran_Resume_content.json"
with open(json_path, "w", encoding='utf-8') as json_file:
    json.dump(pdf_data, json_file, indent=4)

print(f"Extraction complete!")
print(f"JSON saved to: {json_path}")
print(f"Images saved to folder: {output_dir}")
