// UpdateProductForm.js
import React, { useState } from 'react';

const UpdateProductForm = ({ product, onClose, refreshProducts }) => {
    const [name, setName] = useState(product.name);
    const [uploadedImages, setUploadedImages] = useState([]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append('name', name);
    
        uploadedImages.forEach((file) => {
          formData.append('uploaded_images', file);
        });
    
        try {
          const response = await fetch(`http://localhost:5001/product/${product.id}/`, {
            method: 'PUT',
            credentials: 'include',
            body: formData,
          });
    
          if (!response.ok) {
            console.error('Failed to update product:', response.statusText);
            return;
          }
    
          const data = await response.json();
          console.log('Product updated:', data);
          setName('');
          setUploadedImages([]);
    
        } catch (error) {
          console.error('Failed to create product:', error);
        }
        refreshProducts();
        onClose();
    };

    return (
        <div className="Auth-form-container">
          <form className="Auth-form" onSubmit={handleSubmit}>
          <div className="Auth-form-content">
            <h3 className="Auth-form-title">Update Product</h3>
    
            <div className="form-group mt-3">
              <label>Product Name</label>
              <input
                type="text"
                className="form-control mt-1"
                placeholder="Enter product name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>
    
            <div className="form-group mt-3">
              <label>Upload Images</label>
              <input
                type="file"
                className="form-control mt-1"
                multiple
                onChange={(e) => setUploadedImages([...e.target.files])}
              />
            </div>
    
            <div className="d-grid gap-2 mt-3">
              <button type="submit" className="btn btn-primary">
                Update Product
              </button>
            </div>
            </div>
          </form>
        </div>
      );
};

export default UpdateProductForm;
