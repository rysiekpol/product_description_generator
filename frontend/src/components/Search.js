import React, { useEffect, useState } from 'react';

const Search = () => {
  const [products, setProducts] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`http://localhost:5001/search/${searchTerm}`, {
          method: 'GET',
          credentials: 'include',
        });

        if (!response.ok) {
          console.error('Failed to fetch products:', response.statusText);
          return;
        }

        const data = await response.json();
        setProducts(data.results);
      } catch (error) {
        console.error('Failed to fetch products:', error);
      }
    };

     if (searchTerm) {
        fetchData();
      }
    }, [searchTerm]);

  return (
    <>
    <div class="input-group input-group-lg mb-3">
        <span class="input-group-text" id="basic-addon1">?</span>
        <input 
            type="text" 
            class="form-control" 
            placeholder="Search for a product..." 
            aria-label="Search" 
            aria-describedby="basic-addon1" 
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
        />
    </div>
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
    </>

  );
};

export default Search;