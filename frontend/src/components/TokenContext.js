import React from 'react';

const TokenContext = React.createContext({
  isTokenChecked: false,
  setTokenChecked: () => {}
});

export default TokenContext;
