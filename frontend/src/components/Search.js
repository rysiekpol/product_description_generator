import React, { useEffect, useState } from 'react';

const Search = () => {
  const [products, setProducts] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [nextPage, setNextPage] = useState(null);
  const [prevPage, setPrevPage] = useState(null);
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(`http://localhost:5001/search/${searchTerm}?page=${currentPage}`, {
          method: 'GET',
          credentials: 'include',
        });

        if (!response.ok) {
          console.error('Failed to fetch products:', response.statusText);
          return;
        }

        const data = await response.json();
        setProducts(data.results);
        setNextPage(data.next);
        setPrevPage(data.previous);
      } catch (error) {
        console.error('Failed to fetch products:', error);
      }
    };

     if (searchTerm) {
        fetchData();
      }
    }, [searchTerm, currentPage]);

  return (
    <>
    <div className="d-flex justify-content-center mt-5">
      <div className="input-group input-group-lg w-50">
          <span className="input-group-text" id="basic-addon1">?</span>
          <input 
              id="typeText"
              type="text" 
              className="form-control" 
              placeholder="Search for a product..." 
              aria-label="Search" 
              aria-describedby="basic-addon1" 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
          />
      </div>
    </div>
    <div className="container mt-2 justify-content-center w-50">
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
    </>
  );
};

export default Search;
