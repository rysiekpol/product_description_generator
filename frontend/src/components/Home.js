import React, { useState } from 'react';

const Home = () => {
  const [name, setName] = useState('');
  const [uploadedImages, setUploadedImages] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('name', name);

    uploadedImages.forEach((file) => {
      formData.append('uploaded_images', file);
    });

    try {
      const response = await fetch('http://localhost:5001/product/', {
        method: 'POST',
        credentials: 'include',
        body: formData,
      });

      if (!response.ok) {
        console.error('Failed to create product:', response.statusText);
        return;
      }

      const data = await response.json();
      console.log('Product created:', data);
      // Clear the form for a new submission or give user feedback
      setName('');
      setUploadedImages([]);

    } catch (error) {
      console.error('Failed to create product:', error);
    }
  };

  return (
    <div className="Auth-form-container">
      <form className="Auth-form" onSubmit={handleSubmit}>
      <div className="Auth-form-content">
        <h3 className="Auth-form-title">Create Product</h3>

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
            Create Product
          </button>
        </div>
        </div>
      </form>
    </div>
  );
};

export default Home;
