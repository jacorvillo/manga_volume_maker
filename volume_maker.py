#!/usr/bin/env python3
"""
Manga Chapter Merger Script

This script merges multiple manga chapters into a single CBZ file with sequential page numbering.
Given a range of chapters (e.g., 26-30), it will copy all images from those chapters
into a temporary folder, rename them sequentially from 001 onwards, then compress
everything into a CBZ file (Comic Book ZIP format).

Usage:
    python merge_manga_chapters.py [cover_image_path] <start_chapter> <end_chapter> [output_filename]

Example:
    python merge_manga_chapters.py 26 30
    python merge_manga_chapters.py "cover.jpg" 26 30
    python merge_manga_chapters.py "cover.jpg" 26 30 "Volume_7"
"""

import os
import shutil
import sys
import re
import zipfile


def find_chapter_folders(base_path, start_chapter, end_chapter):
    """Find all chapter folders within the specified range."""
    chapter_folders = []
    
    # Get all directories in the base path
    for item in os.listdir(base_path):
        item_path = os.path.join(base_path, item)
        if os.path.isdir(item_path):
            # Extract chapter number from folder name
            match = re.match(r'Chapter (\d+)', item)
            if match:
                chapter_num = int(match.group(1))
                if start_chapter <= chapter_num <= end_chapter:
                    chapter_folders.append((chapter_num, item_path))
    
    # Sort by chapter number
    chapter_folders.sort(key=lambda x: x[0])
    return chapter_folders


def get_image_files(folder_path):
    """Get all image files from a folder, sorted by their numeric order."""
    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
    image_files = []
    
    try:
        for file in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file)
            if os.path.isfile(file_path):
                _, ext = os.path.splitext(file.lower())
                if ext in image_extensions:
                    image_files.append((file, file_path))
    except OSError as e:
        print(f"Error reading folder {folder_path}: {e}")
        return []
    
    # Sort by numeric value in filename
    def extract_number(filename):
        match = re.search(r'(\d+)', filename)
        return int(match.group(1)) if match else 0
    
    image_files.sort(key=lambda x: extract_number(x[0]))
    return image_files


