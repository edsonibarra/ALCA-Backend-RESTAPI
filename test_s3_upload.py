#!/usr/bin/env python
import os
import django
import io
from PIL import Image

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from property.models import PropertyImage, HouseForSale
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile

def create_test_image():
    """Create a simple test image"""
    # Create a simple red image
    img = Image.new('RGB', (100, 100), color='red')
    img_io = io.BytesIO()
    img.save(img_io, format='JPEG')
    img_io.seek(0)
    return img_io.getvalue()

def test_image_upload():
    print("=== Testing Image Upload to S3 ===")
    
    # Get or create a test house
    try:
        house = HouseForSale.objects.first()
        if not house:
            print("No houses found. Creating a test house...")
            from owner.models import Owner
            owner = Owner.objects.first()
            if not owner:
                print("No owners found. Please create an owner first.")
                return
            
            house = HouseForSale.objects.create(
                title="Test House for S3",
                owner=owner,
                selling_cost=100000
            )
            print(f"Created test house: {house.id}")
        else:
            print(f"Using existing house: {house.id}")
    except Exception as e:
        print(f"Error getting/creating house: {e}")
        return
    
    # Create test image file
    try:
        image_data = create_test_image()
        image_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=image_data,
            content_type='image/jpeg'
        )
        print("✓ Test image created")
    except Exception as e:
        print(f"✗ Error creating test image: {e}")
        return
    
    # Upload image
    try:
        content_type = ContentType.objects.get_for_model(HouseForSale)
        
        property_image = PropertyImage.objects.create(
            image=image_file,
            caption="Test image for S3",
            is_main=True,
            order=1,
            content_type=content_type,
            object_id=house.id
        )
        
        print(f"✓ Image uploaded successfully!")
        print(f"Image ID: {property_image.id}")
        print(f"Image path: {property_image.image.name}")
        print(f"Image URL: {property_image.image.url}")
        
        # Test secure URL generation
        secure_url = property_image.get_secure_url()
        if secure_url:
            print(f"✓ Secure URL generated: {secure_url[:100]}...")
        else:
            print("✗ Failed to generate secure URL")
            
    except Exception as e:
        print(f"✗ Error uploading image: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_image_upload()