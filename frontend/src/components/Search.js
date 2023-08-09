import React, { useEffect, useState } from 'react';
import Slider from "react-slick";
import "slick-carousel/slick/slick.css"; 
import "slick-carousel/slick/slick-theme.css";
import UpdateProduct from './UpdateProduct';  // Adjust the path if needed

const Search = () => {
  const [products, setProducts] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const [nextPage, setNextPage] = useState(null);
  const [prevPage, setPrevPage] = useState(null);
  const [showUpdateForm, setShowUpdateForm] = useState(false);
  const [currentProduct, setCurrentProduct] = useState(null);


  const settings = {
    dots: true,
    infinite: true,
    speed: 300,
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows:false,
  };

  const refreshProducts = async () => {
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
};


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

    const renderProducts = () => {
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

        <div className="container mt-5 justify-content-center w-50">
          {products.map((product, index) => (
            <div className="card mb-4 mt-5" key={index}>
              <div className="card-body">
                <h5 className="card-title">{product.name}</h5>
                <button href="#" className="link-primary link-button" onClick={(e) => {
                    e.preventDefault();
                    setCurrentProduct(product);
                    setShowUpdateForm(true);
                }}>Update</button>
  
  
                  {/* Image Grid */}
                {/* <div className="row"> */}
                <Slider {...settings} className='container mb-5 w-75 justify-content-center'>
                  {product.images.map((img, i) => (
                    <div key={i} 
                    style={{ 
                      position: 'relative',   // Ensure the child img is positioned in relation to this div
                  }}>
                      <img 
                        src={img.image_url} 
                        alt={`Product ${index + 1}`} 
                        style={{
                          display: 'flex',
                          margin: '0 auto',
                          height: '50vh',
                          width: '80%',
                          borderRadius: '5%',
                          objectFit: 'cover',
                      }}
                        className="w-75 shadow-1-strong"
                      />
                    </div>
                  ))}
                </Slider>
                {/* </div> */}
                <p className="card-text">
                {product.descriptions.length === 0 ? (
                  <button 
                    className="btn btn-primary"
                    onClick={() => handleAddDescription(product.id)}
                  >
                    Add description
                  </button>
                ) : (
                  product.descriptions.map((desc, i) => (
                    <span key={i}>{desc.description}</span>
                  ))
                )}
              </p>
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

    const handleAddDescription = (productId) => {
      fetch('http://localhost:5001/description/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          product_id: productId,
        }),
      })
      .then(response => response.json())
      .then(data => {
        // Handle success, maybe update the UI or display a success toast
        console.log('Description added:', data);
      })
      .catch((error) => {
        // Handle error, maybe display a toast or log the error
        console.error('Error:', error);
      });
    }
  
    return (
      <div>
        {showUpdateForm ? (
          <UpdateProduct
            product={currentProduct} 
            onClose={() => {
              setShowUpdateForm(false);
              setCurrentProduct(null);
            }} 
            refreshProducts={refreshProducts}
          />
        ) : (
          renderProducts() // Render product list if not showing update form
        )}
      </div>
    );
};

export default Search;
