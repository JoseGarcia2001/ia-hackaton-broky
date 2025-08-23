import os
import glob
from src.app.services.openai import process_images_with_prompt

def process_all_images():
    input_folder = "src/app/resources/without_filter"
    output_folder = "src/app/resources/with_filter"
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.JPG', '*.PNG', '*.JPEG']
    image_files = []
    
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(input_folder, ext)))
    
    print(f"Encontradas {len(image_files)} imágenes para procesar...")
    
    for i, image_path in enumerate(image_files, 1):
        filename = os.path.basename(image_path)
        name_without_ext = os.path.splitext(filename)[0]
        output_filename = os.path.join(output_folder, f"{name_without_ext}_processed.png")
        
        print(f"Procesando imagen {i}/{len(image_files)}: {filename}")
        
        try:
            success = process_images_with_prompt(
                "images_pretty_short.txt", 
                [image_path], 
                output_filename
            )
            
            if success:
                print(f"✅ Imagen procesada exitosamente: {output_filename}")
            else:
                print(f"❌ Error procesando: {filename}")
                
        except Exception as e:
            print(f"❌ Error con {filename}: {str(e)}")
    
    print("🎉 Procesamiento completado!")

if __name__ == "__main__":
    process_all_images()
