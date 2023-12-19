import React, { useState, useEffect } from 'react';
import axios from 'axios';

const App = () => {
  const [amount, setAmount] = useState(1);
  const [result, setResult] = useState('');
  const [targetCurrency, setTargetCurrency] = useState('EUR');
  const [rates, setRates] = useState({});
  const apiUrl = process.env.REACT_APP_API_URL || 'http://ccbackend:5000';

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

  const updateResult = async () => {
    try {
      const response = await axios.post(`http://localhost:5000/convert`, {
        targetCurrency,
        amount: parseFloat(amount),
      });

      setResult(response.data.result.toFixed(4));
    } catch (error) {
      console.error('Error:', error);
    }
  };

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://localhost:5000/exchange-rates'); // || 'http://ccbackend:5000/exchange-rates'
        const data = await response.data;
        const euroRate = data['EUR'];
        const usdRate = data['USD'];

        setRates({ euroRate, usdRate });
      } catch (error) {
        console.error('Error:', error);
      }
    };
    
    fetchData();
    updateResult();
  }, [amount, targetCurrency]);

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