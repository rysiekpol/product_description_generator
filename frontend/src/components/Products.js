import React, { useEffect, useState } from 'react';


const Products = () => {
  const [products, setProducts] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [nextPage, setNextPage] = useState(null);
  const [prevPage, setPrevPage] = useState(null);

  useEffect(() => {
    fetch(`http://localhost:5001/product?page=${currentPage}/`, {
        method: 'GET',
        credentials: 'include',
        })
      .then(response => response.json())
      .then(data => {
        setProducts(data.results)
        setNextPage(data.next);
        setPrevPage(data.previous);
      });
  }, [currentPage]);

  return (
    <div className="container mt-5 justify-content-center w-50">
      {products.map((product, index) => (
        <div className="card mb-4 mt-5" key={index}>
          <div className="card-body">
            <h5 className="card-title">{product.name}</h5>
            <a href={product.share_link} className="card-link">Share Link</a>
            <p className="card-text">
              {product.descriptions.map((desc, i) => (
                <span key={i}>{desc.description}</span>
              ))}
            </p>
              {/* Image Grid */}
              <div className="row">
              {product.images.map((img, i) => (
                <div key={i} className="col-6 mb-4">
                  <a href={img.image_url}><img src={img.image_url} alt={`Product ${index + 1}`} style={{objectFit: 'cover'}} className="w-100 h-100 shadow-1-strong rounded mb-4"/></a>
                </div>
              ))}
            </div>
          </div>
        </div>
      ))}
      <div className="d-flex justify-content-center">
        <nav aria-label="Page navigation example">
          <ul className="pagination">
            <li className={`page-item ${!prevPage ? 'disabled' : ''}`}>
              <button className="page-link" onClick={() => setCurrentPage(currentPage - 1)}>Previous</button>
            </li>
            <li className={`page-item ${!nextPage ? 'disabled' : ''}`}>
              <button className="page-link" onClick={() => setCurrentPage(currentPage + 1)}>Next</button>
            </li>
          </ul>
        </nav>
      </div>
    </div>
    
  );
};

export default Products;