import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';

const App = () => {
  const [amount, setAmount] = useState(1);
  const [result, setResult] = useState('');
  const [targetCurrency, setTargetCurrency] = useState('EUR');

  const handleAmountChange = (e) => {
    const value = e.target.value;
    if (value >= 1) {
      setAmount(value);
    } else {
      setAmount(1);
    }
  };

  const handleCurrencyChange = (e) => {
    const value = e.target.value;
    setTargetCurrency(value);
  };


  const updateResult = useCallback(() => {
    try {
      async function fetchResult() {
        const response = await axios.post(`http://localhost:5000/convert`, {
          targetCurrency,
          amount: parseFloat(amount),
        });

        setResult(response.data.result.toFixed(4));
      }

      fetchResult();
    } catch (error) {
      console.error('Error:', error);
    }
  }, [amount, targetCurrency]);

  useEffect(() => {
    updateResult();
  }, [updateResult]);

  return (
    <div>
      <h1>Currency Converter</h1>
      <div>
        <select value={targetCurrency} onChange={handleCurrencyChange}>
          <option value="USD">USD</option>
          <option value="EUR">EUR</option>
        </select>
      </div>
      <div>
        <input type="number" value={amount} onChange={handleAmountChange} />
      </div>
      <div>
        <p>Result: {result} PLN</p>
      </div>
    </div>
  );
};

export default App;