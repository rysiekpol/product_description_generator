import React, { useEffect, useState, useContext } from 'react';
import Slider from "react-slick";
import "slick-carousel/slick/slick.css"; 
import "slick-carousel/slick/slick-theme.css";
import TokenContext from './TokenContext';  // Adjust the path accordingly.

const Products = () => {
  const [products, setProducts] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [nextPage, setNextPage] = useState(null);
  const [prevPage, setPrevPage] = useState(null);
  const { isTokenChecked } = useContext(TokenContext);

  const settings = {
    dots: true,
    infinite: true,
    speed: 300,
    slidesToShow: 1,
    slidesToScroll: 1,
  };

  useEffect(() => {
    console.log('isTokenChecked:', isTokenChecked);
    if (!isTokenChecked) return;
    const getProducts = async () => {
    try{
      await fetch(`http://localhost:5001/product?page=${currentPage}/`, {
          method: 'GET',
          credentials: 'include',
          })
        .then(response => response.json())
        .then(data => {
          setProducts(data.results);
          setNextPage(data.next);
          setPrevPage(data.previous);
        });
    } catch (error) {
      console.log(error);
    }
  };
  getProducts();
  }, [currentPage, isTokenChecked]);

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
    <div className="container mt-5 justify-content-center w-50">
      {products.map((product, index) => (
        <div className="card mb-4 mt-5" key={index}>
          <div className="card-body">
            <h5 className="card-title">{product.name}</h5>
            <a href={product.share_link} className="card-link">Update</a>
              {/* Image Grid */}
            {/* <div className="row"> */}
            <Slider {...settings} className='container mb-5 w-75 justify-content-center'>
              {product.images.map((img, i) => (
                <div key={i} >
                  <img 
                    src={img.image_url} 
                    alt={`Product ${index + 1}`} 
                    style={{objectFit: 'cover'}}
                    className="w-100 shadow-1-strong rounded"
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
    
  );
};

export default Products;