def merge_chapters(base_path, start_chapter, end_chapter, output_folder=None, cover_image_path=None):
    """Merge chapters within the specified range into a single folder and create CBZ file."""
    
    # Create output folder name if not provided
    if output_folder is None:
        if start_chapter == end_chapter:
            output_folder = f"Chapter_{start_chapter}_merged"
        else:
            output_folder = f"Chapters_{start_chapter}-{end_chapter}_merged"
    
    output_path = os.path.join(base_path, output_folder)
    cbz_filename = f"{output_folder}.cbz"
    cbz_path = os.path.join(base_path, cbz_filename)
    
    # Check if CBZ file already exists
    if os.path.exists(cbz_path):
        response = input(f"CBZ file '{cbz_filename}' already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("Operation cancelled.")
            return False
        os.remove(cbz_path)
    
    # Validate cover image if provided
    if cover_image_path:
        if not os.path.exists(cover_image_path):
            print(f"❌ Cover image not found: {cover_image_path}")
            return False
        
        # Check if it's a valid image file
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        _, ext = os.path.splitext(cover_image_path.lower())
        if ext not in image_extensions:
            print(f"❌ Invalid cover image format: {ext}. Supported formats: {', '.join(image_extensions)}")
            return False
        
        print(f"📖 Using cover image: {os.path.basename(cover_image_path)}")
    
    # Create temporary output directory
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    
    os.makedirs(output_path)
    print(f"Created temporary folder: {output_path}")
    
    # Find chapter folders
    chapter_folders = find_chapter_folders(base_path, start_chapter, end_chapter)
    
    if not chapter_folders:
        print(f"No chapters found in range {start_chapter}-{end_chapter}")
        return False
    
    print(f"Found {len(chapter_folders)} chapters:")
    for chapter_num, folder_path in chapter_folders:
        folder_name = os.path.basename(folder_path)
        print(f"  Chapter {chapter_num}: {folder_name}")
    
    # Process cover image first if provided
    page_counter = 1
    total_pages = 0
    
    if cover_image_path:
        print(f"\n📖 Processing cover image...")
        _, ext = os.path.splitext(cover_image_path.lower())
        cover_name = f"{page_counter:03d}{ext}"
        cover_dest = os.path.join(output_path, cover_name)
        
        try:
            shutil.copy2(cover_image_path, cover_dest)
            print(f"    {os.path.basename(cover_image_path)} -> {cover_name} (COVER)")
            page_counter += 1
            total_pages += 1
        except Exception as e:
            print(f"    Error copying cover image: {e}")
            return False
    
    # Process each chapter
    for chapter_num, folder_path in chapter_folders:
        print(f"\nProcessing Chapter {chapter_num}...")
        
        # Get all image files from this chapter
        image_files = get_image_files(folder_path)
        
        if not image_files:
            print(f"  No image files found in Chapter {chapter_num}")
            continue
        
        print(f"  Found {len(image_files)} pages")
        
        # Copy and rename each image file
        for original_name, original_path in image_files:
            # Get file extension
            _, ext = os.path.splitext(original_name.lower())
            
            # Create new filename with zero-padding
            new_name = f"{page_counter:03d}{ext}"
            new_path = os.path.join(output_path, new_name)
            
            try:
                shutil.copy2(original_path, new_path)
                print(f"    {original_name} -> {new_name}")
                page_counter += 1
                total_pages += 1
            except Exception as e:
                print(f"    Error copying {original_name}: {e}")
    
    # Create CBZ file
    print(f"\n📦 Creating CBZ file: {cbz_filename}")
    try:
        with zipfile.ZipFile(cbz_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=6) as cbz_file:
            for root, dirs, files in os.walk(output_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, output_path)
                    cbz_file.write(file_path, arcname)
                    print(f"    Added to CBZ: {arcname}")
        
        # Get CBZ file size
        cbz_size = os.path.getsize(cbz_path)
        cbz_size_mb = cbz_size / (1024 * 1024)
        
        print(f"\n✅ Successfully created CBZ file!")
        print(f"📖 Total pages: {total_pages}")
        if cover_image_path:
            print(f"📘 Cover image: {os.path.basename(cover_image_path)}")
        print(f"📁 CBZ file: {cbz_filename}")
        print(f"💾 File size: {cbz_size_mb:.2f} MB")
        
        # Clean up temporary folder
        print(f"\n🧹 Cleaning up temporary folder...")
        shutil.rmtree(output_path)
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating CBZ file: {e}")
        # Clean up temporary folder even if CBZ creation failed
        if os.path.exists(output_path):
            shutil.rmtree(output_path)
        return False


def main():
    """Main function to parse arguments and execute the merge."""
    
    if len(sys.argv) < 3:
        print("Usage: python merge_manga_chapters.py [cover_image_path] <start_chapter> <end_chapter> [output_filename]")
        print("\nExamples:")
        print("  python merge_manga_chapters.py 26 30")
        print("  python merge_manga_chapters.py 'cover.jpg' 26 30")
        print("  python merge_manga_chapters.py 'cover.jpg' 26 30 'Volume_7'")
        print("\nNote: Output will be a CBZ file (Comic Book ZIP format)")
        print("      Cover image will be placed as the first page (001)")
        print("      Cover image path is optional and can be first parameter")
        sys.exit(1)
    
    try:
        # Parse arguments - cover image is optional and can be first parameter
        args = sys.argv[1:]
        cover_image_path = None
        start_chapter = None
        end_chapter = None
        output_folder = None
        
        # Check if first argument is a cover image (not a number)
        if not args[0].isdigit():
            # First argument is cover image path
            cover_image_path = args[0]
            if len(args) < 3:
                print("Error: Not enough arguments provided")
                print("When using cover image, format: [cover_image] <start_chapter> <end_chapter> [output_filename]")
                sys.exit(1)
            start_chapter = int(args[1])
            end_chapter = int(args[2])
            output_folder = args[3] if len(args) > 3 else None
        else:
            # First argument is start chapter
            start_chapter = int(args[0])
            if len(args) < 2:
                print("Error: End chapter is required")
                sys.exit(1)
            end_chapter = int(args[1])
            output_folder = args[2] if len(args) > 2 else None
        
        if start_chapter > end_chapter:
            print("Error: Start chapter must be less than or equal to end chapter")
            sys.exit(1)
        
        # Validate cover image path if provided
        if cover_image_path and not os.path.isabs(cover_image_path):
            # Convert relative path to absolute path
            cover_image_path = os.path.abspath(cover_image_path)
        
        # Use the directory where the script is located as base path
        base_path = os.path.dirname(os.path.abspath(__file__))
        
        print(f"🔍 Searching for chapters {start_chapter}-{end_chapter} in: {base_path}")
        if cover_image_path:
            print(f"📖 Cover image: {cover_image_path}")
        
        success = merge_chapters(base_path, start_chapter, end_chapter, output_folder, cover_image_path)
        
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
            
    except ValueError:
        print("Error: Chapter numbers must be integers")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
