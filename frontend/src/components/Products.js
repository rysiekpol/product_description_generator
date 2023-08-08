import React, { useEffect, useState } from 'react';

const Products = () => {
  const [products, setProducts] = useState([]);
  
  useEffect(() => {
    fetch('http://localhost:5001/product/', {
        method: 'GET',
        credentials: 'include',  // <--- add this line
        })
      .then(response => response.json())
      .then(data => setProducts(data.results));
  }, []);

  return (
    <div className="container mt-5">
      {products.map((product, index) => (
        <div className="card mb-4" key={index}>
          <div className="card-body">
            <h5 className="card-title">{product.name}</h5>
            <a href={product.share_link} className="card-link">Share Link</a>
            <p className="card-text">
              {product.descriptions.map((desc, i) => (
                <span key={i}>{desc.description}</span>
              ))}
            </p>
            {product.images.map((img, i) => (
              <div key={i}>
                <img src={img.image_url} alt={`Product ${index + 1}`} className="img-fluid" />
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};

export default Products;