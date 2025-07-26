import streamlit as st
from PIL import Image
import io
import os
from datetime import datetime

def compress_image(image, max_size_mb=0.9, quality=75):
    """Compress an image to be under max_size_mb (in MB)"""
    img = Image.open(image)
    
    # Convert to RGB if needed
    if img.mode in ('RGBA', 'LA'):
        img = img.convert('RGB')
    
    img_byte_arr = io.BytesIO()
    current_quality = quality
    
    while True:
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG', quality=current_quality)
        size_mb = img_byte_arr.tell() / (1024 * 1024)
        
        if size_mb <= max_size_mb or current_quality <= 10:
            break
            
        current_quality -= 5
    
    return img_byte_arr, current_quality

def main():
    st.title("Image Compression Tool")
    st.write("Upload an image to compress it to your desired size")
    
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
    
    if uploaded_file:
        # Show original file info
        original_size = uploaded_file.size / (1024 * 1024)
        st.write(f"Original file size: {original_size:.2f} MB")
        
        # Compression settings
        max_size = st.slider(
            "Target maximum size (MB)", 
            min_value=0.1, 
            max_value=5.0, 
            value=0.9,
            step=0.1
        )
        
        # Compress image
        compressed_img, final_quality = compress_image(uploaded_file, max_size_mb=max_size)
        compressed_size = compressed_img.tell() / (1024 * 1024)
        
        # Show results
        st.write(f"Compressed size: {compressed_size:.2f} MB (Quality: {final_quality})")
        

        name_opt = st.radio("Naming:", ["Preset", "Custom"], horizontal=True)
        base = os.path.splitext(uploaded_file.name)[0]
        
        if name_opt == "Preset":
            col1, col2 = st.columns(2)
            with col1: pre = st.text_input("Name (HKCR format)", "FUNG_HeiLongAdriel")
            with col2: suf = st.text_input("Class code", "MS")
            fname = f"{pre}_BasicCO25_{suf}"
        else:
            fname = st.text_input("Filename", f"{base}_compressed")
        
        # Download button
        st.download_button(
            label="Download Compressed Image",
            data=compressed_img,
            file_name=f"{fname}.jpg",
            mime="image/jpeg"
        )

if __name__ == "__main__":
    main()
